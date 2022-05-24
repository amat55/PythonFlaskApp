from flask import Blueprint, render_template, redirect, url_for, request, current_app
from src import db
from src.models import BlogModel,UserModel
from src.forms import BlogForm
from flask_login import login_required, current_user
import os
import secrets

blog_bp = Blueprint('blog_bp', __name__)


@blog_bp.route('/')
def home_page():
    all_blogs = BlogModel.query.order_by(BlogModel.created_at.desc()).all()
    top_user = UserModel.query.order_by(UserModel.log.desc()).filter_by(admin=False).all()
    if len(top_user) > 3:
        top_user = top_user[:3]
    print(top_user)
    return render_template('pages/home.html', blogs=all_blogs, top_user=top_user)


@blog_bp.route('/create-blog', methods=["GET", "POST"])
@login_required
def create_blog():
    form = BlogForm()
    if request.method == "POST" and 'img_url' in request.files:
        img_url = request.files.get('img_url')
        audio_url = request.files.get('audio_url')
        video_url = request.files.get('video_url')
        img_filename = None
        audio_filename = None
        video_filename = None
        if img_url:
            print(img_url.filename)
            f_name = str(secrets.token_hex(10))
            extension = os.path.splitext(img_url.filename)[1]
            img_filename = f_name + extension
            img_url.save(os.path.join(current_app.root_path, 'static/img/' + img_filename))
        if audio_url:
            f_name = str(secrets.token_hex(10))
            extension = os.path.splitext(audio_url.filename)[1]
            audio_filename = f_name + extension
            audio_url.save(os.path.join(current_app.root_path, 'static/audio/' + audio_filename))

        if video_url:
            f_name = str(secrets.token_hex(10))
            extension = os.path.splitext(video_url.filename)[1]
            video_filename = f_name + extension
            video_url.save(os.path.join(current_app.root_path, 'static/video/' + video_filename))
        if not img_filename:
            img_filename = "default.png"
        new_blog = BlogModel(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            image=img_filename,
            audio=audio_filename,
            video=video_filename,
            user=current_user
        )
        db.session.add(new_blog)
        db.session.commit()
        if current_user.admin:
            return redirect(url_for("admin_bp.admin_page"))
        return redirect(url_for("blog_bp.home_page"))
    return render_template("blogs/blog-form.html", form=form, title="Create Blog")


@blog_bp.route("/blog/<int:blog_id>", methods=['GET', 'POST'])
def view_blog(blog_id):
    blog = BlogModel.query.get_or_404(blog_id)
    return render_template("blogs/single-blog.html", blog=blog)


@blog_bp.route("/edit-blog/<int:blog_id>", methods=['GET', 'POST'])
@login_required
def edit_blog(blog_id):
    blog = BlogModel.query.get_or_404(blog_id)
    if blog:
        if current_user.id == blog.user.id or current_user.admin == True:
            form = BlogForm(
                title=blog.title,
                subtitle=blog.subtitle,
                user=current_user,
                body=blog.body
            )
            if request.method == "POST":
                blog.title = form.title.data
                blog.subtitle = form.subtitle.data
                blog.body = form.body.data
                img_url = request.files.get('img_url')
                audio_url = request.files.get('audio_url')
                video_url = request.files.get('video_url')
                if img_url:
                    try:
                        os.unlink(os.path.join(current_app.root_path, "static/img/" + blog.image))
                        f_name = str(secrets.token_hex(10))
                        extension = os.path.splitext(img_url.filename)[1]
                        filename = f_name + extension
                        img_url.save(os.path.join(current_app.root_path, 'static/img/' + filename))
                        blog.image = filename
                    except Exception:
                        f_name = str(secrets.token_hex(10))
                        extension = os.path.splitext(img_url.filename)[1]
                        filename = f_name + extension
                        img_url.save(os.path.join(current_app.root_path, 'static/img/' + filename))
                        blog.image = filename

                if audio_url:
                    try:
                        os.unlink(os.path.join(current_app.root_path, "static/audio/" + blog.audio))
                        f_name = str(secrets.token_hex(10))
                        extension = os.path.splitext(audio_url.filename)[1]
                        filename = f_name + extension
                        audio_url.save(os.path.join(current_app.root_path, 'static/audio/' + filename))
                        blog.audio = filename
                    except Exception:
                        f_name = str(secrets.token_hex(10))
                        extension = os.path.splitext(audio_url.filename)[1]
                        filename = f_name + extension
                        audio_url.save(os.path.join(current_app.root_path, 'static/audio/' + filename))
                        blog.audio = filename

                if video_url:
                    try:
                        os.unlink(os.path.join(current_app.root_path, "static/video/" + blog.video))
                        f_name = str(secrets.token_hex(10))
                        extension = os.path.splitext(video_url.filename)[1]
                        filename = f_name + extension
                        video_url.save(os.path.join(current_app.root_path, 'static/video/' + filename))
                        blog.video = filename
                    except Exception:
                        f_name = str(secrets.token_hex(10))
                        extension = os.path.splitext(video_url.filename)[1]
                        filename = f_name + extension
                        video_url.save(os.path.join(current_app.root_path, 'static/video/' + filename))
                        blog.video = filename

                db.session.commit()
                if current_user.admin:
                    return redirect(url_for("admin_bp.admin_page"))
                return redirect(url_for("blog_bp.view_blog", blog_id=blog.id))

            return render_template("blogs/blog-form.html", form=form, title="Update Blog", blog=blog)
        else:
            return redirect(url_for("blog_bp.view_blog", blog_id=blog.id))
    else:
        return redirect(url_for("blog_bp.view_blog", blog_id=blog.id))


@blog_bp.route("/delete-blog/<int:blog_id>")
@login_required
def delete_blog(blog_id):
    blog_to_delete = BlogModel.query.get_or_404(blog_id)
    if blog_to_delete:
        if current_user.id == blog_to_delete.user.id or current_user.admin_bp == True:
            try:
                os.unlink(os.path.join(current_app.root_path, "static/img/" + blog_to_delete.image))
                os.unlink(os.path.join(current_app.root_path, "static/audio/" + blog_to_delete.audio))
                os.unlink(os.path.join(current_app.root_path, "static/video/" + blog_to_delete.video))
            except Exception as e:
                print(e)
            db.session.delete(blog_to_delete)
            db.session.commit()
            if current_user.admin:
                return redirect(url_for("admin_bp.admin_page"))
            return redirect(url_for('blog_bp.home_page'))
        else:
            return redirect(url_for("blog_bp.view_blog", blog_id=blog_to_delete.id))
    else:
        return redirect(url_for('blog_bp.home_page'))
