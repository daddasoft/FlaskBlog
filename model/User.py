import mysql.connector
from flask import session
from env import env
from werkzeug.security import generate_password_hash, check_password_hash
try:
    mydb = mysql.connector.connect(
        host=env("host"),
        user=env("user"),
        passwd=env("pass"),
        database=env("database")
    )
except:
    print("Error Will Connecting To Database")
    exit()


def CheckAvaliableField(field, value="", column="userID", table="user", condition=""):
    mycursor = mydb.cursor()
    sql = "SELECT "+column+" FROM "+table + \
        " where "+field+" = %s "+condition+" LIMIT 1"
    params = (value, )
    mycursor.execute(sql, params)
    mycursor.fetchall()
    res = mycursor.rowcount
    mydb.commit()
    return res


def AddUser(name, username, password, email):
    mycursor = mydb.cursor()
    sql = "INSERT INTO `user`(`name`, `username`, `email`, `password`,`createdAt`) \
     VALUES (%s,%s,%s,%s,CURRENT_TIMESTAMP())"
    password = generate_password_hash(password, "sha256")
    params = (name.strip(), username.strip().replace(' ', '_'),
              email.strip(), password.strip())
    mycursor.execute(sql, params)
    mydb.commit()
    session["id"] = mycursor.lastrowid
    session["user"] = username
    if(mycursor.rowcount > 0):
        return True
    return False


def logUser(username, password):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM user WHERE username = %s or email = %s"
    params = (username.strip(), username.strip())
    mycursor.execute(sql, params)
    res = mycursor.fetchone()
    mydb.commit()
    if(mycursor.rowcount > 0):
        # chexk pass
        if(check_password_hash(res[4], password)):
            session["user"] = res[2]
            session["id"] = res[0]
            return {"status": True}
        else:
            return {"status": False, "msg": "password not correct"}
    else:
        return {"status": False, "msg": "username or email not correct"}


def isLog():
    if(session["user"]):
        return True
    return False


def userInfo(username):
    mycursor = mydb.cursor()
    query = "SELECT postTitle,postBody,imagePath,u.name,u.email,  \
    (SELECT Count(*) FROM posts WHERE createdBy = u.userID) as postCount, \
    (SELECT count(*) from comments c WHERE c.byUser = u.userID) as countCommenr  \
    ,u.createdAt FROM posts p right JOIN user u on u.userID = p.createdBy \
     where u.username =%s"
    params = (username, )
    mycursor.execute(query, params)
    res = mycursor.fetchall()
    mydb.commit()
    return res
