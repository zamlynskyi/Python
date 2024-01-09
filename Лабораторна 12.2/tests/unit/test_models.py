from app.auth.models import User
from app.post.models import Post
from app.todo.models import Todo
from app import db


def test_user_model():

    user = User(username="user", email="user@gmail.com", password="password")
    assert user.username == 'user'
    assert user.email == 'user@gmail.com'
    assert user.password == 'password'


def test_todo_model():

    todo = Todo(todo_item="todo title", description="this is todo description")
    assert todo.todo_item == "todo title"
    assert todo.description == "this is todo description"


def test_post_model():

    post = Post(title='Post_test', text='Text post test')
    assert post.title == 'Post_test'
    assert post.text == 'Text post test'
