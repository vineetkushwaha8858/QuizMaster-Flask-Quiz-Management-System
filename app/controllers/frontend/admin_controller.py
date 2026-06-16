from flask import render_template, request,jsonify,session,flash,redirect,url_for
from flask_bcrypt import Bcrypt
import re
from app.models import create_user,get_users_list,get_user_details,update_user_details,getuser_count,delete_user

from app.models import model_subject_add,model_get_subjects,model_get_subject_count,model_delete_subject,model_subject_updated,model_get_subjects_details

from app.models import modal_chapter_create,modal_chapter_getAll,model_delete_chapter,model_get_chapter_details,model_get_chapter_count,model_chapter_updated,model_quiz_create,model_get_quiz_details,model_get_quiz_count,model_quiz_getAll,model_delete_quiz,model_quiz_update,model_get_all_user_results

from app.models import model_question_create,model_question_delete,model_question_getAll,model_get_question_details,model_get_question_count,model_question_update

bcrypt = Bcrypt()

#---------------------------------------Dashboard Methods-------------------------

def dashboard_page():
        user_count = getuser_count()
        subject_count = model_get_subject_count()
        chapter_count = model_get_chapter_count()
        quiz_count = model_get_quiz_count()
        question_count = model_get_question_count()
        return render_template('admin/dashboard.html',user_count=user_count,subject_count=subject_count,chapter_count = chapter_count,quiz_count=quiz_count,question_count=question_count)

#---------------------------------------Log Out  -------------------------
def logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_email', None)
    session.pop('admin_id',None)
    flash("👋 Logged out successfully!", "info")
    return redirect(url_for('index.login'))

#------------------------------------ User Methods -----------------------------------
def user_add(methods):
        if methods == 'POST':
            full_name = request.form.get('fullname','').strip()
            email = request.form.get('email','').strip()
            password = request.form.get('password','').strip()
            qualification = request.form.get('qualification','').strip()
            dob = request.form.get('dob','').strip()

            #Validation for the Form
            # 1️⃣ Check if any field is empty
            if not full_name or not email or not password or not qualification or not dob:
                  flash("All fields are required!", "danger")
                  return render_template('admin/user/add.html')

            # 2️⃣ Validate Email Format
            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_pattern, email):
                  flash("Invalid email format!", "danger")
                  return render_template('admin/user/add.html')

            # 3️⃣ Password Length Check
            if len(password) < 6:
                  flash("Password must be at least 6 characters long!", "danger")
                  return render_template('admin/user/add.html')
            
            #Hash Form form of the Type Error.
            hashed_password = bcrypt.generate_password_hash(password)
            user = {
                     'fullname':full_name,
                     'email':email,
                     'password':hashed_password,      
                     'qualification':qualification,
                     'dob':dob
              }
            
            inserted = create_user(user)
            if inserted == True:
                     flash('user created successfully','success')
                     return redirect(url_for('admin.admin_create_user_listing'))
            else:     
                     flash('cannot created the Record','danger')
                     return redirect(url_for('admin.admin_create_user_listing')) 
              
              
        else:    
                return render_template('admin/user/add.html')
              
def user_listing():
      users = get_users_list()
      return render_template('admin/user/show.html',users=users)

def user_edit(methods,user_id):
      if methods == 'POST':
            print(request.form.to_dict())
            full_name = request.form.get('fullname','').strip()
            email = request.form.get('email','').strip()
            qualification = request.form.get('qualification','').strip()
            dob = request.form.get('dob','').strip()
            user = get_user_details(user_id)
            #Validation for the Form
            # 1️⃣ Check if any field is empty
            if not full_name or not email or not qualification or not dob:
                  flash("All fields are required!", "danger")
                  return render_template('admin/user/edit.html',user=user)

            # 2️⃣ Validate Email Format
            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_pattern, email):
                  flash("Invalid email format!", "danger")
                  return render_template('admin/user/edit.html',user=user)
            
            updated_user = {
                     'fullname':full_name,
                     'email':email,    
                     'qualification':qualification,
                     'dob':dob
              }
            
            updated = update_user_details(user_id,updated_user)
            if updated == True:
                     flash('user updated successfully','success')
                     return redirect(url_for('admin.admin_create_user_listing'))
            else:     
                     flash('cannot updated the Record','danger')
                     return redirect(url_for('admin.admin_create_user_listing')) 
      else: 
             user = get_user_details(user_id)
             return render_template('admin/user/edit.html',user=user)

