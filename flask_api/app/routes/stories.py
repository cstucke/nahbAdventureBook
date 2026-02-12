from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import Story, Page
from sqlalchemy import func

stories_bp = Blueprint('stories', __name__, url_prefix='/stories')

# GET /stories?status=published
@stories_bp.route('', methods=['GET'])
def get_stories():
    status_filter = request.args.get('status')
    search_query = request.args.get('q')

    query = Story.query

    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if search_query:
        lower_query = search_query.lower()
        query = query.filter(
            (func.lower(Story.title).contains(lower_query)) | (func.lower(Story.description).contains(lower_query))
        )

    stories = query.all()

    return jsonify([s.to_dict() for s in stories])

# GET /stories/<id>
@stories_bp.route('/<int:story_id>', methods=['GET'])
def get_story(story_id):
    story = Story.query.get_or_404(story_id)
    return jsonify(story.to_dict())

# GET /stories/<id>/start
@stories_bp.route('/<int:story_id>/start', methods=['GET'])
def start_story(story_id):
    story = Story.query.get_or_404(story_id)
    if not story.start_page_id:
        return jsonify({'error': 'Story has no start page'}), 404
    start_page = Page.query.get(story.start_page_id)
    return jsonify(start_page.to_dict())

# POST /stories
@stories_bp.route('', methods=['POST'])
def create_story():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
        
    new_story = Story(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'draft')
    )
    db.session.add(new_story)
    db.session.commit()
    return jsonify(new_story.to_dict()), 201

# PUT /stories/<id>
@stories_bp.route('/<int:story_id>', methods=['PUT'])
def update_story(story_id):
    story = Story.query.get_or_404(story_id)
    data = request.get_json()
    
    if 'title' in data:
        story.title = data['title']
    if 'description' in data:
        story.description = data['description']
    if 'status' in data:
        story.status = data['status']
    if 'start_page_id' in data:
        story.start_page_id = data['start_page_id']
        
    db.session.commit()
    return jsonify(story.to_dict())

# DELETE /stories/<id>
@stories_bp.route('/<int:story_id>', methods=['DELETE'])
def delete_story(story_id):
    story = Story.query.get_or_404(story_id)
    db.session.delete(story)
    db.session.commit()
    return jsonify({'message': 'Story deleted'})

# POST /stories/<id>/pages
@stories_bp.route('/<int:story_id>/pages', methods=['POST'])
def create_page_for_story(story_id):
    story = Story.query.get_or_404(story_id)
    data = request.get_json()
    
    if 'text' not in data:
        return jsonify({'error': 'Text is required'}), 400
        
    new_page = Page(
        story_id=story.id,
        text=data['text'],
        is_ending=data.get('is_ending', False),
        ending_label=data.get('ending_label', None)
    )
    db.session.add(new_page)
    db.session.commit()
    return jsonify(new_page.to_dict()), 201