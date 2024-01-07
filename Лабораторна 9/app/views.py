from collections import UserString
from os.path import dirname, join, realpath
from flask import request, render_template, redirect, url_for, make_response, session, flash, current_app
from datetime import datetime, timedelta
from .forms import LoginForm, ChangePasswordForm, TodoForm, FeedbackForm, RegistrationForm, UpdateAccountForm
from .models import Todo, Feedback, User
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from app import app, db
from PIL import Image
import secrets
import json
import os

dataJsonPath = join(dirname(realpath(__file__)), 'users.json')

with open(dataJsonPath, 'r') as f:
    users = json.load(f)

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Ваш обліковий запис створено! Тепер ви можете увійти в систему", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            flash('Вхід успішний!', 'success')
            return redirect(url_for('account'))

        flash("Вхід невдалий. Будь ласка, перевірте своє ім'я користувача та пароль.", 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вихід успішний!', 'success')
    return redirect(url_for('home'))


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


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        feedback_entry = Feedback(name=name, email=email, message=message)
        db.session.add(feedback_entry)
        db.session.commit()

        flash('Ваш відгук був збережений', 'success')
        return redirect(url_for('feedback'))

    feedbacks = Feedback.query.all()

    return render_template('feedback.html', form=form, feedbacks=feedbacks)


@app.route('/users')
def users():
    all_users = User.query.all()
    total_users = len(all_users)
    return render_template('users.html', users=all_users, total_users=total_users)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        db.session.commit()
        flash('Ваш обліковий запис оновлено!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    return render_template('account.html', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)

    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    form_picture.save(picture_path)
    return picture_fn


@app.after_request
def after_request(response):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Помилка під час оновлення!', 'danger')
    return response
