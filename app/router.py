import datetime
from datetime import timedelta
from flask import request, jsonify, redirect
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import app, jwt, user_space, task_space, db
from models import User, Task
from flask_restx import Resource
# from flask import current_app as app
from waitress import serve

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify(code="invalid_token", err="The access token provided is invalid"), 401


@user_space.route("/register")
class Register(Resource):
    @user_space.doc(
        summary="Register",
        description="This endpoint allows you to register a new user.",
        params={
            'body': {
                'in': 'body',
                'description':
                    'Input your username and password. The id will be automatically generated. '
                    'The username will be used to login. The password is optional and will be set to "password" if not given ',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {
                            'type': 'string'
                        },
                        'password': {
                            'type': 'string'
                        }
                    },
                    'required': ['username', 'password']
                }}})
    def post(self):
        """Register a new user"""
        print("in register")
        data = request.get_json()
        user = User.query.filter_by(username=data["username"]).first()
        if user:
            return {"message": "username taken"}, 400
        user = User(
            username=data["username"],
            password=data["password"],
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "success", "user": user.to_dict()}, 200
    

@user_space.route("/login")
class Login(Resource):
    @user_space.doc(
        summary="Login",
        description="This endpoint returns a JWT token to be used for authentication. You may use the username and "
                    "password to login. JWT TOKEN will be valid for 1 hour",
        params={
            'body': {
                'in': 'body',
                'description':
                    'Input your id and password',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {
                            'type': 'string'
                        },
                        'password': {
                            'type': 'string'
                        }
                    },
                    'required': ['username', 'password']
                }}})
    def post(self):
        data = request.get_json()
        #     return {"access_token": access_token}, 200
        user = User.query.filter_by(username=data["username"]).first()
        if user and user.verify_password(data["password"]):
            payload = {
                "user_id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }
            access_token = create_access_token(identity=payload, expires_delta=timedelta(days=1), fresh=True)
            print(access_token)
            # access_token_str = access_token.decode('utf-8')
            return {"access_token": access_token}, 200
        

@task_space.route("/all")
class GetAllTasks(Resource):
    @task_space.header("Authorization", "JWT Token", required=True)
    @task_space.doc(
        summary="Get all Tasks",
        description="This endpoint allows you to get all Tasks.",
        params={
            'Authorization': {
                'in': 'header',
                'description':
                    'Bearer and JWT'
            }})
    @jwt_required()
    # @verify_jwt_in_request
    def get(self):
        """Get all tasks for a user"""
        print( get_jwt_identity())
        user_id = get_jwt_identity()['user_id']
        tasks = Task.query.filter_by(user_id=user_id).all()
        return jsonify([task.to_dict() for task in tasks])
@task_space.route("/add")
class AddTask(Resource):
    @task_space.header("Authorization", "JWT Token", required=True)
    @task_space.doc(
        summary="Add an task",
        description="This endpoint allows you to add a new task",
        params={
            'Authorization': {
                'in': 'header',
                'description':
                    'Bearer and JWT'
            },
            'body': {
                'in': 'body',
                'description':
                    'Input your description, title and urgency. Title can not be empty',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'description': {
                            'type': 'string'
                        },
                        'title': {
                            'type': 'string',
                            'maxLength': 40  
                        },
                        'urgency' : { 
                            'type': 'string',
                            'maxLength': 10  
                        }
                    },
                    'required': ['title']
                }}})
    @jwt_required()
    def post(self):
        """Create an task"""

        data = request.get_json()
        if not data["title"].strip():  # This checks if the title is an empty string or consists only of whitespace
            return {"message": "Title cannot be empty"}, 400
        user_id = get_jwt_identity()['user_id']
        task = Task(
            user_id=user_id,
            description=data["description"],
            title=data["title"],
            urgency= data["urgency"]
        )
        db.session.add(task)
        db.session.commit()
        return {"message": "success", "task": task.to_dict()}, 200
    

@task_space.route("/edit/<int:id>")
class UpdateTask(Resource):
    @task_space.header("Authorization", "JWT Token", required=True)
    @task_space.doc(
        summary="Edit any task",
        description="This endpoint allows you to edit a task.",
        params={
            'Authorization': {
                'in': 'header',
                'description':
                    'Add your JWT token by adding "Bearer " before your token'
            },
            'body': {
                'in': 'body',
                'description':
                    'Input any of the following prooperites you want to edit: title, urgency, done, description '
                    'required.',
                'schema': {
                    'type': 'object',
                    'required': ['title'],
                    'properties': {
                        'title': {
                            'type': 'string'
                        },
                        'description': {
                            'type': 'string'
                        },
                        'urgency': {
                            'type': 'string'
                        },'done': {
                            'type': 'boolean'
                        }
                    }}},
                "response": { 
                    200: {
                        'description': 'Success',
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'message': {
                                    'type': 'string',
                                    'example': 'success'
                                },
                                'task': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {
                                            'type': 'integer'
                                        },
                                        'title': {
                                            'type': 'string'
                                        },
                                        'description': {
                                            'type': 'string'
                                        },
                                        'urgency': {
                                            'type': 'string'
                                        },
                                        'done': {
                                            'type': 'boolean'
                                        }
                                    }
                                }
                            }
                        }
                    },
                    404: {
                        'description': 'Task not found',
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'message': {
                                    'type': 'string',
                                    'example': 'task not found'
                                }
                            }
                }}
        }}
        
    )
    @jwt_required()
    def put(self, id):
        user_id = get_jwt_identity()['user_id']
        task = Task.query.filter_by(id=id, user_id=user_id).first()
        if not task:
            return {"message": "task not found"}, 404
        data = request.get_json()
        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "urgency" in data:
            task.urgency = data["urgency"]
        if "done" in data:
            task.done = data["done"]
        db.session.commit()
        return {"message": "task successfully edited", "task": task.to_dict()}, 200
    
@task_space.route('/<int:id>')
class DeleteTask(Resource):
    @task_space.header("Authorization", "JWT Token", required=True)
    @task_space.doc(
        summary="Delete a task",
        description="This endpoint is to delete a task.",
        params={
            'Authorization': {
                'in': 'header',
                'description':
                        'Add your JWT token by adding "Bearer " before your token'
            }})
    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()['user_id']
        task = Task.query.filter_by(id=id, user_id=user_id).first()
        if not task:
            return {"message": "task not found"}, 404
        db.session.delete(task)
        db.session.commit()
        return {"message": "success"}, 200




if __name__ == "__main__":
    with app.app_context():
        print(app.url_map)
        try:
            # for table in db.metadata.tables.values():
            #     print(f"Table: {table.name}")
            #     for column in table.c:
            #         print(f"  Column: {column.name} - Type: {column.type}")
            db.create_all()
        except Exception as e:
            print(f"error creating users : ${e}")
    serve(app, host='0.0.0.0', port=5000)
    # app.run(host='0.0.0.0')