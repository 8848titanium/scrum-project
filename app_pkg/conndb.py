import pymysql


class conndb:
    def __init__(self):
        pass

    # function used to connect database, will return 1 row of data
    def conn_one(self, string):
        self.string = string
        con = pymysql.connect(host='localhost', user='a3', password='123456', database='happylearning')
        cur = con.cursor()
        cur.execute(self.string)
        res = cur.fetchone()
        cur.close()
        con.close()
        return res

    # function used to connect database, will return several rows of data
    def conn_mul(self, string):
        self.string = string
        con = pymysql.connect(host='localhost', user='a3', password='123456', database='happylearning')
        cur = con.cursor()
        cur.execute(self.string)
        res = cur.fetchall()
        cur.connection.commit()
        cur.close()
        con.close()
        return res

    # function used to connect database, doesn't have return value
    def conn_non(self, string):
        self.string = string
        con = pymysql.connect(host='localhost', user='a3', password='123456', database='happylearning')
        cur = con.cursor()
        cur.execute(self.string)
        cur.connection.commit()
        cur.close()
        con.close()
