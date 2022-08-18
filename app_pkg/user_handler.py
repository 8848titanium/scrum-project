import random
import string

from app_pkg.conn_db import *

PIN_LENGTH = 6


class User:
    def __init__(self, email="", user_name="", password="", user_type="", user_id=""):
        self.email = email
        self.user_name = user_name
        self.password = password
        self.user_type = user_type
        self.user_id = user_id

    # check the given email is existing or not
    def check_exist(self):
        user_type = self.check_type()
        if user_type is not None:
            self.user_type = "student" if user_type else "lecturer"
            return True
        else:
            return False

    def check_type(self):
        string1 = "select student_email from student;"
        student_email = conn_mul(string1)
        string2 = "select lecturer_email from lecturer;"
        lecturer_email = conn_mul(string2)
        for i in student_email:
            if self.email == str(i[0]):
                return True
        for j in lecturer_email:
            if self.email == str(j[0]):
                return False
        return None

    def login(self):
        if self.check_type():
            string = "select * from student where student_email = '%s'" % self.email
        else:
            string = "select * from lecturer where lecturer_email = '%s'" % self.email
        res = conn_one(string)
        return res if res[2] == self.password else None

    def signup(self):
        if self.check_type():
            string1 = "insert into student values(null,'%s','%s','%s') " % (self.user_name, self.password, self.email)
            conn_non(string1)
        else:
            string2 = "insert into lecturer values(null,'%s','%s','%s') " % (self.user_name, self.password, self.email)
            conn_non(string2)


class Quiz:
    def __init__(self, lecturer_id=None, quiz_id=None):
        self.lecturer_id = lecturer_id
        self.question_set = []
        if not quiz_id:
            self.quiz_id = conn_one("SELECT COUNT(*) FROM quiz;")[0] + 1
            self.quiz_PIN = ''.join(random.choice(string.digits) for i in range(PIN_LENGTH))
            write_cmd = "INSERT INTO quiz VALUES('%s', '%s', '%s')" % (self.quiz_id, self.lecturer_id, self.quiz_PIN)
            conn_non(write_cmd)
        else:
            self.quiz_id = quiz_id
        # self.quiz_attendant = quiz_attendant

    def __repr__(self):
        return str({self.lecturer_id: {self.quiz_id: [self.quiz_PIN, self.question_set]}})

    def __str__(self):
        return f"lecturer id - {self.lecturer_id}, quiz id - {self.quiz_id}, PIN - {self.quiz_PIN}, question set - {self.question_set}"

    def add_question(self, question, category, choices, answer):
        question_id = conn_one("SELECT COUNT(*) FROM question;")[0] + 1
        a, b, c, d = choices
        write_cmd = "INSERT INTO question VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
            question_id, self.quiz_id, question, category, a, b, c, d, answer)
        conn_non(write_cmd)
        self.question_set.append(question_id)


def load_questions(quiz_id):
    query_result = conn_mul("SELECT * FROM question WHERE quiz_id = '%s'" % quiz_id)
    return [{"question_id": row[0], "question": row[2], "category": row[3], "choices": row[4:8], "answer": row[-1]}
            for row in query_result]  # list comprehension


def launch_quiz(pin):
    query_result = conn_one("SELECT * FROM quiz WhERE quiz_PIN = '%s'" % pin)
    if query_result:
        quiz_id = query_result[0]
        return load_questions(quiz_id)
    else:
        return None


"""Demo"""
# quiz = Quiz(1)  # add a new quiz by declaring the lecturer_id
# print(quiz)
# quiz.add_question("hello?", 0, ['dasd', 'gefv', 'bfdsb', 'h6tuyn'], 'B')
# quiz.add_question("hello??", 1, ['dasd', 'gefv', 'bfdsb', 'h6tuyn'], 'BC')
# quiz.add_question("Please fill__", 0, ['dasd', 'gefv', 'bfdsb', 'h6tuyn'], 'Filled')
# print(quiz)
#
# old_quiz = Quiz(quiz_id=4)  # load exist quiz by declaring quiz_id with keyword argument
# print(old_quiz.load_questions())
