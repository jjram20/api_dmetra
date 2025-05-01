from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db import db
from models.task import Task
import json

tasks_bp = Blueprint('tasks', __name__)

#Route to create new task
@tasks_bp.post('/tasks')
#Verify user is authenticated
@jwt_required()
def tasks_post():
    try:
        current_user = get_jwt_identity()
        print(current_user)
        req = request.get_json(force=True)
        title = req['title']
        description = req['description']
        #Examine required information to continue exist
        if title and description:
            #Save new task
            new_task = Task(int(current_user), title, description)
            db.session.add(new_task)
            db.session.flush()
            db.session.commit()
            return Response(json.dumps({'message': 'Task saved'}), status=200, mimetype='application/json')
        else:
            return Response(json.dumps({'message': 'There is no enough data to process request'}), status=400, mimetype='application/json')
    #In case any unexpected error
    except Exception as error:
        print(error)
        return Response(json.dumps({'message': 'Error processing request'}), status=500, mimetype='application/json')

#Route to get list of tasks
@tasks_bp.get('/tasks')
#Verify user is authenticated
@jwt_required()
def tasks_get():
    try:
        #Get tasks related to authenticated user
        current_user = get_jwt_identity()
        tasks_user = Task.query.filter_by(user_id=current_user)
        tasks_list = [task.to_dict() for task in tasks_user]
        return Response(json.dumps({'message': 'Tasks retrieved sucessfully', 'tasks': tasks_list}), status=200, mimetype='application/json')
    #In case any unexpected error
    except Exception as error:
        print(error)
        return Response(json.dumps({'message': 'Error processing request'}), status=500, mimetype='application/json')

#Route to update completed status for any task
@tasks_bp.patch('/tasks/<id>')
#Verify user is authenticated
@jwt_required()
def tasks_patch(id):
    try:
        current_user = get_jwt_identity()
        #Get task to update
        task_to_edit = Task.query.filter_by(id=int(id)).first()
        if not task_to_edit:
            return Response(json.dumps({'message': 'Task does not exist'}), status=404, mimetype='application/json')
        #Verify user owns the task
        if task_to_edit.user_id == current_user:
            #Update completed status for task
            task_to_edit.completed = True
            db.session.flush()
            db.session.commit()
            return Response(json.dumps({'message': 'Task updated'}), status=200, mimetype='application/json')
        else:
            return Response(json.dumps({'message': 'There is no authorization to modify task'}), status=401, mimetype='application/json')
    #In case any unexpected error
    except Exception as error:
        print(error)
        return Response(json.dumps({'message': 'Error processing request'}), status=500, mimetype='application/json')