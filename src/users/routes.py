from flask import Blueprint, render_template, flash, redirect, url_for, request
from src import db, bcrypt
from src.models import UserModel
from src.forms import RegisterForm, LoginFrom, UpdateForm
from flask_login import current_user, logout_user, login_user,login_required


users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
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
        name = form.name.data
        surname = form.surname.data
        hash_password = bcrypt.generate_password_hash(password)
        user = UserModel(name=name, surname=surname, email=email, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {name} Thank you for registering', 'success')

        return redirect(url_for('users_bp.login'))
    return render_template('auth/register.html', form=form, title="Register")


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.admin:
        flash('You are already logged in.', 'info')
        return redirect(url_for('admin_bp.admin_page'))

    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('blog_bp.home_page'))

    form = LoginFrom()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            user = current_user
            user.log = user.log+1
            db.session.commit()

            flash('You are login now!', 'success')
            next_url = request.args.get('next')
            if current_user.admin:
                return redirect(next_url or url_for('admin_bp.admin_page'))
            return redirect(next_url or url_for('blog_bp.home_page'))
        flash('Incorrect email and password', 'danger')
        return redirect(url_for('users_bp.login'))

    return render_template('auth/login.html', form=form)


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blog_bp.home_page'))


@users_bp.route('/profile')
@login_required
def profile():
    return render_template('pages/profile.html')


@users_bp.route("/edit-user/<int:user_id>", methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = UserModel.query.get_or_404(user_id)
    if user:
        form = UpdateForm(
            name=user.name,
            surname=user.surname,
            email=user.email
        )
        if request.method == "POST":
            user.name = form.name.data
            user.surname = form.surname.data
            user.email = form.email.data
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            return redirect(url_for('users_bp.profile'))
        return render_template('auth/register.html', form=form, title="Update Profile")
    else:
        return redirect(url_for('users_bp.profile'))
