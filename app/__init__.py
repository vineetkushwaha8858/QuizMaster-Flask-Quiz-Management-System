from flask import Flask
from app.models import model_count_no_of_question_in_quiz
 
def create_app():
    app = Flask(__name__)
    app.secret_key  = 'Your_Secret_key'

    #Import the Globals Utility.
    app.jinja_env.globals['model_helper'] = {}
    app.jinja_env.globals['model_helper']['get_questions_count'] = model_count_no_of_question_in_quiz


    #Set Application Context Manager
    with app.app_context():
        from app.models import initialise_db,create_admin
        initialise_db() #create Tables.

        # Admin Credentials for Login
        admin_credentials = {
            'admin':'admin@gmail.com',
            'password':'admin@123'
        }

        create_admin(admin_email = admin_credentials['admin'],admin_password = admin_credentials['password'])

    #Web Routes Blueprint
    from app.routes.web import index_bp
    app.register_blueprint(index_bp,url_prefix='/')


    #Api Routes Blueprint
    from app.routes.web import users_bp
    app.register_blueprint(users_bp,url_prefix='/user')

    #admin Routes Blueprint
    from app.routes.web import admin_bp
    app.register_blueprint(admin_bp,url_prefix='/admin')

    return app







