from app_pkg.conn_db import *
import random

PIN_LENGTH = 8
MINIMUM = 0
MAXIMUM = 9

class Quiz:
    def __init__(self, lecturer_id=None, quiz_id=None, quiz_PIN=None):
        self.lecturer_id = lecturer_id
        # self.quiz_attendant = quiz_attendant
        self.quiz_id = quiz_id
        self.quiz_PIN = quiz_PIN
        self.questions = []

    def create(self):
        self.lecturer_id = "TestUser_id"  # need to change after class finished
        self.quiz_PIN = ""
        for i in range(PIN_LENGTH):
            number = random.randint(MINIMUM, MAXIMUM)
            self.quiz_PIN += str(number)
        # self.quiz_id = int(max(happylearning.quiz.quiz_id)) + 1  # 这里俺不知道怎么弄嘞，只能demo一个最大id+1的placeholder

    # def add_question(self):做不动了，解构俺也不太确定，晚上再继续
    #     if is


    def __str__(self):
        return f"quiz id - {self.quiz_id}, quiz PIN - {self.quiz_PIN}, quiz creator - {self.lecturer_id}"

"""Test"""
new_quiz = Quiz()
Quiz.create(new_quiz)
print(new_quiz)
