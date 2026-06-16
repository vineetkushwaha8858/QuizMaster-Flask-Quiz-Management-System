from flask import Flask, Blueprint, redirect, url_for, request, session, flash
from functools import wraps

# Decorator to restrict access to logged-in users
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_email' not in session or 'admin_logged_in' not in session:  # Assuming 'admin_id' is stored in session upon login
            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for('index.login'))  # Redirect to login page
        return f(*args, **kwargs)
    return decorated_function


# Decorator to restrict access to logged-in users
def user_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session or 'user_logged_in' not in session:  # Assuming 'user_id' is stored in session upon login
            flash("User must be logged in to access this page.", "warning")
            return redirect(url_for('index.login'))  # Redirect to login page
        return f(*args, **kwargs)
    return decorated_function
