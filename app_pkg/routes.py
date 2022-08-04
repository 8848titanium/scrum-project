from flask import render_template

from app_pkg import app


# import config

# app = Flask(__name__)
# app.config.from_object(config)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about', methods=['POST', 'GET'])
def quizlist():
    return render_template('about.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


@app.route('/login_check', methods=['POST', 'GET'])
def login_check():
    user_name = request.form['username']
    password = request.form['password']
    if password == '' or user_name == '':
        return render_template('login.html')
    else:
        return 


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('signup.html')


@app.route('/quizstudent', methods=['POST', 'GET'])
def quizlist():
    return render_template('quizstudent.html')
