from flask import Flask,Blueprint,redirect,url_for,request
from app.controllers.frontend import index_controller,admin_controller,user_controller
from app.middleware import auth

index_bp = Blueprint('index',__name__)
admin_bp = Blueprint('admin',__name__)
users_bp = Blueprint('user',__name__)


@index_bp.route('/')
def home():
    return index_controller.index_page()

@index_bp.route('/signup')
def signup():
     return index_controller.signup_page()

@index_bp.route('/login',methods=['GET','POST'])
def login():
     if request.method == 'POST':
         return index_controller.login(methods='POST')     
     else:
          return index_controller.login_page()

@index_bp.route('/about-us')
def about():
     return index_controller.about_page()


@admin_bp.route('/')
@admin_bp.route('/dashboard')
@auth.login_required
def admin_dashboard():
     return admin_controller.dashboard_page() 

@admin_bp.route('/logout')
@auth.login_required
def admin_logout():
    return admin_controller.logout()

@admin_bp.route('/user/create/form',methods=['GET','POST'])
@auth.login_required
def admin_create_user_form():
     if request.method == 'POST':
         return admin_controller.user_add(methods='POST')     
     else:
          return admin_controller.user_add(methods='GET')
    
@admin_bp.route('/user/show',methods=['GET'])
@auth.login_required
def admin_create_user_listing():
          return admin_controller.user_listing()


@admin_bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@auth.login_required
def admin_edit_user_form(user_id):
     if request.method == 'POST':
          return admin_controller.user_edit(methods='POST',user_id=user_id)
     else:
          return admin_controller.user_edit(methods='GET',user_id=user_id)


@admin_bp.route('/user/delete/<int:user_id>',methods=['GET'])
@auth.login_required
def admin_delete_user(user_id):
          return admin_controller.user_delete(user_id)


@admin_bp.route('/subject/add/form',methods=['GET','POST'])
@auth.login_required
def admin_subject_add_form():
     if request.method == 'POST':
          return admin_controller.subject_add(methods='POST')
     else:
          return admin_controller.subject_add(methods='GET')
     
@admin_bp.route('/subject/show',methods=['GET'])
@auth.login_required
def admin_subject_show():
     return admin_controller.subject_show()

@admin_bp.route('/subject/edit/<int:subject_id>',methods=['GET','POST'])
@auth.login_required
def admin_subject_edit(subject_id):
     if request.method == 'POST':
          return admin_controller.subject_edit(methods='POST',subject_id=subject_id)
     else:
          return admin_controller.subject_edit(methods='GET',subject_id=subject_id)

@admin_bp.route('/subject/delete/<int:subject_id>',methods=['GET'])
@auth.login_required
def admin_subject_delete(subject_id):
     return admin_controller.subject_delete(subject_id)

@admin_bp.route('/chapter/add',methods=['GET','POST'])
@auth.login_required
def admin_chapter_add():
     if request.method == 'POST':
          return admin_controller.chapter_create(methods='POST')
     else:
          return admin_controller.chapter_create(methods='GET')

@admin_bp.route('/chapter/show',methods=['GET'])
@auth.login_required
def admin_chapter_show():
     return admin_controller.chapter_show()

@admin_bp.route('/chapter/edit/<int:chapter_id>',methods=['GET','POST'])
@auth.login_required
def admin_chapter_edit(chapter_id):
     if request.method == 'POST':
          return admin_controller.chapter_edit(methods='POST',chapter_id=chapter_id)
     else:
          return admin_controller.chapter_edit(methods='GET',chapter_id=chapter_id)

@admin_bp.route('/chapter/delete/<int:chapter_id>',methods=['GET'])
@auth.login_required
def admin_chapter_delete(chapter_id):
     return admin_controller.chapter_delete(chapter_id)

@admin_bp.route('/show/results',methods=['GET'])
@auth.login_required
def admin_view_scores():
     return admin_controller.view_users_scores()

#-----------------------Routes of the Quizes------------------------

@admin_bp.route('/quiz/add',methods=['GET','POST'])
@auth.login_required
def admin_quiz_add():
     if request.method == 'POST':
          return admin_controller.quiz_create(methods='POST')
     else:
          return admin_controller.quiz_create(methods='GET')
     

@admin_bp.route('/quiz/show',methods=['GET'])
@auth.login_required
def admin_quiz_show():
     return admin_controller.quiz_show()


@admin_bp.route('/quiz/edit/<int:quiz_id>',methods=['GET','POST'])
@auth.login_required
def admin_quiz_edit(quiz_id):
     if request.method == 'POST':
          return admin_controller.quiz_edit(methods='POST',quiz_id=quiz_id)
     else:
          return admin_controller.quiz_edit(methods='GET',quiz_id=quiz_id)
     
@admin_bp.route('/quiz/delete/<int:quiz_id>',methods=['GET'])
@auth.login_required
def admin_quiz_delete(quiz_id):
     return admin_controller.quiz_delete(quiz_id)

# ------------------------------------------ Routes for Questions ---------------------------------------

@admin_bp.route('/question/add', methods=['GET', 'POST'])
@auth.login_required
def admin_question_add():
    if request.method == 'POST':
        return admin_controller.question_create(methods='POST')
    else:
        return admin_controller.question_create(methods='GET')


@admin_bp.route('/question/show', methods=['GET'])
@auth.login_required
def admin_question_show():
    return admin_controller.question_show()


@admin_bp.route('/question/edit/<int:question_id>', methods=['GET', 'POST'])
@auth.login_required
def admin_question_edit(question_id):
    if request.method == 'POST':
        return admin_controller.question_edit(methods='POST', question_id=question_id)
    else:
        return admin_controller.question_edit(methods='GET', question_id=question_id)


@admin_bp.route('/question/delete/<int:question_id>', methods=['GET'])
@auth.login_required
def admin_question_delete(question_id):
    return admin_controller.question_delete(question_id)

#----------------------------------user dashboard----------------------------
@users_bp.route('/')
@users_bp.route('/dashboard')
@auth.user_login_required
def user_dashboard():
     return user_controller.dashboard_page() 


@users_bp.route('/mock/quizes')
@auth.user_login_required
def user_myquizes_list():
     return user_controller.quizes_list()

@users_bp.route('/mock/quiz/info/<int:quiz_id>')
@auth.user_login_required
def user_quiz_info(quiz_id):
    pass 

@users_bp.route('/mock/quiz/attempt/<int:quiz_id>')
@auth.user_login_required
def user_start_quiz(quiz_id):
    return user_controller.quiz_attempt(quiz_id)    

@users_bp.route('/mock/quiz/submit/<int:quiz_id>',methods=['POST'])
@auth.user_login_required
def user_submit_quiz(quiz_id):
     return user_controller.user_submit_quiz(quiz_id)


@users_bp.route('/quiz/result/<int:quiz_id>')
@auth.user_login_required
def user_quiz_result(quiz_id):
    return user_controller.user_quiz_result(quiz_id)

@users_bp.route('/mock/quiz/result/<int:user_id>')
@auth.user_login_required
def user_all_result(user_id):
    return user_controller.user_my_result(user_id)
    
    
@users_bp.route('/user/logout')
@auth.user_login_required
def user_logout():
    return user_controller.logout()


