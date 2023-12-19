from flask import Flask
# from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api
app = Flask(__name__)    
import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)
 


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@mysql/mydatabase'
app.config['JWT_SECRET_KEY'] = 'my_secret'
app.config['PROPAGATE_EXCEPTIONS'] = True

db = SQLAlchemy(app)
jwt = JWTManager(app)
setattr(app, 'db', db)


rest_api = Api(app=app, version='1.0',
               title='Flask REST API with Flask-RESTX, Flask-SQLAlchemy, JWT Authentication, and MySQL',
               description="This API provides a robust platform for user management and task t"
               "racking. It features secure user authentication using JWT (JSON Web Tokens)," 
               "and CRUD operations for users and tasks stored in a MySQL database")
user_space = rest_api.namespace('users', description="CRUD User")
task_space = rest_api.namespace('tasks', description="CRUD Task")
