from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app_pkg import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    type = db.Column(db.String(20), index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"<User: {self.username}, Email: {self.email}, User Type: {self.type}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), index=True)
    pin = db.Column(db.String(64), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Quiz {self.id} with name <<{self.name}>> by Lecturer {self.user_id}>"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    question = db.Column(db.String(255), index=True)
    type = db.Column(db.String(20), index=True)
    choice_a = db.Column(db.String(255), index=True)
    choice_b = db.Column(db.String(255), index=True)
    choice_c = db.Column(db.String(255), index=True)
    choice_d = db.Column(db.String(255), index=True)
    answer = db.Column(db.String(255), index=True)

    def __repr__(self):
        return f"<Question {self.id}: {self.type} type, {self.question}," \
               f"{[self.choice_a, self.choice_b, self.choice_c, self.choice_d]}, answer: {self.answer}> "


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    score = db.Column(db.Integer)
    rank_score = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Mark of {self.score} with score of {self.rank_score} on number {self.quiz_id} quiz for student {self.student_id}>"
