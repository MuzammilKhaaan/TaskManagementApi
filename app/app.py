from flask import Flask, request, url_for, session, Blueprint, Response, jsonify
# from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy

# from flask_httpauth import HTTPBasicAuth
import jwt
import os
import time

from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
from flask_restx import Api



 
app = Flask(__name__)
 


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@mysql/mydatabase'
app.config['JWT_SECRET_KEY'] = 'my_secret'


db = SQLAlchemy(app)
jwt = JWTManager(app)

# auth = HTTPBasicAuth()


rest_api = Api(app=app, version='1.0',
               title='Flask REST API with Flask-RESTX, Flask-SQLAlchemy, JWT Auth, and MySQL',
               description="add description")
user_space = rest_api.namespace('users', description="CRUD User")
task_space = rest_api.namespace('tasks', description="CRUD Task")

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(20), nullable=False)
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


    # def __repr__(self):
    #     return f"task(user_id={self.user_id})"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "urgency": self.urgency,
            "description": self.description,
            "title": self.title,
            "done": self.done 
        }
        
def get_user_id_from_token():
    token = request.headers.get("Authorization")
    if token:
        token = token.split(" ")[1]
        try:
            payload = jwt.decode(token, app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
            user_id = payload["sub"]["user_id"]
            return user_id
        except:
            return
    return

from router import *

if __name__ == "__main__":
    print("I am in main")
    with app.app_context():
        print(app.url_map)
        try:
            print("creating db")
            for table in db.metadata.tables.values():
                print(f"Table: {table.name}")
                for column in table.c:
                    print(f"  Column: {column.name} - Type: {column.type}")
            print("Creating db")
            print(db.metadata)
            db.create_all()
        except Exception as e:
            print(f"error creating users : ${e}")
    app.run(host='0.0.0.0', debug=True)