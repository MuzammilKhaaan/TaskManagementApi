from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    tasks = db.relationship('Task', back_populates= 'user')


    def __init__(self, username, password="password"):
        self.username = username
        self.password = self.hash_password(password=password)

    def __repr__(self):
        return f"User(username={self.username})"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
        }
    def hash_password(self, password):
        return generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    urgency = db.Column(db.String(10))
    user = db.relationship('User', back_populates='tasks')

    def __init__(self, user_id ,title, description = '', urgency = ''):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.urgency = urgency
        self.done = False

    def to_dict(self):
        return {
            "id": self.id,
            "urgency": self.urgency,
            "description": self.description,
            "title": self.title,
            "done": self.done 
        }
