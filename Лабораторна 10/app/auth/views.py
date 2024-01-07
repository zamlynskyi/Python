from datetime import datetime
from flask import render_template, redirect, session, url_for, flash, request, current_app
from flask_login import current_user, login_required, login_user, logout_user
from .forms import RegistrationForm, LoginForm, ChangePasswordForm, UpdateAccountForm
from collections import UserString
from . import auth
from .. import db
from .models import User
import secrets
import os


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Ваш обліковий запис створено! Тепер ви можете увійти в систему', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            flash('Вхід успішний!', 'success')
            return redirect(url_for('portfolio.home'))

        flash("Вхід невдалий. Будь ласка, перевірте своє ім'я користувача та пароль", 'danger')
    return render_template('login.html', title='Login', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('portfolio.home'))


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if 'username' in session:
            new_password = form.new_password.data

            if new_password:
                username = session['username']
                UserString[username] = new_password

                flash("Пароль успішно змінено", "success")
                return redirect(url_for('auth.login'))

    return render_template('change_password.html', form=form)


@auth.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.account'))

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


@auth.after_request
def after_request(response):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Помилка під час оновлення!', 'danger')
    return response
