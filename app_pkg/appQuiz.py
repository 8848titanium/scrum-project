from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
#

app = Flask(__name__)
app.config['SECRET'] = "secret!123"
socketio = SocketIO(app, cors_allowed_origins="*")

active_users = []
question_1 = {"Question": "Q1:How are you?", "A": "Good", "B": "Not Bad", "C": "Fine", "D": "OK", "Answer": "A"}
question_2 = {"Question": "Q2:Is this Q2?", "A": "Yes", "B": "No", "C": "Not Sure", "D": "Sure No", "Answer": "A"}
question_list = [question_1, question_2]


@app.route('/')
def index():
    return render_template('indexQuizLecturer.html')


@socketio.on('message')
def handle_message(message):
    print("Received message:" + message)
    if message != "User connected!":
        send(message, broadcast=True)
    # if message == "Display question":
    #     send(question_list, broadcast=True)
    # send(data)  # send message received to the connected client - push to client on event message
    # # send message on FE - to the @socketio.on('message')


@socketio.event
def display_question():
    emit("display question", question_1, broadcast=True)


@socketio.on('ask for question')
def ask_for_question():
    current_question = question_1
    question = current_question.get("Question")
    choice_a = current_question.get("A")
    choice_b = current_question.get("B")
    choice_c = current_question.get("C")
    choice_d = current_question.get("D")
    answer = current_question.get("Answer")
    emit("display question", (question, choice_a, choice_b, choice_c, choice_d, answer), broadcast=True)

# @socketio.on('chosen_answer')
# def chosen_answer(answer):
#     # question_list.remove(question_list[0])
#     emit('Answer chosen', answer, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)

