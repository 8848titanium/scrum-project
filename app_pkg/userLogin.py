from app_pkg.conndb import conndb


class userLogin:
    def __init__(self):
        pass

    # check the given email is existing or not
    def check_exist(self, email):
        self.email = email
        string1 = "select student_email from student;"
        student_email = conndb().conn_mul(string1)
        print(student_email)
        string2 = "select lecturer_email from lecturer;"
        lecturer_email = conndb().conn_mul(string2)
        if student_email is None and lecturer_email is None:
            return False
        else:
            for i in student_email:
                if self.email == str(i[0]):
                    return True
            for i in lecturer_email:
                if self.email == str(i[0]):
                    return True

    def check_type(self, email):
        self.email = email
        string1 = "select student_email from student;"
        student_email = conndb().conn_mul(string1)
        string2 = "select lecturer_email from lecturer;"
        lecturer_email = conndb().conn_mul(string2)
        for i in student_email:
            if self.email == str(i[0]):
                return True
        for j in lecturer_email:
            if self.email == str(j[0]):
                return False

    # student login
    def student_login(self, email, password):
        self.email = email
        self.password = password
        string = "select * from student where student_email = '%s'" % self.email
        res = conndb().conn_one(string)
        if res[2] == self.password:
            return res
        else:
            return -1

    # lecturer login
    def lecturer_login(self, email, password):
        self.email = email
        self.password = password
        string = "select * from lecturer where lecturer_email = '%s'" % self.email
        res = conndb().conn_one(string)
        if res[2] == self.password:
            return res
        else:
            return -1

    def user_signup(self, name, password, email, user_type):
        self.name = name
        self.password = password
        self.email = email
        self.user_type = user_type
        if user_type == "student":
            string1 = "insert into student values(null,'%s','%s','%s') " % (self.name, self.password, self.email)
            conndb().conn_non(string1)
        else:
            string2 = "insert into lecturer values(null,'%s','%s','%s') " % (self.name, self.password, self.email)
            conndb().conn_non(string2)