def user_delete(user_id):
            if delete_user(user_id) == True:
                   flash('User Deleted Successfully','success')
                   return redirect(url_for('admin.admin_create_user_listing'))  
            else:
                   flash('User Not Deleted Succssfully','danger')
                   return redirect(url_for('admin.admin_create_user_listing'))

#----------------------------Subject Methods -----------------------------------
def subject_add(methods):
      if methods == 'POST':
            name = request.form['name']
            description = request.form['description']
            difficulty_level = request.form['difficulty_level']

            #----------------Validation All Required !!!----------------------
            if not name or not description or not difficulty_level:
                  flash('All Field are Required','danger')
                  return redirect('admin/subject/add_subject.html')
            
            subject = {
                   'name':name,
                   'description':description,
                   'difficulty_level':difficulty_level,
            }

            inserted = model_subject_add(subject)
            if inserted == True:
                  flash('subject added successfully','success')
                  return redirect(url_for('admin.admin_subject_show'))
            else:
                  flash('subject cannot be added','danger')
                  return redirect(url_for('admin.admin_subject_show'))
      else:
          return render_template('admin/subject/add_subject.html')
        

def subject_edit(methods,subject_id):
      if methods == 'POST':
            subject = model_get_subjects_details(subject_id)
            name = request.form.get('name','').strip()
            description = request.form.get('description','').strip()
            difficulty_level = request.form.get('difficulty_level','').strip()
            #----------------Validation All Required !!!----------------------
            if not name or not description or not difficulty_level:
                  flash('All Field are Required','danger')
                  return redirect('admin/subject/edit_subject.html',subject=subject)
            
            subject = {
                   'name':name,
                   'description':description,
                   'difficulty_level':difficulty_level,
            }

            updated = model_subject_updated(subject_id,subject)
            if updated == True:
                  flash('subject updated successfully','success')
                  return redirect(url_for('admin.admin_subject_show'))
            else:
                  flash('subject cannot be updated','danger')
                  return redirect(url_for('admin.admin_subject_show'))
      else:
            subject = model_get_subjects_details(subject_id)
            return render_template('admin/subject/edit_subject.html',subject=subject)

def subject_show():
      subjects = model_get_subjects()
      print(subjects)
      return render_template('admin/subject/list_subject.html',subjects=subjects)

def subject_delete(user_id):
      if model_delete_subject(user_id) == True:
            flash('Subject Deleted Successfully','success')
            return redirect(url_for('admin.admin_subject_show'))  
      else:
            flash('Subject Not Deleted Succssfully','danger')
            return redirect(url_for('admin.admin_subject_show'))


#-------------------------Chapter Methods--------------------------------
def chapter_show():
       subjects = model_get_subjects()
       chapters = modal_chapter_getAll()
       return render_template('admin/chapter/show.html',subjects=subjects,chapters=chapters)

def chapter_create(methods):
      if methods == 'POST':
            name = request.form.get('name','').strip()
            description = request.form.get('description','').strip()
            subject_id = request.form.get('subject_id','').strip()

            #Validation for request form 
            if not name or not description or not subject_id:
                  flash('All Fields are Required','danger')
                  return render_template('admin/chapter/add.html')

            chapter = {
                   'name' : name,
                   'description':description,
                   'subject_id' : subject_id
            }

            if modal_chapter_create(chapter = chapter,) == True:
                   flash('Chapter Created Successfully','success')
                   return redirect(url_for('admin.admin_chapter_show'))
            else:
                   flash('cannot create the chapter','danger')
                   return redirect(url_for('admin.admin_chapter_show'))
      else: 
            subjects = model_get_subjects()
            return render_template('admin/chapter/add.html',subjects=subjects)
       
def chapter_delete(chapter_id):
      if model_delete_chapter(chapter_id) == True:
            flash('Chapter Deleted Successfully','success')
            return redirect(url_for('admin.admin_chapter_show'))  
      else:
            flash('Chapter Not Deleted Succssfully','danger')
            return redirect(url_for('admin.admin_chapter_show'))
      
