from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_principal import Principal, Permission, RoleNeed

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miot.db'

db = SQLAlchemy(app)

# Flask-Login Configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Flask-Principal Configuration
principal = Principal(app)
website_master_permission = Permission(RoleNeed('master'))
administrator_permission = Permission(RoleNeed('admin'))
practitioner_permission = Permission(RoleNeed('practitioner'))
patient_permission = Permission(RoleNeed('patient'))

migrate = Migrate(app, db)

from app.models import User  # Assuming User is in your models.py

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes  # Import routes at the end
app.config.from_object('config')
