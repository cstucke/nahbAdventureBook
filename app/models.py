from . import db
from datetime import datetime, timezone

class Story(db.Model):
    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='draft') 
    
    start_page_id = db.Column(
        db.Integer, 
        db.ForeignKey('pages.id', use_alter=True, name='fk_story_start_page'), 
        nullable=True
    )
    
    illustration_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    pages = db.relationship('Page', backref='story', lazy=True, foreign_keys='Page.story_id', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'start_page_id': self.start_page_id,
            'illustration_url': self.illustration_url
        }

class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_ending = db.Column(db.Boolean, default=False)
    ending_label = db.Column(db.String(100), nullable=True)
    illustration_url = db.Column(db.String(255), nullable=True)

    choices = db.relationship(
        'Choice', 
        foreign_keys='Choice.page_id', 
        backref='page', 
        lazy=True, 
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            'id': self.id,
            'story_id': self.story_id,
            'text': self.text,
            'is_ending': self.is_ending,
            'ending_label': self.ending_label,
            'illustration_url': self.illustration_url,
            'choices': [c.to_dict() for c in self.choices] 
        }

class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    next_page_id = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'next_page_id': self.next_page_id
        }