def chapter_edit(methods,chapter_id):
      if methods == 'POST':

            subjects = model_get_subjects()
            chapter = model_get_chapter_details(chapter_id)
            name = request.form.get('name','').strip()
            description = request.form.get('description','').strip()
            subject_id = request.form.get('subject_id','').strip()

            #Validation for request form 
            if not name or not description or not subject_id:
                  flash('All Fields are Required','danger')
                  render_template('admin/chapter/edit.html',subjects=subjects,chapter=chapter)

            chapter = {
                   'name' : name,
                   'description':description,
                   'subject_id' : subject_id
            }

            if model_chapter_updated(chapter_id=chapter_id,chapter = chapter) == True:
                   flash('Chapter updated Successfully','success')
                   return redirect(url_for('admin.admin_chapter_show'))
            else:
                   flash('cannot update the chapter','danger')
                   return redirect(url_for('admin.admin_chapter_show'))
      else: 
            subjects = model_get_subjects()
            chapter = model_get_chapter_details(chapter_id)
            return render_template('admin/chapter/edit.html',subjects=subjects,chapter=chapter)
      
#---------------------------------- Quiz Methods--------------------------------------------
def quiz_create(methods):
      chapters = modal_chapter_getAll()
      if methods == 'POST':
            name = request.form.get('name','').strip()
            description = request.form.get('description','').strip()
            chapter_id = request.form.get('chapter_id','').strip()
            start_date = request.form.get('start_date','').strip()
            end_date = request.form.get('end_date','').strip()
            status = request.form.get('status','').strip()
            time_duration = request.form.get('time_duration','').strip()
            remarks = request.form.get('remarks','').strip()

            #Validation for request form 
            if not name or not description or not chapter_id or not start_date or not end_date or not status or not time_duration or not remarks:
                  flash('All Fields are Required','danger')
                  render_template('admin/quizes/add_quiz.html',chapters=chapters)

            quiz = {
                   'name' : name,
                   'description':description,
                   'chapter_id' : chapter_id,
                   'start_date' : start_date,
                   'end_date' : end_date,
                   'status' : status,
                   'time_duration' : time_duration,
                   'remarks' : remarks
            }

            if model_quiz_create(quiz = quiz) == True:
                   flash('Quiz Created Successfully','success')
                   return redirect(url_for('admin.admin_quiz_show'))
            else:
                   flash('cannot create the Quiz','danger')
                   return redirect(url_for('admin.admin_quiz_show'))
            
      else:
            return render_template('admin/quizes/add_quiz.html',chapters=chapters)
            
      
def quiz_show():
       quizzes = model_quiz_getAll()
       chapters = modal_chapter_getAll()
       return render_template('admin/quizes/show_quiz.html',quizzes=quizzes,chapters=chapters)

def quiz_edit(methods,quiz_id):
      chapters = modal_chapter_getAll()
      quiz = model_get_quiz_details(quiz_id)
      if methods == 'POST':
            name = request.form.get('name','').strip()
            description = request.form.get('description','').strip()
            chapter_id = request.form.get('chapter_id','').strip()
            start_date = request.form.get('start_date','').strip()
            end_date = request.form.get('end_date','').strip()
            status = request.form.get('status','').strip()
            time_duration = request.form.get('time_duration','').strip()
            remarks = request.form.get('remarks','').strip()

            #Validation for request form 
            if not name or not description or not chapter_id or not start_date or not end_date or not status or not time_duration or not remarks:
                  flash('All Fields are Required','danger')
                  render_template('admin/quizes/add_quiz.html',chapters=chapters,quiz=quiz)

            updated_quiz = {
                   'name' : name,
                   'description':description,
                   'chapter_id' : chapter_id,
                   'start_date' : start_date,
                   'end_date' : end_date,
                   'status' : status,
                   'time_duration' : time_duration,
                   'remarks' : remarks
            }

            if model_quiz_update(quiz = updated_quiz,quiz_id=quiz_id) == True:
                   flash('Quiz Updated Successfully','success')
                   return redirect(url_for('admin.admin_quiz_show'))
            else:
                   flash('cannot updated the Quiz','danger')
                   return redirect(url_for('admin.admin_quiz_show'))
            
      else:
            return render_template('admin/quizes/add_quiz.html',chapters=chapters,quiz=quiz)
      
