import json
import random
import string
import time

from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from flask_socketio import emit, send
from werkzeug.urls import url_parse

from app_pkg import app, socketio
from app_pkg.forms import *
from app_pkg.models import *

ROLES = ['lecturer', 'student']
CHOICES = ['A', 'B', 'C', 'D']
PIN_LENGTH = 6
COUNTDOWN = 10
GAP_ANSWERING_TIME = 2

question_launch_time = 0
current_rank_scores = {}


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = JoinQuizForm()  # arg.request - from url, url - ?  # 有form的时候就直接从forms.py里get前端input
    if form.validate_on_submit():
        quiz = Quiz.query.filter_by(pin=form.pin.data).first()  # get quiz from db
        if quiz:
            return redirect('/quiz_play/' + str(quiz.pin))  # jump to direct url
    return render_template('index.html', title='Home', form=form)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # block manually access to /login if one user already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # url_for jump to route function

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
    # remove all pin when lecturer logout
    if current_user.type == "lecturer":
        for quiz in Quiz.query.filter_by(user_id=current_user.id):
            quiz.pin = None
            db.session.commit()
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


@app.route('/lecturer_main', methods=['GET', 'POST'])
@login_required
def lecturer_main():
    return render_template('lecturer_main.html', quizzes=Quiz.query.filter_by(user_id=current_user.id))


@app.route('/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    quiz_entry = Quiz(user_id=current_user.id, name='The New Quiz',
                      pin=None)
    db.session.add(quiz_entry)
    db.session.commit()
    return redirect(url_for('lecturer_main'))


