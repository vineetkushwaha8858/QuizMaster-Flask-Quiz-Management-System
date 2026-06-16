from flask import render_template, request,jsonify,session,flash,redirect,url_for
from flask_bcrypt import Bcrypt
import re
from app.models import create_user,get_users_list,get_user_details,update_user_details,getuser_count,delete_user,model_quiz_getAll,model_get_quiz_details,model_get_question_details,model_get_questions_by_quiz_id,model_get_correct_answers,model_save_question_attempts,model_calculate_total_score,model_get_user_results



bcrypt = Bcrypt()

def dashboard_page():
    return render_template('user/dashboard.html')


#---------------------------------------Log Out  -------------------------
def logout():
    session.pop('user_logged_in', None)
    session.pop('user_email', None)
    session.pop('user_id',None)
    flash("👋 User Logged out successfully!", "info")
    return redirect(url_for('index.login'))


def quizes_list():
    quizzes  = model_quiz_getAll()
    return render_template('user/quizes/quizes_list.html',quizzes=quizzes)

def quiz_attempt(quiz_id):
    quiz = model_get_quiz_details(quiz_id)
    questions = model_get_questions_by_quiz_id(quiz_id)
    print(questions)
    return render_template('user/quizes/quiz_ui.html',quiz=quiz,questions=questions)



def user_submit_quiz(quiz_id):
    user_id = session.get('user_id')
    user_answers = request.form  # Get submitted answers

    # Get correct answers from the database
    correct_answers = model_get_correct_answers(quiz_id)

    attempts = []  # Store each question attempt

    for question_id, correct_option in correct_answers.items():
        user_choice = user_answers.get(f'q{question_id}')  # Get user-selected option
        scored_mark = '1' if user_choice and int(user_choice) == correct_option else '0'

        # Append each question attempt
        attempts.append((quiz_id, question_id, user_id, user_choice, scored_mark))

    # Store all attempts in DB
    if model_save_question_attempts(attempts) == True:
        flash('Quiz Submitted Successfully','success')
        return redirect(url_for('user.user_quiz_result', quiz_id=quiz_id))
    else: 
        flash('Quiz Failed To Submit','danger')
        return redirect(url_for('user.user_quiz_result', quiz_id=quiz_id))
    

def user_quiz_result(quiz_id):
    user_id = session.get('user_id')

    # Fetch total score from question attempts
    score, total_questions = model_calculate_total_score(user_id, quiz_id)
    percentage = round((score / total_questions) * 100, 2) if total_questions > 0 else 0

    return render_template('user/quizes/result.html', 
                           quiz_id=quiz_id, 
                           score=score, 
                           total_questions=total_questions,
                           percentage=percentage)


def user_my_result(user_id):
    user_id = session.get('user_id')  # Get the logged-in user ID
    results = model_get_user_results(user_id)  # Fetch quiz results from the database
    return render_template('user/quizes/result_summary.html', results=results)