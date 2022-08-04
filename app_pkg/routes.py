from flask import render_template

from app_pkg import app


# import config

# app = Flask(__name__)
# app.config.from_object(config)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('signup.html')

# @app.route('/quizlist', methods=['POST', 'GET'])
# def quizlist():
#     return render_template('quizlist.html')

@app.route('/quizstudent', methods=['POST', 'GET'])
def quizlist():
    return render_template('quizstudent.html')