@app.route('/edit_quiz/<quiz_id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(quiz_id):
    the_pin = ''.join(random.choice(string.digits) for _ in range(PIN_LENGTH))
    the_quiz = Quiz.query.filter_by(id=quiz_id).first()
    the_quiz.pin = the_pin
    form = QuizNameForm()
    if form.validate_on_submit():
        the_quiz.name = form.name.data
    db.session.commit()
    return render_template('edit_quiz.html', form=form, question_set=Question.query.filter_by(quiz_id=quiz_id),
                           quiz=the_quiz)


@app.route('/edit_quiz/quiz_history/<quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz_history(quiz_id):
    num_of_questions = db.session.query(Question).filter_by(quiz_id=quiz_id).count()
    user_join_score = db.session.query(Score, User).filter(Score.quiz_id == quiz_id).filter(
        Score.student_id == User.id).all()
    return render_template('quiz_history.html', user_join_score=user_join_score, num_of_questions=num_of_questions)


@app.route('/delete_quiz/', methods=['GET', 'POST'])
@login_required
def delete_quiz():
    quiz_id = request.args.get('id')
    the_quiz = Quiz.query.filter_by(id=quiz_id).first()
    questions = Question.query.filter_by(quiz_id=quiz_id)
    scores = Score.query.filter_by(quiz_id=quiz_id)
    for score in scores:
        db.session.delete(score)
    for question in questions:
        db.session.delete(question)
    db.session.delete(the_quiz)
    db.session.commit()
    return redirect(url_for('lecturer_main'))


@app.route('/create_question/<quiz_id>', methods=['GET', 'POST'])
@login_required
def create_question(quiz_id):
    question_entry = Question(quiz_id=quiz_id, question="The New Question")
    db.session.add(question_entry)
    db.session.commit()
    return redirect('/edit_quiz/' + quiz_id)


@app.route('/edit_question/<quiz_id>/', methods=['GET', 'POST'])
@login_required
def edit_question(quiz_id):
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
        return redirect('/edit_quiz/' + str(quiz_id))
    return render_template('edit_question.html', form=form, question=question)


@app.route('/student_main', methods=['GET', 'POST'])
@login_required
def student_main():
    quizzes_have_done = db.session.query(Score).join(Quiz).filter(Score.student_id == current_user.id)
    num_of_questions = {}
    for quiz in quizzes_have_done:
        num_of_questions[quiz.quiz_id] = db.session.query(Question).filter_by(quiz_id=quiz.quiz_id).count()
    return render_template('student_main.html', completed_quizzes=quizzes_have_done, num_of_questions=num_of_questions)


@app.route('/quiz_play/<pin>', methods=['GET', 'POST'])
@login_required
def quiz_play(pin):
    quiz_id = Quiz.query.filter_by(pin=pin).first().id
    questions = Question.query.filter_by(quiz_id=quiz_id)  # all questions from the quiz
    list_of_questions = []
    for question in questions:
        question_dict = dict(question.__dict__)
        question_dict.pop('_sa_instance_state', None)
        list_of_questions.append(question_dict)
    return render_template("quiz_play.html", quiz_id=quiz_id, PIN=pin, the_quiz=json.dumps(list_of_questions))


@app.route("/send_quiz_result", methods=["get", "post"])
@login_required
def receive_grade():
    mark_on_questions = request.get_json()
    quiz_id = mark_on_questions.pop("quiz_id")
    current_quiz = Quiz.query.filter_by(id=quiz_id).first()
    score = Score.query.filter_by(student_id=current_user.id, quiz_id=current_quiz.id).first()
    total_mark = sum(mark_on_questions.values())
    if score:
        score.score = total_mark
    else:
        score = Score(student_id=current_user.id, quiz_id=current_quiz.id, score=total_mark)
        db.session.add(score)
    db.session.commit()
    # reset pin after quiz finished
    current_quiz.pin = None
    db.session.commit()
    return "grade saved!"


@socketio.on('message')
def handle_message(message):
    print("Received message:" + message)
    if message != "User connected!":
        send(message, broadcast=True)


@socketio.on('ask-question-block')
def question_block():
    emit("show-question-block", broadcast=True)


@socketio.on("ask-question-content")
def question_content(time_stamp):
    global question_launch_time
    question_launch_time = time_stamp
    emit("show-question-content", broadcast=True)


@socketio.on("ask-next-question")
def next_question(time_stamp):
    global question_launch_time
    global current_rank_scores
    question_launch_time = time_stamp
    emit("show-next-question", current_rank_scores, broadcast=True)


@socketio.on("ask-finish-quiz")
def finish_quiz():
    emit("show-finish-quiz", broadcast=True)


@socketio.on("ask-choice-A")
def choice_a():
    emit("show-select-choice", 'A')


@socketio.on("ask-choice-B")
def choice_b():
    emit("show-select-choice", 'B', )


@socketio.on("ask-choice-C")
def choice_c():
    emit("show-select-choice", 'C')


@socketio.on("ask-choice-D")
def choice_d():
    emit("show-select-choice", 'D')


@socketio.on("calculate-rank-score")
def calculate_rank_score(username, time_answered, is_wrong=False):
    global current_rank_scores
    rank_score = 0 if is_wrong else round(
        ((COUNTDOWN + GAP_ANSWERING_TIME - (time_answered - question_launch_time) / 1000) / COUNTDOWN) * 1000)
    if username not in current_rank_scores:
        current_rank_scores[username] = 0
    current_rank_scores[username] += rank_score


@socketio.on("ask-scoreboard")
def populate_scoreboard():
    global current_rank_scores
    emit("show-populate-scoreboard", current_rank_scores, broadcast=True)


@socketio.on("ask-prevent-choice")
def prevent_choice():
    emit("receive-enable-choice", broadcast=True)


@socketio.on("ask-countdown-block")
def show_countdown():
    emit("show-countdown-block", broadcast=True)


@socketio.on("ask-countdown")
def one_second():
    for i in range(COUNTDOWN, 0, -1):
        time.sleep(1)
        emit("receive-one-second", broadcast=True)


@socketio.on("ask-reset-countdown")
def reset_countdown():
    emit("receive-reset-countdown", broadcast=True)
