from flask import render_template, request

from app_pkg import app
# import pymysql
# import traceback
from app_pkg.user_handler import *

# 导入弹出警告框模块

# import config

# app = Flask(__name__)
# app.config.from_object(config)

# Define a global variable to store user info after successfully login to the system.
global current_user
global current_pin


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


@app.route('/login_check', methods=['POST', 'GET'])
def login_check():
    global current_user
    current_user = User(email=request.form['email'], password=request.form['password'])

    # check for existing user
    if current_user.check_exist():
        result = current_user.login()
        if result:
            current_user.user_id = result[0]
            current_user.user_name = result[1]
            if current_user.user_type == "student":
                return render_template('student_main.html', user=current_user.user_name)
            else:
                return render_template('lecturer_main.html', user=current_user.user_name)
        else:
            return render_template('login.html', tips='Wrong password, please try again.')
    else:
        return render_template('login.html', tips='User non-exist, please check your input or sign-up.')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('signup.html', name="")


@app.route('/signup_check', methods=['POST', 'GET'])
def signup_check():
    input_name = request.form['username']
    input_email = request.form['email']
    password1 = request.form['password1']
    password2 = request.form['password2']
    account_type = request.form['type']
    if input_name and input_email and password1 and password2:
        if password1 == password2:
            new_user = User(input_email, input_name, password1, account_type)
            if new_user.check_exist():  # check user email is existing or not
                return render_template('signup.html', tips='This email has been registered already!')
            else:
                new_user.signup()
                if new_user.user_type == "student":
                    return render_template('student_main.html', user=new_user.user_name)
                else:
                    return render_template('lecturer_main.html', user=new_user.user_name)
        else:
            return render_template('signup.html', name=input_name, tips='Password mismatch, please try again.')
    else:
        return render_template('signup.html', tips='Please fill all the fields.')


@app.route('/quiz_student', methods=['POST', 'GET'])
def quiz_student():
    global current_pin
    current_pin = request.form["quiz_PIN"]
    if launch_quiz(current_pin):
        return render_template('quiz_student.html')
    else:
        return render_template('index.html')


@app.route('/student_main')
def student_main():
    return render_template('student_main.html')


@app.route('/quiz_lecturer')
def quiz_lecturer():
    return render_template('quiz_lecturer.html')


@app.route('/create_quiz')
def create_quiz():
    return render_template('create_quiz.html')


# @app.route('/quiz_list', methods=['POST', 'GET'])
# def quiz_list():
#     return render_template('quiz_list.html')


@app.route('/lecturer_main')
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