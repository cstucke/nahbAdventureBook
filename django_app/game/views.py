from django.shortcuts import render, redirect
import requests
from django.conf import settings
from .models import Play
from django.db.models import Count

# Create your views here.
def story_list(request):
    try:
        response = requests.get(f"{settings.FLASK_API_URL}/stories?status=published")
        stories = response.json()
    except requests.RequestException:
        stories = []

    return render(request, 'game/story_list.html', {'stories': stories})

def play_story(request, story_id):
    page_id = request.GET.get('page')

    if not page_id:
        story_res = requests.get(f"{settings.FLASK_API_URL}/stories/{story_id}")
        if story_res.status_code != 200:
            return render(request, 'game/error.html', {'message': "Story not found"})
        
        story_data = story_res.json()
        start_page_id = story_data.get('start_page_id')
        
        if not start_page_id:
             return render(request, 'game/error.html', {'message': "Story has no start page"})
             
        return redirect(f"/play/{story_id}?page={start_page_id}")

    page_res = requests.get(f"{settings.FLASK_API_URL}/pages/{page_id}")
    if page_res.status_code != 200:
        return render(request, 'game/error.html', {'message': "Page not found"})

    page_data = page_res.json()

    if page_data.get('is_ending'):
        Play.objects.create(
            story_id=story_id,
            ending_page_id=page_data['id']
        )
    
    return render(request, 'game/play.html', {
        'story_id': story_id,
        'page': page_data
    })

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