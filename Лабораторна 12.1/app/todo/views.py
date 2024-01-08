from flask import flash, redirect, render_template, url_for
from . import todo
from .forms import TodoForm
from .models import Todo
from .. import db, navigation


@todo.context_processor
def inject_navigation():
    return dict(navigation=navigation())


@todo.route('/todo', methods=['GET'])
def todos():
    todos = Todo.query.all()
    return render_template('todo.html', todos=todos)


@todo.route('/todo/create', methods=['GET', 'POST'])
def create_todo():
    form = TodoForm()

    if form.validate_on_submit():
        new_todo = Todo(
            todo_item=form.todo_item.data,
            status=form.status.data,
            description=form.description.data
        )
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo додано', 'success')
        return redirect(url_for('todo.todos'))

    return render_template('create_todo.html', form=form)


@todo.route('/todo/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    todo = Todo.query.get_or_404(id)
    form = TodoForm(obj=todo)

    if form.validate_on_submit():
        todo.todo_item = form.todo_item.data
        todo.status = form.status.data
        todo.description = form.description.data
        db.session.commit()
        flash('Todo оновлено', 'success')
        return redirect(url_for('todo.todos'))

    return render_template('edit_todo.html', form=form, todo=todo)


@todo.route('/todo/delete/<int:id>')
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo видалено', 'success')
    return redirect(url_for('todo.todos'))
