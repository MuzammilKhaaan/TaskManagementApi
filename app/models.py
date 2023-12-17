from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

import app

db = app.db

db = SQLAlchemy(app.app)
class User(db.Model):
    __tablename__ = "Users"
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

    @staticmethod
    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    urgency = db.Column(db.String)
    user = db.relationship('User', back_populates='tasks')

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"task(user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity
        }
    
# with app.app.app_context():
#     print("creating users")
#     try:
#         db.create_all()
#     except:
#         print("Error creating USERS")