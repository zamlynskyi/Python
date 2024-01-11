from flask import jsonify, request
from app.todo.models import Todo
from app.auth.models import User
from app.friends.models import Friend
from datetime import datetime, timedelta
from app import db, basic_auth
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required
from config import Config
from . import api_bp
from .. import db
import jwt


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return True
    return False


# Login API

@api_bp.route('/login')
def login():
    auth = request.authorization

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('No such user in database', 401,
                             {'WWW-Authenticate': 'Bearer realm="Authentication Required"'})

    if user.password == auth.password:
        expiry = datetime.utcnow() + timedelta(minutes=30)
        subject = "access"
        secret_key = Config.SECRET_KEY

        token = jwt.encode(
            {"sub": subject, "username": user.username, "exp": expiry},
            secret_key,
            algorithm="HS256"
        )

        return jsonify({"token": token})

    return make_response('Invalid username or password', 401,
                         {'WWW-Authenticate': 'Bearer realm="Authentication Required"'})


# Todo API

@api_bp.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    todos = Todo.query.all()
    todos_list = []
    for todo in todos:
        todos_list.append({
            'id': todo.id,
            'todo_item': todo.todo_item,
            'status': todo.status,
            'description': todo.description
        })
    return jsonify({'todos': todos_list})


@api_bp.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    data = request.json
    new_todo = Todo(
        todo_item=data.get('todo_item'),
        status=data.get('status', False),
        description=data.get('description')
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully'}), 201


@api_bp.route('/todos/<int:id>', methods=['GET'])
@jwt_required()
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return jsonify({
        'id': todo.id,
        'todo_item': todo.todo_item,
        'status': todo.status,
        'description': todo.description
    })


@api_bp.route('/todos/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.json
    todo.todo_item = data.get('todo_item', todo.todo_item)
    todo.status = data.get('status', todo.status)
    todo.description = data.get('description', todo.description)
    db.session.commit()
    return jsonify({'message': 'Todo updated successfully'}), 200


@api_bp.route('/todos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'}), 200


# Friends API

@api_bp.route('/friends', methods=['GET'])
@jwt_required()
def get_friends():
    friends = Friend.query.all()
    friends_list = [{
        'id': friend.id,
        'name': friend.name,
        'age': friend.age,
        'email': friend.email
    } for friend in friends]
    return jsonify({'friends': friends_list})


@api_bp.route('/friends/<int:id>', methods=['GET'])
@jwt_required()
def get_friend(id):
    friend = Friend.query.get_or_404(id)
    return jsonify({
        'id': friend.id,
        'name': friend.name,
        'age': friend.age,
        'email': friend.email
    })


@api_bp.route('/friends', methods=['POST'])
@jwt_required()
def create_friend():
    data = request.json
    new_friend = Friend(
        name=data['name'],
        age=data['age'],
        email=data['email']
    )
    db.session.add(new_friend)
    db.session.commit()
    return jsonify({'message': 'Friend created successfully'}), 201


@api_bp.route('/friends/<int:id>', methods=['PUT'])
@jwt_required()
def update_friend(id):
    friend = Friend.query.get_or_404(id)
    data = request.json
    friend.name = data.get('name', friend.name)
    friend.age = data.get('age', friend.age)
    friend.email = data.get('email', friend.email)
    db.session.commit()
    return jsonify({'message': 'Friend updated successfully'}), 200


@api_bp.route('/friends/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_friend(id):
    friend = Friend.query.get_or_404(id)
    db.session.delete(friend)
    db.session.commit()
    return jsonify({'message': 'Friend deleted successfully'}), 200
