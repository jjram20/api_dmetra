from utils.db import db

#User model. Table definition
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)

    #Method included to get info using dictionary format
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password
        }
    
    #Constructor to save a new record
    def __init__(self, email, password):
        self.email = email
        self.password = password