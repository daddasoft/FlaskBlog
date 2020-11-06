import mysql.connector
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="dadda",
        database="myblog"
    )
except:
    print("Error Will Connecting To Database")
    exit()


def allPosts(page=1):
    mycursor = mydb.cursor()
    OFFSET = abs(5 * (int(page)-1))
    mycursor.execute(f"SELECT p.imagePath,p.postTitle,p.postBody,u.name,u.username \
  ,(SELECT Count(*) from posts WHERE isArchived = 0) as pcount ,(SELECT Count(*) from comments c WHERE c.forPost = p.postID) as \
    commentCount,p.createdAt from posts p join user u on p.createdBy = u.userID   \
     WHERE p.isArchived = 0   \
     ORDER BY createdAt DESC LIMIT 5 OFFSET {OFFSET} ")
    res = mycursor.fetchall()
    mydb.commit()
    return res


def singlePost(slug):
    mycursor2 = mydb.cursor()
    sql = "SELECT imagePath , postTitle,postBody,postID FROM `posts` WHERE `posts`.`postSlug`= %s Or postID = %s  LIMIT 1;"
    params = (str(slug), str(slug))
    mycursor2.execute(sql, params)
    res = mycursor2.fetchone()
    mydb.commit()
    if(mycursor2.rowcount > 0):
        return res
    return res


def getPostToEdit(id, userID):
    mycursor2 = mydb.cursor()
    sql = "SELECT imagePath , postTitle,postBody,isArchived,tags FROM `posts` WHERE `posts`.`postID`= %s AND createdBy= %s LIMIT 1;"
    params = (id, userID)
    mycursor2.execute(sql, params)
    res = mycursor2.fetchone()
    mydb.commit()
    if(mycursor2.rowcount > 0):
        return res
    return res


def AddPost(title, imagePath, postBody, tags, createdBy):
    mycursor = mydb.cursor()
    slug = title.replace(' ', '-')
    sql = "INSERT INTO `posts`( `postTitle`, `postSlug`, `imagePath`, `postBody`, `tags`, `createdBy`, `createdAt`, `updatedAt`)  \
    VALUES (%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP())"
    params = (str(title), str(slug.lower()), str(
        imagePath), str(postBody), str(tags), str(createdBy))
    mycursor.execute(sql, params)
    mydb.commit()

    if(mycursor.rowcount > 0):
        return "Inserted"
    return "None"


def UserPost(userid):
    mycursor = mydb.cursor()
    sql = "SELECT p.imagePath,p.postTitle,p.postBody,p.postID,p.isArchived  from posts p where  \
    p.createdBy = %s ORDER BY createdAt DESC"
    params = (userid,)
    mycursor.execute(sql, params)
    res = mycursor.fetchall()
    mydb.commit()
    return res


def UserPostArchive(userid):
    mycursor = mydb.cursor()
    sql = "SELECT p.imagePath,p.postTitle,p.postBody,p.postID,p.isArchived  from posts p where  \
    p.createdBy = %s  AND p.isArchived = 1 ORDER BY createdAt DESC"
    params = (userid,)
    mycursor.execute(sql, params)
    res = mycursor.fetchall()
    mydb.commit()
    return res


def UpdatePost(PostID, body, title, tags, image, isArchived, userID):
    mycursor = mydb.cursor()
    slug = title.replace(' ', '-')
    if image == '':
        sql = "UPDATE `posts` SET `postTitle`= %s,`postSlug`= %s \
        ,`imagePath`= imagePath,`postBody`= %s,`isArchived`=%s,`tags`=%s,`updatedAt`=CURRENT_TIMESTAMP() \
            WHERE postID = %s AND createdBy = %s"
        params = (title, slug, body, isArchived, tags, PostID, userID)
        mycursor.execute(sql, params)
    else:
        sql = "UPDATE `posts` SET `postTitle`= %s,`postSlug`= %s \
        ,`imagePath`= %s,`postBody`= %s,`isArchived`=%s,`tags`=%s,`updatedAt`=CURRENT_TIMESTAMP() \
            WHERE postID = %s AND createdBy = %s "
        params = (title, slug, "img/"+image, body,
                  isArchived, tags, PostID, userID)
        mycursor.execute(sql, params)
    mydb.commit()
    if(mycursor.rowcount > 0):
        return True
    return False


def DeletePost(PostID, userid):
    mycursor = mydb.cursor()
    sql = "DELETE  FROM  posts  where postID = %s AND createdBy = %s"
    params = (PostID, userid,)
    mycursor.execute(sql, params)
    mydb.commit()
    if(mycursor.rowcount > 0):
        return True
    return False


def ArchivePost(PostID, userid, val):
    mycursor = mydb.cursor()
    sql = "UPDATE posts SET isArchived = %s WHERE postID = %s AND createdBy =%s"
    params = (val, PostID, userid,)
    mycursor.execute(sql, params)
    mydb.commit()
    if(mycursor.rowcount > 0):
        return True
    return False


def getComments(postSlug):
    mycursor = mydb.cursor()
    sql = "SELECT u.username, \
    c.commentBody ,c.byUser,c.commentID FROM posts p join comments c on  \
    p.postID = c.forPost join user u on u.userID = c.byUser \
        WHERE p.postSlug = %s"
    params = (postSlug.strip(),)
    mycursor.execute(sql, params)
    res = mycursor.fetchall()
    mydb.commit()
    return res


def addComment(commentBody, PostID, userid):
    mycursor = mydb.cursor()
    sql = "INSERT INTO `comments`(`commentBody`, `forPost`, `byUser`, `createdAt`, `updatedAt`) \
    VALUES (%s,%s,%s,CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP())"
    params = (commentBody, PostID, userid,)
    mycursor.execute(sql, params)
    mydb.commit()
    if(mycursor.rowcount > 0):
        return True
    return False


def DeleteComment(commentID, userid):
    mycursor = mydb.cursor()
    sql = "DELETE  FROM  comments  where commentID = %s AND byUser = %s"
    params = (commentID, userid,)
    mycursor.execute(sql, params)
    mydb.commit()
    if(mycursor.rowcount > 0):
        return True
    return False
