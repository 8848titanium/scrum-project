from flask import render_template, request

from app_pkg import app
# import pymysql
# import traceback
from app_pkg.user_handler import User

# 导入弹出警告框模块

# import config

# app = Flask(__name__)
# app.config.from_object(config)

# Define a global variable to store user info after successfully login to the system.
global current_user


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

    exist_flag = current_user.check_exist()
    if exist_flag:
        # account_type = True --> this is a student account
        # account_type = False --> this is a lecturer account
        account_type = current_user.check_type()
        if account_type:
            student_result = current_user.student_login()
            if student_result == -1:
                return render_template('login.html', tips='Wrong password, please check.')
            else:
                current_user.user_id = student_result[0]
                current_user.user_name = student_result[1]
                return render_template('student_main.html', user=current_user.user_name)
        else:
            current_user.lecturer_login()
            lecturer_result = current_user.lecturer_login()
            if lecturer_result == -1:
                return render_template('login.html', tips='Wrong password, please check.')
            else:
                current_user.user_id = lecturer_result[0]
                current_user.user_name = lecturer_result[1]
                return render_template('lecturer_main.html', user=current_user.user_name)
    else:
        return render_template('login.html', tips='User not exist, please check the input or register.')


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
    return render_template('quiz_student.html')


@app.route('/student_main')
def student_main():
    return render_template('student_main.html')

# @app.route('/quiz_list', methods=['POST', 'GET'])
# def quiz_list():
#     return render_template('quiz_list.html')
