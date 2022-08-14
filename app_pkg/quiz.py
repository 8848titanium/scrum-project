import random
import string

from app_pkg.conn_db import *

PIN_LENGTH = 8


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

    def load_questions(self):
        query_result = conn_mul("SELECT * FROM question WHERE quiz_id = '%s'" % self.quiz_id)
        return [{"question_id": row[0], "question": row[2], "category": row[3], "choices": row[4:8], "answer": row[-1]}
                for row in query_result]


"""Demo"""
quiz = Quiz(1)  # add a new quiz by declaring the lecturer_id
print(quiz)
quiz.add_question("hello?", 0, ['dasd', 'gefv', 'bfdsb', 'h6tuyn'], 'B')
quiz.add_question("hello??", 1, ['dasd', 'gefv', 'bfdsb', 'h6tuyn'], 'BC')
quiz.add_question("Please fill__", 0, ['dasd', 'gefv', 'bfdsb', 'h6tuyn'], 'Filled')
print(quiz)

old_quiz = Quiz(quiz_id=4)  # load exist quiz by declaring quiz_id with keyword argument
print(old_quiz.load_questions())