def quiz_delete(quiz_id):
      if model_delete_quiz(quiz_id) == True:
            flash('Quiz Deleted Successfully','success')
            return redirect(url_for('admin.admin_quiz_show'))  
      else:
            flash('Quiz Not Deleted Succssfully','danger')
            return redirect(url_for('admin.admin_quiz_show'))
      
def view_users_scores():
    results = model_get_all_user_results()  # Fetch all user quiz results
    return render_template('admin/result/result_summary.html', results=results)
      
# ----------------------> Question Controller Methods <-----------------------

def question_create(methods):
    quizzes = model_quiz_getAll()
    if methods == 'POST':
        quiz_id = request.form.get('quiz_id', '').strip()
        question_text = request.form.get('question', '').strip()
        option_1 = request.form.get('option_1', '').strip()
        option_2 = request.form.get('option_2', '').strip()
        option_3 = request.form.get('option_3', '').strip()
        option_4 = request.form.get('option_4', '').strip()
        correct_option = request.form.get('correct_option', '').strip()
        correct_mark = request.form.get('correct_mark', '1').strip()
        wrong_mark = request.form.get('wrong_mark', '0').strip()

        # Validation
        if not quiz_id or not question_text or not correct_option:
            flash('Quiz, Question, and Correct Option are required', 'danger')
            return render_template('admin/questions/add_question.html', quizzes=quizzes)

        question = {
            'quiz_id': quiz_id,
            'question': question_text,
            'option_1': option_1,
            'option_2': option_2,
            'option_3': option_3,
            'option_4': option_4,
            'correct_option': correct_option,
            'correct_mark': correct_mark,
            'wrong_mark': wrong_mark
        }

        if model_question_create(question):
            flash('Question Created Successfully', 'success')
            return redirect(url_for('admin.admin_question_show'))
        else:
            flash('Cannot create the Question', 'danger')
            return redirect(url_for('admin.admin_question_show'))

    else:
        return render_template('admin/questions/add_question.html', quizzes=quizzes)


def question_show():
    questions = model_question_getAll()
    quizzes = model_quiz_getAll()
    return render_template('admin/questions/show_question.html', questions=questions, quizzes=quizzes)


def question_edit(methods, question_id):
    quizzes = model_quiz_getAll()
    question = model_get_question_details(question_id)
    if methods == 'POST':
        quiz_id = request.form.get('quiz_id', '').strip()
        question_text = request.form.get('question', '').strip()
        option_1 = request.form.get('option_1', '').strip()
        option_2 = request.form.get('option_2', '').strip()
        option_3 = request.form.get('option_3', '').strip()
        option_4 = request.form.get('option_4', '').strip()
        correct_option = request.form.get('correct_option', '').strip()
        correct_mark = request.form.get('correct_mark', '1').strip()
        wrong_mark = request.form.get('wrong_mark', '0').strip()

        # Validation
        if not quiz_id or not question_text or not correct_option:
            flash('Quiz, Question, and Correct Option are required', 'danger')
            return render_template('admin/questions/add_question.html', quizzes=quizzes, question=question)

        updated_question = {
            'quiz_id': quiz_id,
            'question': question_text,
            'option_1': option_1,
            'option_2': option_2,
            'option_3': option_3,
            'option_4': option_4,
            'correct_option': correct_option,
            'correct_mark': correct_mark,
            'wrong_mark': wrong_mark
        }

        if model_question_update(question_id, updated_question):
            flash('Question Updated Successfully', 'success')
            return redirect(url_for('admin.admin_question_show'))
        else:
            flash('Cannot update the Question', 'danger')
            return redirect(url_for('admin.admin_question_show'))

    else:
        return render_template('admin/questions/add_question.html', quizzes=quizzes, question=question)


def question_delete(question_id):
    if model_question_delete(question_id):
        flash('Question Deleted Successfully', 'success')
    else:
        flash('Cannot delete the Question', 'danger')
    return redirect(url_for('admin.admin_question_show'))

