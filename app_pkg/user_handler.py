from app_pkg.conn_db import *


class User:
    def __init__(self, email=None, user_name=None, password=None, user_type=None, user_id=None):
        self.email = email
        self.user_name = user_name
        self.password = password
        self.user_type = user_type
        self.user_id = user_id

    # check the given email is existing or not
    def check_exist(self):
        string1 = "select student_email from student;"
        student_email = conn_mul(string1)
        string2 = "select lecturer_email from lecturer;"
        lecturer_email = conn_mul(string2)
        if student_email is None and lecturer_email is None:
            return False
        else:
            for i in student_email:
                if self.email == str(i[0]):
                    return True
            for i in lecturer_email:
                if self.email == str(i[0]):
                    return True

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

    def login(self):
        if self.user_type == "student":
            string = "select * from student where student_email = '%s'" % self.email
        else:
            string = "select * from lecturer where lecturer_email = '%s'" % self.email
        res = conn_one(string)
        return res if res[2] == self.password else None

    def signup(self):
        if self.user_type == "student":
            string1 = "insert into student values(null,'%s','%s','%s') " % (self.user_name, self.password, self.email)
            conn_non(string1)
        else:
            string2 = "insert into lecturer values(null,'%s','%s','%s') " % (self.user_name, self.password, self.email)
            conn_non(string2)
