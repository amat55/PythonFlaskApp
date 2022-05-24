from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_bcrypt import Bcrypt
from src.models import db


bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    Bootstrap(app)
    db.init_app(app)
    bcrypt.init_app(app)
    moment = Moment()
    moment.init_app(app)
    login_manager.init_app(app)

    from src.users.routes import users_bp
    app.register_blueprint(users_bp, url_prefix="/")
    from src.blogs.routes import blog_bp
    app.register_blueprint(blog_bp, url_prefix="/")

    from src.errors.handlers import errors
    app.register_blueprint(errors, url_prefix="/")
    from src.admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/")

    from src.models import UserModel

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    @app.before_first_request
    def create_table():
        db.create_all()
        if not UserModel.query.filter_by(email='admin@email.com').first():
            hash_password = bcrypt.generate_password_hash('12345')
            admin = UserModel(name='admin', surname='admin', email='admin@email.com',
                              password=hash_password, admin=True)
            db.session.add(admin)
            db.session.commit()

    return app