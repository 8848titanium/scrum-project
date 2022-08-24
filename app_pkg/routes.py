import random
import string

from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app_pkg import app
from app_pkg.forms import *
from app_pkg.models import *

# import pymysql
# import traceback

ROLES = ['lecturer', 'student']
CHOICES = ['A', 'B', 'C', 'D']
PIN_LENGTH = 6

# Define a global variable to store user info after successfully login to the system.
global current_pin
global current_quiz
global current_quiz_question
global current_quiz_question_id
global current_question_choiceA
global current_question_choiceB
global current_question_choiceC
global current_question_choiceD
global ids


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = JoinQuizForm()
    if form.validate_on_submit():
        return quiz_pin(form)
    return render_template('index.html', title='Home', form=form)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # block manually access to /login if one user already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # return a user object if any exists, or None if it doesn't
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # block manually access to /login if one user already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)  # ignore pycharm unexpected argument warning
        user.type = ROLES[0] if form.type.data else ROLES[1]  # 0 for lecturer, 1 for student
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)


@app.route('/quiz_pin', methods=['GET', 'POST'])
@login_required
def quiz_pin(form):
    quiz = Quiz.query.filter_by(pin=form.pin.data).first()
    if quiz is None:
        return redirect(url_for('index'))
    return render_template('quiz_student.html')


@app.route('/lecturer_main', methods=['GET', 'POST'])
@login_required
def lecturer_main():
    return render_template('lecturer_main.html', quizzes=Quiz.query.filter_by(user_id=current_user.id))


@app.route('/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    quiz_entry = Quiz(user_id=current_user.id, name='The New Quiz',
                      pin=''.join(random.choice(string.digits) for _ in range(PIN_LENGTH)))
    db.session.add(quiz_entry)
    db.session.commit()
    return redirect(url_for('lecturer_main'))


@app.route('/edit_quiz/', methods=['GET', 'POST'])
@login_required
def edit_quiz():
    the_quiz_id = request.args.get("id")
    return render_template('edit_quiz.html', question_set=Question.query.filter_by(quiz_id=the_quiz_id),
                           quiz_id=the_quiz_id)


@app.route('/create_question/', methods=['GET', 'POST'])
@login_required
def create_question():
    quiz_id = request.args.get('id')
    question_entry = Question(quiz_id=quiz_id, question="The New Question")
    db.session.add(question_entry)
    db.session.commit()
    return redirect('/edit_quiz/?id=' + quiz_id)


@app.route('/edit_question/', methods=['GET', 'POST'])
@login_required
def edit_question():
    question = Question.query.filter_by(id=request.args.get("id")).first()

    form = QuestionForm(data=question.__dict__)
    if form.validate_on_submit():
        answer = ""
        for i, checkbox in enumerate(
                [form.checkbox_a.data, form.checkbox_b.data, form.checkbox_c.data, form.checkbox_d.data]):
            if checkbox:
                answer += CHOICES[i]
        question.question = form.question.data
        question.choice_a = form.choice_a.data
        question.choice_b = form.choice_b.data
        question.choice_c = form.choice_c.data
        question.choice_d = form.choice_d.data
        question.answer = answer
        db.session.commit()
        return redirect('/edit_quiz/?id=' + str(question.quiz_id))
    return render_template('edit_question.html', form=form, question=question)


@app.route('/student_main', methods=['GET', 'POST'])
@login_required
def student_main():
    return render_template('student_main.html')
