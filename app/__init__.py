from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app.data import staff_categories, semester_data, staff_titles
from flask_login import LoginManager
import os
from flask_bootstrap import Bootstrap5
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate

db = SQLAlchemy()  # Define db at the top
load_dotenv()

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'



def create_admin():
    from app.models import Department, User, Title, Category  # Fixed import from 'models' to 'app.models'
    surname = os.getenv('ADMIN_SURNAME')
    first_name = os.getenv('ADMIN_FIRSTNAME')
    email = os.getenv('ADMIN_EMAIL')
    phone = os.getenv('ADMIN_PHONE')
    department = os.getenv('ADMIN_DEPARTMENT')
    title = "Mr."
    category = "Senior Member (Administrative)"

    if not Department.query.filter_by(name=department).first():
        db.session.add(Department(name=department))
        db.session.commit()

    if not User.query.filter_by(surname=surname, first_name=first_name).first():
        title_id = Title.query.filter_by(title=title).first().id
        category_id = Category.query.filter_by(name=category).first().id
        dept_id = Department.query.filter_by(name=department).first().id
        if dept_id:
            db.session.add(
                User(
                    title_id=title_id,
                    surname=surname,
                    first_name=first_name,
                    email=email,
                    phone=phone,
                    category_id=category_id,
                    department_id=dept_id,
                    is_admin=True,
                    password=generate_password_hash(os.getenv('ADMIN_PASSWORD'), method='scrypt', salt_length=8)
                )
            )
            db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLITE_DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True

    db.init_app(app)  # Initialize db with the app
    login_manager.init_app(app)
    Bootstrap5(app)
    migrate = Migrate(app, db)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    from app.models import User

    def attribute(obj, attr):
        return getattr(obj, attr)

    app.jinja_env.filters['attribute'] = attribute


    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()  # Create tables

    return app