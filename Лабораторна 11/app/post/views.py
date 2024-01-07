import os
import secrets
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import post_bp
from .. import db, navigation
from .forms import PostForm
from .models import Post


@post_bp.context_processor
def inject_navigation():
    return dict(navigation=navigation())


@post_bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            text=form.text.data,
            type=form.type.data,
            enabled=form.enabled.data,
            user_id=current_user.id
        )

        if form.image.data:
            picture_file = save_picture(form.image.data)
            new_post.image = picture_file

        db.session.add(new_post)
        db.session.commit()
        flash('Публікація додана', 'success')
        return redirect(url_for('post_bp.posts'))

    return render_template('create_post.html', form=form)


@post_bp.route('/post', methods=['GET'])
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created.desc()).paginate(page=page, per_page=4)
    return render_template('posts.html', posts=posts)


@post_bp.route('/post/<int:id>', methods=['GET'])
def view_post(id):
    post = Post.query.get_or_404(id)
    return render_template('view_post.html', post=post)


@post_bp.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.type = form.type.data
        post.enabled = form.enabled.data

        if form.image.data:
            picture_file = save_picture(form.image.data)
            post.image = picture_file

        db.session.commit()
        flash('Публікація оновлена', 'success')
        return redirect(url_for('post_bp.view_post', id=post.id))

    return render_template('update_post.html', form=form, post=post)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(post_bp.root_path, '../static/images', picture_fn)

    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    form_picture.save(picture_path)
    return picture_fn


@post_bp.route('/post/<int:id>/delete', methods=['GET'])
@login_required
def confirm_delete_post(id):
    post = Post.query.get_or_404(id)
    return render_template('delete_post.html', post=post)


@post_bp.route('/post/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)

    if post.user_id != current_user.id:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Публікація видалена", "success")
    return redirect(url_for('post_bp.posts'))
