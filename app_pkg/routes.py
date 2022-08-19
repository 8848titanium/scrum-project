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
global current_quiz
global current_quiz_question
global current_quiz_choiceA
global current_quiz_choiceB
global current_quiz_choiceC
global current_quiz_choiceD

CHOICES = ['A', 'B', 'C', 'D']


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


@app.route('/new_quiz', methods=['POST', 'GET'])
def new_quiz():
    return render_template("quiz_lecturer.html", user=current_user.user_name)


@app.route('/lec_add_question', methods=['POST', 'GET'])
def lec_add_question():
    a_quiz = Quiz(current_user.user_id)
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

    a_quiz.add_question(request.form['question'], 0, choices, answer)
    return my_quiz()


@app.route('/my_quiz', methods=['POST', 'GET'])
def my_quiz():
    global current_quiz
    # current_quiz = Quiz(current_user.user_id)
    all_quiz_id = conn_mul("SELECT * FROM quiz WHERE lecturer_id = '%s'" % current_user.user_id)
    all_quiz_string = "Those are all the quiz created:\n"
    for row in all_quiz_id:
        all_quiz_string += "Quiz id:\n"
        all_quiz_string += str(row[0])
        all_quiz_string += "Quiz detail:\n"
        all_quiz_string += str(load_questions(row[0]))
        all_quiz_string += "\n"
    # current_quiz = load_questions(1) #quiz id
    return render_template('my_quiz.html', user=current_user, user_name=current_user.user_name, all_quiz=all_quiz_string)

@app.route('/js_test', methods=['POST', 'GET'])
def js_test():
    return render_template('js_test.html', question_count=5)
@app.route('/view_my_quiz', methods=['POST', 'GET'])
def view_my_quiz():
    global current_quiz_id
    global current_quiz_question
    global current_quiz_choiceA
    global current_quiz_choiceB
    global current_quiz_choiceC
    global current_quiz_choiceD
    # current_quiz_id = request.form.get('get_quiz_id')
    current_quiz_id = request.form['get_quiz_id']
    current_quiz_question = conn_mul(f"SELECT question FROM question where quiz_id={current_quiz_id}")
    current_quiz_choiceA = conn_mul(f"SELECT A FROM question where quiz_id={current_quiz_id}")
    current_quiz_choiceB = conn_mul(f"SELECT B FROM question where quiz_id={current_quiz_id}")
    current_quiz_choiceC = conn_mul(f"SELECT C FROM question where quiz_id={current_quiz_id}")
    current_quiz_choiceD = conn_mul(f"SELECT D FROM question where quiz_id={current_quiz_id}")
    return render_template('view_my_quiz.html', quiz_id=current_quiz_id[0][0], question=current_quiz_question[0][0],
                           A=current_quiz_choiceA[0][0], B=current_quiz_choiceB[0][0], C=current_quiz_choiceC[0][0],
                           D=current_quiz_choiceD[0][0])
# 如果不用[0][0]只用[0]的话会传回一个tuple,这里暂时只做出了只能看quiz中的第一个问题


@app.route('/get_quiz_id', methods=['POST', 'GET'])
def get_quiz_id():
    most_recent_quiz = conn_mul("SELECT MAX(quiz_id) FROM quiz WHERE lecturer_id = '%s'" % current_user.user_id)
    all_quiz_id = conn_mul("SELECT quiz_id FROM quiz WHERE lecturer_id = '%s'" % current_user.user_id)
    quiz_id_list = []
    for row in all_quiz_id:
        quiz_id_list.append(row[0])
        # 这里可以execute javascript就是往网页上添加按钮
    return render_template('get_quiz_id.html', recent_quiz=most_recent_quiz[0][0], all_quiz=str(quiz_id_list), quiz_count=most_recent_quiz[0][0] )
# edit_my_quiz() tuple - 处理成string并存为变量 - 就可以被读了！处理成-opt1 ,question,opt2这样子


@app.route('/edit_my_quiz', methods=['POST', 'GET'])
def edit_my_quiz():
    global current_quiz_id
    global current_quiz_question
    global current_quiz_choiceA
    global current_quiz_choiceB
    global current_quiz_choiceC
    global current_quiz_choiceD
    return render_template('edit_my_quiz.html', quiz_id=current_quiz_id[0][0], question=current_quiz_question[0][0],
                           A=current_quiz_choiceA[0][0], B=current_quiz_choiceB[0][0], C=current_quiz_choiceC[0][0],
                           D=current_quiz_choiceD[0][0])


@app.route('/edit_quiz_question', methods=['POST', 'GET'])
def edit_quiz_question():
    question = request.form["question"]
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
    write_cmd = f"UPDATE question SET question = '{question}' WHERE question_id=1;"
    conn_non(write_cmd)
    # return view_my_quiz()
    return my_quiz()