from flask import Blueprint, jsonify, request
from app import db
from app.models import Page, Choice
from app.utils import require_api_key

pages_bp = Blueprint('pages', __name__, url_prefix='/pages')

# GET /pages/<id>
@pages_bp.route('/<int:page_id>', methods=['GET'])
def get_page(page_id):
    page = Page.query.get_or_404(page_id)
    return jsonify(page.to_dict())

# POST /pages/<id>/choices
@pages_bp.route('/<int:page_id>/choices', methods=['POST'])
@require_api_key
def add_choice(page_id):
    page = Page.query.get_or_404(page_id)
    data = request.get_json()
    
    if 'text' not in data:
        return jsonify({'error': 'Choice text is required'}), 400
        
    new_choice = Choice(
        page_id=page.id,
        text=data['text'],
        next_page_id=data.get('next_page_id')
    )
    db.session.add(new_choice)
    db.session.commit()
    return jsonify(new_choice.to_dict()), 201

# PUT /pages/<id> (Update Page Text/Ending)
@pages_bp.route('/<int:page_id>', methods=['PUT'])
@require_api_key
def update_page(page_id):
    page = Page.query.get_or_404(page_id)
    data = request.get_json()
    
    if 'text' in data:
        page.text = data['text']
    if 'is_ending' in data:
        page.is_ending = data['is_ending']
    if 'ending_label' in data:
        page.ending_label = data['ending_label']
        
    db.session.commit()
    return jsonify(page.to_dict())

# DELETE /pages/<id> (Delete Page)
@pages_bp.route('/<int:page_id>', methods=['DELETE'])
@require_api_key
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    return jsonify({'message': 'Page deleted'})

# DELETE /choices/<id> (Delete a Choice)
# (We can add this here even though it's technically a choice resource)
@pages_bp.route('/choices/<int:choice_id>', methods=['DELETE'])
@require_api_key
def delete_choice(choice_id):
    choice = Choice.query.get_or_404(choice_id)
    db.session.delete(choice)
    db.session.commit()
    return jsonify({'message': 'Choice deleted'})