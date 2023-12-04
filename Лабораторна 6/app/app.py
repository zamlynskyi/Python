from flask import Flask, make_response, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
import json
import os
from datetime import datetime, timedelta
from forms import LoginForm, ChangePasswordForm

app = Flask(__name__)
app.secret_key = b"secret"
app.permanent_session_lifetime = timedelta(days=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

my_skills = [
    "Python",
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
    "Git",
    "C++",
    "PHP",
]

with open('data.json', 'r') as f:
    users = json.load(f)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_item = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    status = db.Column(db.Boolean, default=False)


class TodoForm(FlaskForm):
    todo_item = StringField('Назва завдання', validators=[DataRequired()])
    status = BooleanField('Статус')
    description = StringField('Опис')
    submit = SubmitField('Зберегти')


@app.route('/')
def home():
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('portfolio.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/portfolio')
def portfolio():
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('portfolio.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/skills')
@app.route('/skills/<int:id>')
def skills(id=None):
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if id is None:
        total_skills = len(my_skills)
        return render_template('skills.html', skills=my_skills, total_skills=total_skills, os_info=os_info,
                               user_agent=user_agent, current_time=current_time)
    elif id < len(my_skills):
        return render_template('skill.html', skills=my_skills[id], id=id + 1, os_info=os_info, user_agent=user_agent,
                               current_time=current_time)
    else:
        return "Немає навички з таким id"


@app.route('/resume')
def resume():
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('resume.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/contacts')
def contacts():
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('contacts.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in users and users[username] == password:
            session['username'] = username

            if not form.remember.data:
                return redirect(url_for('home'))

            if form.remember.data:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)

            flash('Ви успішно увійшли', 'success')
            return redirect(url_for('info'))

        flash('Невірне ім\'я користувача або пароль', 'danger')

    flash('Необхідно увійти для доступу', 'warning')
    return render_template('login.html', form=form)


@app.route("/info", methods=['GET', 'POST'])
def info():
    if not session.get("username"):
        return redirect(url_for('login'))

    username = session.get("username")
    cookies = request.cookies
    return render_template("info.html", username=username, cookies=cookies)


@app.route('/setCookie', methods=["POST"])
def setCookie():
    key = request.form.get("key")
    value = request.form.get("value")
    days = request.form.get("days")
    response = make_response(redirect(url_for('info')))
    response.set_cookie(key, value, max_age=60 * 60 * 24 * int(days))
    flash('Cookie був доданий', 'success')
    return response


@app.route("/deleteCookieByKey", methods=["POST"])
def deleteCookieByKey():
    key = request.form.get("key")
    response = make_response(redirect(url_for('info')))
    response.delete_cookie(key)
    flash('Cookie був видалений', 'success')
    return response


@app.route("/deleteCookieAll", methods=["POST"])
def deleteCookieAll():
    cookiesKeys = request.cookies
    response = make_response(redirect(url_for('info')))

    for key, value in cookiesKeys.items():
        if key != "session":
            response.delete_cookie(key)
    flash('Cookie був видалений', 'success')
    return response


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if 'username' in session:
            new_passwords = form.new_passwords.data

            if new_passwords:
                username = session['username']
                users[username] = new_passwords

                flash("Пароль успішно змінено", "success")
                return redirect(url_for('login'))

    return render_template('change_password.html', form=form)


def get_navigation_items():
    navigation_items = [
        {'url': '/portfolio', 'label': 'Головна'},
        {'url': '/skills', 'label': 'Скіли'},
        {'url': '/resume', 'label': 'Резюме'},
        {'url': '/contacts', 'label': 'Контакти'},
        {'url': '/login', 'label': 'Логін'},
        {'url': '/todo', 'label': 'Todo'},
    ]
    return navigation_items


@app.context_processor
def inject_navigation():
    return dict(navigation_items=get_navigation_items())


@app.route('/todo', methods=['GET', 'POST'])
def todo():
    todos = Todo.query.all()
    form = TodoForm()

    if form.validate_on_submit():
        new_todo = Todo(todo_item=form.todo_item.data, status=form.status.data, description=form.description.data)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo додано', 'success')
        return redirect(url_for('todo'))

    return render_template('todo.html', todos=todos, form=form)


@app.route('/todo/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    todo = Todo.query.get_or_404(id)
    form = TodoForm(obj=todo)

    if form.validate_on_submit():
        todo.todo_item = form.todo_item.data
        todo.status = form.status.data
        todo.description = form.description.data
        db.session.commit()
        flash('Todo оновлено', 'success')
        return redirect(url_for('todo'))

    return render_template('edit_todo.html', form=form, todo=todo)


@app.route('/todo/delete/<int:id>', methods=['POST'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo видалено', 'success')
    return redirect(url_for('todo'))


if __name__ == '__main__':
    app.run(debug=True)
