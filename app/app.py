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
               title='Task Management',
               description="This API provides user management and task t"
               "racking. It features user authentication using JWT ," 
               "and CRUD operations for tasks stored in a MySQL database")
user_space = rest_api.namespace('users', description="CRUD User")
task_space = rest_api.namespace('tasks', description="CRUD Task")
