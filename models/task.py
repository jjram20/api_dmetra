from utils.db import db
from .user import User
from datetime import datetime

#Task model. Table definition
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), unique=False)
    description = db.Column(db.String(1000), unique=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    #Method included to get info using dictionary format
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    #Constructor to save a new record
    def __init__(self, user_id, title, description):
        self.user_id = user_id
        self.title = title
        self.description = description
