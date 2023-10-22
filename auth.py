from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_wtf import FlaskForm
from auth.form import RegistrationForm, LoginForm
from auth.models import User
from app import db 


auth_bp = Blueprint('auth', __name__)

# User loader function for Flask-Login
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Set the login view
login_manager.init_app(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes for user authentication
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful. You can now log in.", "success")
            return redirect('/login')
    return render_template("register.html")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):  # Implement check_password() method in User model
            login_user(user)
            flash("Login successful", "success")
            return redirect('/')
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect('/')