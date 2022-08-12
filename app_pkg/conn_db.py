import pymysql


# function used to connect database, will return 1 row of data
def conn_one(string):
    con = pymysql.connect(host='localhost', user='a3', password='123456', database='happylearning')
    cur = con.cursor()
    cur.execute(string)
    res = cur.fetchone()
    cur.close()
    con.close()
    return res


# function used to connect database, will return several rows of data
def conn_mul(string):
    con = pymysql.connect(host='localhost', user='a3', password='123456', database='happylearning')
    cur = con.cursor()
    cur.execute(string)
    res = cur.fetchall()
    cur.connection.commit()
    cur.close()
    con.close()
    return res


# function used to connect database, doesn't have return value
def conn_non(string):
    con = pymysql.connect(host='localhost', user='a3', password='123456', database='happylearning')
    cur = con.cursor()
    cur.execute(string)
    cur.connection.commit()
    cur.close()
    con.close()
