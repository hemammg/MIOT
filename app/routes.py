from flask import flash, render_template, redirect, url_for, request, session
from app import app, db
from app.forms.auth_forms import RegistrationForm, LoginForm
from app.models import User, Device, Role
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_principal import (
    Identity, identity_changed, RoleNeed, Permission, 
    PermissionDenied, identity_loaded
)

# Initialize bcrypt
bcrypt = Bcrypt(app)

# Define permissions
admin_need = RoleNeed('admin')
administrator_permission = Permission(admin_need)


# ======================== CONTEXT PROCESSORS ========================

@app.context_processor
def context_processor():
    return dict(administrator_permission=administrator_permission)


# ======================== MAIN ROUTES ========================

@app.route('/')
def index():
    return "Welcome to the MIOT Platform!"


# ======================== AUTHENTICATION ROUTES ========================

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # This method will hash and set the password for the user
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):  # Using the check_password method
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check email and password.', 'danger')
    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


# ======================== USER ROUTES ========================

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/device/<int:device_id>')
def device(device_id):
    return render_template('device.html', device_id=device_id)


# ======================== ADMIN ROUTES ========================

@app.route('/admin_dashboard')
@administrator_permission.require(http_exception=403)
def admin_dashboard():
    return "Welcome to Admin Dashboard"


# ======================== PERMISSIONS AND ROLES ========================

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    for role in current_user.roles:
        identity.provides.add(RoleNeed(role.name))


@app.errorhandler(PermissionDenied)
def permission_denied_error(error):
    return "You do not have permission to view this content.", 403
