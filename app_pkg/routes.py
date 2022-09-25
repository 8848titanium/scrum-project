import json
import random
import string
import time

from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from flask_socketio import emit, send, join_room, leave_room
from sqlalchemy import desc
from werkzeug.urls import url_parse

from app_pkg import app, socketio
from app_pkg.forms import *
from app_pkg.models import *

ROLES = ['lecturer', 'student']
CHOICES = ['A', 'B', 'C', 'D']
PIN_LENGTH = 6
COUNTDOWN = 10
GAP_ANSWERING_TIME = 2

room_to_player = {}


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = JoinQuizForm()
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
        login_user(user)
        return redirect(url_for('index'))
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
    score_join_user = db.session.query(Score, User).filter(Score.quiz_id == quiz_id).filter(
        Score.student_id == User.id).all()
    return render_template('quiz_history.html', score_join_user=score_join_user, num_of_questions=num_of_questions)


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
        question.question = form.question.data
        for field in form:
            if field.type == "BooleanField":
                if field.data:
                    question.answer = field.name[-1].upper()
            else:
                setattr(question, 'choice_' + field.name[-1], field.data)
        db.session.commit()
        return redirect('/edit_quiz/' + str(quiz_id))
    for field in form:
        if field.type == "BooleanField":
            if question.answer == field.name[-1].upper():
                field.data = True
    return render_template('edit_question.html', form=form, question=question)


@app.route('/delete_question/<question_id>', methods=['GET', 'POST'])
def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    return redirect('/edit_quiz/' + str(quiz_id))


@app.route('/student_main', methods=['GET', 'POST'])
@login_required
def student_main():
    score_join_quiz = db.session.query(Score, Quiz).filter(Score.student_id == current_user.id).filter(
        Score.quiz_id == Quiz.id).all()
    num_of_questions = {}
    for row in score_join_quiz:
        num_of_questions[row[1].id] = db.session.query(Question).filter_by(quiz_id=row[1].id).count()
    return render_template('student_main.html', score_join_quiz=score_join_quiz, num_of_questions=num_of_questions)


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
    room_to_player[pin] = {}  # contain player_to_data
    print(room_to_player)
    return render_template("quiz_play.html", quiz_id=quiz_id, PIN=pin, the_quiz=json.dumps(list_of_questions))


@socketio.on('connect')
def connect():
    print(f"{current_user.type} {current_user.username} connected.")


@socketio.on('disconnect')
def disconnect():
    print(f"{current_user.type} {current_user.username} disconnected.")


@socketio.on('join')
def on_join(pin):
    join_room(pin)
    if current_user.type == "lecturer":
        send(f"Lecturer {current_user.username} initiates a game!", to=pin)
    send(f"{current_user.type.capitalize()} {current_user.username} has slided into this game room.", to=pin)


@socketio.on('leave')
def on_leave(pin):
    leave_room(pin)
    if current_user.type == "lecturer":
        room_to_player.pop(pin)
    send(f"Sneaky {current_user.username} has quietly left the room.", to=pin)


@socketio.on("ask-question-block")
def question_block(pin):
    emit("show-question-block", to=pin)


@socketio.on("ask-question-content")
def question_content(pin):
    emit("show-question-content", to=pin)


@socketio.on("ask-next-question")
def next_question(pin):
    emit("show-next-question", room_to_player[pin], to=pin)


@socketio.on("ask-choice-A")
def choice_a():
    emit("show-select-choice", 'A')


@socketio.on("ask-choice-B")
def choice_b():
    emit("show-select-choice", 'B')


@socketio.on("ask-choice-C")
def choice_c():
    emit("show-select-choice", 'C')


@socketio.on("ask-choice-D")
def choice_d():
    emit("show-select-choice", 'D')


@socketio.on("ask-prevent-choice")
def prevent_choice(pin):
    emit("receive-enable-choice", to=pin)


@socketio.on("ask-countdown-block")
def show_countdown(pin):
    emit("show-countdown-block", to=pin)


@socketio.on("ask-countdown")
def one_second(pin):
    for i in range(COUNTDOWN, 0, -1):
        time.sleep(1)
        emit("receive-one-second", to=pin)


@socketio.on("ask-reset-countdown")
def reset_countdown(pin):
    emit("receive-reset-countdown", to=pin)


@socketio.on("calculate-rank-score")
def calculate_rank_score(question_launch_time, time_answered, is_correct, pin):
    username = current_user.username
    rank_score = round(
        ((COUNTDOWN + GAP_ANSWERING_TIME - (
                time_answered - question_launch_time) / 1000) / COUNTDOWN) * 1000) if is_correct else 0
    if username not in room_to_player[pin]:
        room_to_player[pin][username] = 0
    room_to_player[pin][username] += rank_score
    print(room_to_player, current_user.username)


@socketio.on("ask-scoreboard")
def populate_scoreboard(pin):
    emit("show-populate-scoreboard", room_to_player[pin], to=pin)


@socketio.on("send-answer")
def receive_grade(student_answers, pin):
    print(student_answers)
    quiz_id = student_answers.pop("quiz_id")
    rank_score = student_answers.pop("rank_score")
    current_quiz = Quiz.query.filter_by(id=quiz_id).first()
    score = Score.query.filter_by(student_id=current_user.id, quiz_id=current_quiz.id).first()
    total_mark = sum(student_answers.values())
    if score:
        score.score = total_mark
        score.rank_score = rank_score
    else:
        score = Score(student_id=current_user.id, quiz_id=current_quiz.id, score=total_mark, rank_score=rank_score)
        db.session.add(score)
    db.session.commit()
    room_to_player[pin][current_user.username] = None


@socketio.on("ask-finish-quiz")
def finish_quiz(quiz_id, pin):
    while any(room_to_player[pin].values()):
        pass
    total_players = [user.id for user in User.query.filter(User.username.in_(room_to_player[pin].keys()))]
    score_join_user = db.session.query(Score, User).filter(Score.quiz_id == quiz_id).filter(
        Score.student_id == User.id).filter(
        Score.student_id.in_(total_players)).filter(User.id.in_(total_players)).order_by(desc(Score.rank_score)).limit(
        3 if len(total_players) >= 3 else len(total_players)).all()
    top_three = {}
    for row in score_join_user:
        top_three[row[1].username] = row[0].rank_score

    i = 1
    while len(top_three) < 3:
        top_three["Missing Player " + str(i)] = "Nothing"
        i += 1
    emit("show-finish-quiz", top_three, to=pin)
    # reset pin after quiz finished
    Quiz.query.filter_by(id=quiz_id).first().pin = None
    db.session.commit()
    print(room_to_player.pop(pin))
    print(room_to_player)
