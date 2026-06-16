from flask import render_template, request,jsonify,redirect,session,flash,url_for
from flask_bcrypt import Bcrypt 
from app.models import getConnection,validateAdmin

bcrypt = Bcrypt()


def index_page():
        return render_template('index.html')

def signup_page():
        return render_template('signup.html')


def login_page():
        return render_template('login.html')

def login(methods):
    if methods == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validation
        if not email or not password:
            flash("⚠️ Email and Password are required!", "danger")
            return redirect(url_for('login'))

        user,isAdmin = validateAdmin(email=email)

        if user:
            stored_password = user["password"]  # Fetch stored hashed password
            if bcrypt.check_password_hash(stored_password, password):
                if isAdmin:
                    session['admin_logged_in'] = True
                    session['admin_email'] = email
                    session['admin_id'] = user['id']
                    flash("✅ Login successful!", "success")
                    return redirect(url_for('admin.admin_dashboard'))
                else:
                    session['user_logged_in'] = True
                    session['user_id'] = user['id']
                    session['user_email'] = email
                    flash("✅ Login successful!", "success")
                    return redirect(url_for('user.user_dashboard'))
            else:
                flash("❌ Incorrect password!", "danger")
        else:
            flash("❌ No account found with this email!", "danger")

    return render_template('login.html')




def about_page():
        data = {"name":"Prakhar Mishra","organisation":"Prakhar Enterprises"}
        return render_template('about.html',data=data)