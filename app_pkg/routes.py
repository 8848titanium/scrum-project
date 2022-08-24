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
def create_quiz():
    quiz = Quiz(user_id=current_user.id, name='The New Quiz',
                pin=''.join(random.choice(string.digits) for i in range(PIN_LENGTH)))
    db.session.add(quiz)
    db.session.commit()
    return redirect(url_for('lecturer_main'))


@app.route('/edit_quiz/', methods=['GET', 'POST'])
def edit_quiz():
    quiz_id = request.args.get("id")
    print(quiz_id)


@app.route('/get_quiz_id', methods=['GET', 'POST'])
def get_quiz_id():
    most_recent_quiz = conn_mul("SELECT MAX(id) FROM quiz WHERE user_id = '%s'" % current_user.id)
    all_quiz_id = conn_mul("SELECT id FROM quiz WHERE user_id = '%s'" % current_user.id)
    quiz_id_list = []
    for row in all_quiz_id:
        quiz_id_list.append(row[0])
        # 这里可以execute javascript就是往网页上添加按钮
    return render_template('get_quiz_id.html', recent_quiz=most_recent_quiz[0][0], all_quiz=str(quiz_id_list),
                           quiz_count=most_recent_quiz[0][0])


@app.route('/load_quiz', methods=['GET', 'POST'])
def load_quiz():
    global current_pin
    questions = launch_quiz(current_pin)
    a, b, c, d = questions[0].get('choices')
    return '<span>%s</span><span>%s</span><span>%s</span><span>%s</span><span>%s</span>' % (
        questions[0].get('question'), a, b, c, d)


@app.route('/student_main', methods=['GET', 'POST'])
@login_required
def student_main():
    return render_template('student_main.html')


@app.route('/lec_add_question', methods=['GET', 'POST'])
def lec_add_question():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        quiz = Quiz(user_id=current_user.id)
        answer = ''

        if request.form.get('checkbox1') == "on":
            answer = 'A'
        if request.form.get('checkbox2') == "on":
            answer = 'B'
        if request.form.get('checkbox3') == "on":
            answer = 'C'
        if request.form.get('checkbox4') == "on":
            answer = 'D'

        quiz.add_question(request.form['question'], 0, answer)
        return my_quiz()


@app.route('/my_quiz', methods=['GET', 'POST'])
def my_quiz():
    global current_quiz
    all_quiz_id = conn_mul("SELECT * FROM quiz WHERE user_id = '%s'" % current_user.id)
    all_quiz_string = "Those are all the quiz created:\n"
    for row in all_quiz_id:
        all_quiz_string += "Quiz id:\n"
        all_quiz_string += str(row[0])
        all_quiz_string += "Quiz detail:\n"
        all_quiz_string += str(load_questions(row[0]))
        all_quiz_string += "\n"
    # current_quiz = load_questions(1) #quiz id
    return render_template('my_quiz.html', user=current_user, user_name=current_user.username, all_quiz=all_quiz_string)


@app.route('/view_my_quiz', methods=['GET', 'POST'])
def view_my_quiz():
    global current_quiz_id
    global current_quiz_question
    global current_quiz_question_id
    global current_quiz_choiceA
    global current_quiz_choiceB
    global current_quiz_choiceC
    global current_quiz_choiceD
    global ids
    try:
        current_quiz_id = request.form['get_quiz_id']
        all_question_id = [row[0] for row in
                           conn_mul(f"SELECT question_id FROM question where quiz_id={current_quiz_id}")]
        ids = iter(all_question_id)
        current_quiz_question_id = next(ids)
    except:
        current_quiz_question_id = next(ids)
    current_quiz_question = conn_mul(f"SELECT question FROM question where question_id={current_quiz_question_id}")[0][
        0]
    current_quiz_choiceA = conn_mul(f"SELECT A FROM question where question_id={current_quiz_question_id}")[0][0]
    current_quiz_choiceB = conn_mul(f"SELECT B FROM question where question_id={current_quiz_question_id}")[0][0]
    current_quiz_choiceC = conn_mul(f"SELECT C FROM question where question_id={current_quiz_question_id}")[0][0]
    current_quiz_choiceD = conn_mul(f"SELECT D FROM question where question_id={current_quiz_question_id}")[0][0]
    return render_template('view_my_quiz.html', quiz_id=current_quiz_id, question=current_quiz_question,
                           A=current_quiz_choiceA, B=current_quiz_choiceB, C=current_quiz_choiceC,
                           D=current_quiz_choiceD, question_id=current_quiz_question_id)


@app.route('/edit_my_quiz', methods=['GET', 'POST'])
def edit_my_quiz():
    global current_quiz_id
    global current_quiz_question
    global current_quiz_choiceA
    global current_quiz_choiceB
    global current_quiz_choiceC
    global current_quiz_choiceD
    return render_template('edit_my_quiz.html', quiz_id=current_quiz_id, question=current_quiz_question,
                           A=current_quiz_choiceA, B=current_quiz_choiceB, C=current_quiz_choiceC,
                           D=current_quiz_choiceD)


@app.route('/edit_quiz_question', methods=['GET', 'POST'])
def edit_quiz_question():
    question = request.form["question"]  # 这里出问题的可能原因是form没填？？
    a = request.form["op1"]
    b = request.form["op2"]
    c = request.form["op3"]
    d = request.form["op4"]
    choices = [a, b, c, d]
    answer = ''

    if request.form.get('checkbox1') == "on":
        answer = 'A'
    if request.form.get('checkbox2') == "on":
        answer = 'B'
    if request.form.get('checkbox3') == "on":
        answer = 'C'
    if request.form.get('checkbox4') == "on":
        answer = 'D'

    # write_cmd = f"UPDATE question SET question = '{question}' WHERE question_id=1;UPDATE question SET A = '{a}' WHERE question_id=1;UPDATE question SET B = '{b}' WHERE question_id=1;UPDATE question SET C = '{c}' WHERE question_id=1;UPDATE question SET D = '{d}' WHERE question_id=1;"
    # write_cmd = f"UPDATE question SET question = '{question}' WHERE question_id=1;"
    # write_cmd = "UPDATE question SET question = ' Hi ' WHERE question_id=1;"
    write_cmd = f"UPDATE question SET question = '{question}' WHERE question_id={current_quiz_question_id};"
    conn_non(write_cmd)
    # return view_my_quiz()
    return my_quiz()
