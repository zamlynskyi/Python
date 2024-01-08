from flask import Blueprint, jsonify, request
from app.todo.models import Todo
from app import db

api_todo = Blueprint('api_todo', __name__, url_prefix='/api/todos')


@api_todo.route('/', methods=['GET'])
def get_todos():
    todos = Todo.session.all()
    todos_list = []
    for todo in todos:
        todos_list.append({
            '№': todo.id,
            'Назва завдання': todo.todo_item,
            'Опис': todo.description,
            'Статус': todo.status
        })
    return jsonify({'todos': todos_list})


@api_todo.route('/', methods=['POST'])
def create_todo():
    data = request.json
    new_todo = Todo(
        todo_item=data.get('Назва завдання'),
        description=data.get('Опис'),
        status=data.get('Статус', False),
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo успішно створено'}), 201


@api_todo.route('/<int:id>', methods=['GET'])
def get_todo(id):
    todo = Todo.session.get_or_404(id)
    return jsonify({
        '№': todo.id,
        'Назва завдання': todo.todo_item,
        'Опис': todo.description,
        'Статус': todo.status
    })


@api_todo.route('/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.json
    todo.todo_item = data.get('Назва завдання', todo.todo_item)
    todo.description = data.get('Опис', todo.description)
    todo.status = data.get('Статус', todo.status)
    db.session.commit()
    return jsonify({'message': 'Todo успішно оновлено'}), 200


@api_todo.route('/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo успішно видалено'}), 200
