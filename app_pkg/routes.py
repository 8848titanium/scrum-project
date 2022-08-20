from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app_pkg import app
from app_pkg import db
from app_pkg.forms import LoginForm, RegistrationForm, JoinQuizForm
from app_pkg.user_handler import *
from app_pkg.models import *

# import pymysql
# import traceback

ROLES = ['lecturer', 'student']


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    form = JoinQuizForm()
    if form.validate_on_submit():
        quiz = Quiz.query.filter_by(pin=form.pin.data).first()
        if quiz is None:
            return redirect(url_for('index'))
        return render_template('quiz_student.html')
    return render_template('index.html', title='Home', form=form)


@app.route('/about', methods=['POST', 'GET'])
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
        user = User(username=form.username.data, email=form.email.data)
        user.type = ROLES[0] if form.type.data else ROLES[1]  # 0 for lecturer, 1 for student
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)


@app.route('/student_main')
@login_required
def student_main():
    return render_template('student_main.html')


@app.route('/quiz_lecturer')
@login_required
def quiz_lecturer():
    return render_template('quiz_lecturer.html')


@app.route('/create_quiz')
@login_required
def create_quiz():
    return render_template('create_quiz.html')


# @app.route('/quiz_list', methods=['POST', 'GET'])
# def quiz_list():
#     return render_template('quiz_list.html')


@app.route('/lecturer_main')
@login_required
def lecturer_main():
    return render_template('lecturer_main.html')


@app.route('/load_quiz', methods=['POST', 'GET'])
def load_quiz():
    global current_pin
    questions = launch_quiz(current_pin)
    a, b, c, d = questions[0].get('choices')
    return '<span>%s</span><span>%s</span><span>%s</span><span>%s</span><span>%s</span>' % (questions[0].get('question'), a, b, c, d)

# @app.route('/lecturer_main')
# def lecturer_main():
#     return render_template('lecturer_main.html')


@app.route('/lec_add_question', methods=['POST', 'GET'])
def lec_add_question():
    a_quiz = Quiz(current_user.user_id)
    a_quiz.add_question(request.form['question'], 'Category Undefined', request.form['choices'], 'Answer Undefined')
    return render_template('create_quiz.html')


@app.route('/my_quiz', methods=['POST', 'GET'])
def my_quiz():
    return render_template('my_quiz.html')