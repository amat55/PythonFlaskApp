from flask import render_template, Blueprint, request, redirect, url_for, flash
from src import bcrypt 
from src.models import db, BlogModel, UserModel
from .helpers import role_admin
from src.forms import RegisterForm
from flask_login import current_user

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if current_user.is_authenticated and current_user.admin:
        flash('You are already logged in.', 'info')
        return redirect(url_for('admin_bp.admin_page'))

    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('blog_bp.home_page'))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        username = form.name.data
        surname = form.surname.data
        hash_password = bcrypt.generate_password_hash(password)
        user = UserModel(name=username, surname=surname, email=email, password=hash_password, admin=True)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {username} Thank you for registering', 'success')

        return redirect(url_for('users_bp.login'))
    return render_template('auth/register.html', form=form)


@admin_bp.route('/admin', methods=['GET', 'POST'])
@role_admin
def admin_page():
    blogs = BlogModel.query.order_by(BlogModel.created_at.desc()).all()
    if request.method == "POST":
        blog_id = request.form.get('blog_id')
        private = request.form.get('private')
        blog = BlogModel.query.get_or_404(blog_id)
        if blog:
            blog.private = int(private)
            db.session.commit()
    return render_template('admin/all-blogs.html', blogs=blogs)


@admin_bp.route('/admin-users', methods=['GET', 'POST'])
@role_admin
def admin_users():
    all_users = UserModel.query.order_by(UserModel.created_at.desc()).all()
    if request.method == "POST":
        user_id = request.form.get('user_id')
        admin = request.form.get('admin')
        user = UserModel.query.get_or_404(user_id)
        if user:
            user.admin = int(admin)
            db.session.commit()
    return render_template('admin/all-users.html', users=all_users)


@admin_bp.route("/delete-user/<int:user_id>")
@role_admin
def delete_user(user_id):
    user_to_delete = UserModel.query.get_or_404(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
    return redirect(url_for("admin_bp.admin_users"))

