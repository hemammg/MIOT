from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Association table for Role and Permission
role_permission = db.Table('role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    permissions = db.relationship('Permission', secondary=role_permission, lazy='subquery',
        backref=db.backref('roles', lazy=True))

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class User(db.Model, UserMixin):  # Include UserMixin for Flask-Login compatibility
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # New column to represent if a user is active
    role_id = db.Column(db.Integer, db.ForeignKey('role.id')) # link to Role model

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # The following methods are required for flask_login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Add more columns as needed
    # Define any additional methods or relationships here
