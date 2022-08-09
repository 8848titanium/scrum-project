from flask import render_template, request

from app_pkg import app
import pymysql
import traceback
from app_pkg.userLogin import userLogin

# 导入弹出警告框模块

# import config

# app = Flask(__name__)
# app.config.from_object(config)

# Define two global variables to store the user's name and user's id after user login this system.
global this_user_name, this_user_id


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
    global this_user_name, this_user_id
    email = request.form['email']
    password = request.form['password']

    exist_flag = userLogin().check_exist(email)
    if exist_flag:
        # account_type = True --> this is a student account
        # account_type = False --> this is a lecturer account
        account_type = userLogin().check_type(email)
        if account_type:
            student_result = userLogin().student_login(email, password)
            if student_result == -1:
                return render_template('login.html', tips='Wrong password, please check.')
            else:
                this_user_id = student_result[0]
                this_user_name = student_result[1]
                return render_template('student_main.html', user=this_user_name)
        else:
            userLogin().lecturer_login(email, password)
            lecturer_result = userLogin().student_login(email, password)
            if lecturer_result == -1:
                return render_template('login.html', tips='Wrong password, please check.')
            else:
                this_user_id = lecturer_result[0]
                this_user_name = lecturer_result[1]
                return render_template('lecturer_main.html', user=this_user_name)
    else:
        return render_template('login.html', tips='User not exist, please check the input or register.')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('signup.html')


@app.route('/quiz_student', methods=['POST', 'GET'])
def quiz_student():
    return render_template('quiz_student.html')


@app.route('/student_main')
def student_main():
    return render_template('student_page.html')

# @app.route('/quiz_list', methods=['POST', 'GET'])
# def quiz_list():
#     return render_template('quiz_list.html')
