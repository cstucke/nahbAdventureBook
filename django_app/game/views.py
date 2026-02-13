from django.shortcuts import render, redirect
import requests
from django.conf import settings
from .models import Play
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.
def get_headers():
    return {'X-API-KEY': settings.FLASK_API_KEY}

# Authentication Views

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Author Views

@login_required
def my_stories(request):
    try:
        api_url = f"{settings.FLASK_API_URL}/stories"
        response = requests.get(api_url, params={'author_id': request.user.id})
        stories = response.json()
    except requests.RequestException:
        stories = []
    
    return render(request, 'game/my_stories.html', {'stories': stories})

@login_required
def create_story(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        payload = {
            'title': title,
            'description': description,
            'status': 'draft',
            'author_id': request.user.id
        }
        
        try:
            response = requests.post(
                f"{settings.FLASK_API_URL}/stories", 
                json=payload,
                headers=get_headers() 
            )
            response.raise_for_status()
            return redirect('my_stories')
        except requests.RequestException:
             return render(request, 'game/error.html', {'message': "Failed to create story"})

    return render(request, 'game/create_story.html')

@login_required
def delete_story(request, story_id):
    try:
        res = requests.get(f"{settings.FLASK_API_URL}/stories/{story_id}")
        if res.status_code == 200:
            story = res.json()
            if story.get('author_id') != request.user.id:
                 return render(request, 'game/error.html', {'message': "Unauthorized"})
            
            requests.delete(
                f"{settings.FLASK_API_URL}/stories/{story_id}", 
                headers=get_headers()
            )
    except requests.RequestException:
        pass
        
    return redirect('my_stories')

# Public Views

def story_list(request):
    search_query = request.GET.get('q', '')

    try:
        api_url = f"{settings.FLASK_API_URL}/stories?status=published"

        if search_query:
            api_url += f"&q={search_query}"
        
        response = requests.get(api_url)
        stories = response.json()
    except requests.RequestException:
        stories = []

    for story in stories:
        story_id = story['id']
        story['has_save'] = request.session.get(f'progress_{story_id}') is not None

    return render(request, 'game/story_list.html', {'stories': stories, 'search_query': search_query})

@login_required
def play_story(request, story_id):
    page_id = request.GET.get('page')
    session_key = f'progress_{story_id}'
    
    
    if not page_id:

        saved_page = request.session.get(session_key)
        if saved_page:
            return redirect(f"/play/{story_id}?page={saved_page}")

        story_res = requests.get(f"{settings.FLASK_API_URL}/stories/{story_id}")
        if story_res.status_code != 200:
            return render(request, 'game/error.html', {'message': "Story not found"})
        
        story_data = story_res.json()
        if story_data.get('status') == 'suspended':
            return render(request, 'game/error.html', {'message': "This story is suspended."})
        
        start_page_id = story_data.get('start_page_id')
        if not start_page_id:
             return render(request, 'game/error.html', {'message': "Story has no start page"})
             
        return redirect(f"/play/{story_id}?page={start_page_id}")

    page_res = requests.get(f"{settings.FLASK_API_URL}/pages/{page_id}")
    if page_res.status_code != 200:
        return render(request, 'game/error.html', {'message': "Page not found"})

    page_data = page_res.json()

    if page_data.get('is_ending'):
        if session_key in request.session:
            del request.session[session_key]

        Play.objects.create(
            user=request.user,
            story_id=story_id,
            ending_page_id=page_data['id']
        )
    else:
        request.session[session_key] = page_id
    
    return render(request, 'game/play.html', {
        'story_id': story_id,
        'page': page_data
    })

def restart_story(request, story_id):
    session_key = f'progress_{story_id}'
    if session_key in request.session:
        del request.session[session_key]
    return redirect('story_list')

def global_stats(request):
    try:
        response = requests.get(f"{settings.FLASK_API_URL}/stories?status=published")
        stories = response.json()
    except requests.RequestException:
        stories = []

    stats_data = []

    for story in stories:
        s_id = story['id']
        
        total_plays = Play.objects.filter(story_id=s_id).count()
        
        if total_plays > 0:
            ending_counts = Play.objects.filter(story_id=s_id).values('ending_page_id').annotate(count=Count('ending_page_id'))
            
            detailed_endings = []
            for ec in ending_counts:
                page_id = ec['ending_page_id']
                count = ec['count']
                percentage = int((count / total_plays) * 100)
                
                try:
                    p_res = requests.get(f"{settings.FLASK_API_URL}/pages/{page_id}")
                    if p_res.status_code == 200:
                        label = p_res.json().get('ending_label') or f"Page #{page_id}"
                    else:
                        label = f"Unknown Page {page_id}"
                except:
                    label = "API Error"

                detailed_endings.append({
                    'label': label,
                    'count': count,
                    'percentage': percentage
                })
            
            stats_data.append({
                'title': story['title'],
                'total_plays': total_plays,
                'endings': detailed_endings
            })

    return render(request, 'game/stats.html', {'stats_data': stats_data})