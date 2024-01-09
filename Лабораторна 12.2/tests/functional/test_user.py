from flask import url_for
from flask_login import current_user
from app.auth.models import User
from app import db


def test_register_user(client):
    response = client.post(
        url_for('auth.register'),
        data=dict(
            username='regTest',
            email='regTest@gmail.com',
            password='password',
            confirm_password='password'
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert u'Ваш обліковий запис створено' in response.data.decode('utf8')


def test_login_user(client):
    response = client.post(
        url_for('auth.login', external=True),
        data=dict(
            username='regTest',
            password='password'
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert u'Вхід успішний' in response.data.decode('utf8')


def test_log_out_user(client, log_in_default_user):
    response = client.get(
        url_for('auth.logout'),
        follow_redirects=True
    )

    assert u'Ви вийшли з системи' in response.data.decode('utf8')
    assert response.status_code == 200
    assert current_user.is_authenticated == False
