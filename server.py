from flask import Flask, make_response, Response, render_template, jsonify, request, redirect, url_for, flash, escape
from model.Post import DeleteComment, addComment, allPosts, getComments, singlePost, ArchivePost, UpdatePost, AddPost, UserPost, DeletePost, getPostToEdit, UserPostArchive
from model.User import CheckAvaliableField, userInfo, AddUser, logUser, isLog, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from Random import RandomString
from math import ceil
import mistune
from env import env
from re import sub
from flask_cors import CORS
todoApp = Flask(__name__, static_folder="Resources/static")
todoApp.config['SECRET_KEY'] = env("appSecret")

CORS(todoApp)


@todoApp.route('/')
def index():
    req = request.args.get("page") or 1
    if (int(req) <= 0):
        req = 1
    posts = allPosts(req)
    if(len(posts) < 1):
        countPost = 0
    else:
        countPost = posts[0][5]
    pagenum = ceil(float(countPost / 5))
    return render_template("app/index.html",title="My B Blog", page=int(req), lenPost=len(posts), pageCount=int(pagenum), posts=posts)


@todoApp.route('/about')
def about():
    return render_template("layout/app.html", title="about")


@todoApp.route('/auth/login')
def login():
    if("user" in session):
        return redirect(url_for('index'))
    return render_template("Auth/login.html", title="login", old=(" ",))


@todoApp.route('/auth/login', methods=['POST'])
def Auth():
    if("user" in session):
        return redirect(url_for('index'))
    username = request.form['username'] or " "
    password = request.form['password'] or " "
    user = logUser(username, password)
    if(user["status"]):
        return redirect(url_for('index'))
    return render_template("Auth/login.html",title="login", user=user, old=(username,))


@todoApp.route('/auth/register')
def register():
    if("user" in session):
        return redirect(url_for('index'))
    return render_template("Auth/register.html",title="Register", old=("", "", ""))


@ todoApp.route('/auth/register', methods=['POST'])
def addNewUser():
    if("user" in session):
        return redirect(url_for('index'))
    formError = {"name": None, "username": None, "email": None,
                 "password": None, "passwordConf": None}
    name = request.form['name'] or " "
    username = request.form['username'] or " "
    email = request.form['email'] or " "
    password = request.form['password'] or " "
    passwordConf = request.form['password-confirm'] or " "
    errors = 0
    username = sub('\s+', '_', username)
    if(len(name) < 5):
        formError["name"] = "Name Should Be At Least 5 Characters"
        errors = 1
    if(len(username) < 5):
        formError["username"] = "username Should Be At Least 5 Characters"
        errors = 1
    elif (CheckAvaliableField('username', username.strip())):
        formError["username"] = "username is Already Taken"
        errors = 1
    if(len(email) < 5):
        formError["email"] = "email Should Be At Least 5 Characters"
        errors = 1
    elif (CheckAvaliableField('email', email.strip())):
        formError["email"] = "email is Already Taken"
        errors = 1
    if(len(password) < 5):
        formError["password"] = "password Should Be At Least 5 Characters"
        errors = 1
    if(passwordConf != password):
        formError["passwordConf"] = "password  Not Matches"
        errors = 1
    old = (name, username, email)
    if(errors == 0):
        AddUser(name, username, password, email)
        flash("Account Created Successfully")
        return redirect(url_for('login'))
    return render_template("Auth/register.html",title="Register", old=old, passwordConfError=formError["passwordConf"], passwordError=formError["password"], emailError=formError["email"], nameError=formError["name"], usernameError=formError["username"])


@ todoApp.route('/post/create')
def createPost():
    if("user" not in session):
        return redirect(url_for('login'))
    return render_template("app/create.html",title="Create New Post", errors="")


@ todoApp.route('/archive')
def archive():
    if("user" not in session):
        return redirect(url_for('login'))
    post = UserPostArchive(session["id"])
    return render_template("app/userPosts.html",title="archived Posts", posts=post, postCount=len(post))


@ todoApp.route('/post/create', methods=['POST'])
def savePost():
    if("user" not in session):
        return redirect(url_for('login'))
    name = ''
    if('file' in request.files):
        f = request.files['file']
    if(f.filename != ''):
        name = session["user"]+RandomString() + "." + f.filename.split('.')[-1]
        f.save("Resources\static\img\\"+secure_filename(name))
    title = request.form['title'].strip()
    tags = request.form['tags'].strip()
    body = request.form['body'].strip()
    body = body.replace('<script>', '').replace('</script>', '')
    errors = {"title": None, "body": None}
    if(CheckAvaliableField(table="posts", field="postTitle", column="postTitle", value=title)):
        errors["title"] = "Title Already Used"
    elif len(title.strip()) > 99:
        errors["title"] = "title At Max Should Have 99 Characters"
    elif len(title.strip()) < 5:
        errors["title"] = "title At Least Should Have 5 Characters"
    elif len(body.strip()) < 10:
        errors["body"] = "Body At Least Should Have 10 Characters"
    else:
        AddPost(title, 'img/'+name, body, tags, session["id"])
        return redirect(url_for('index'))
    return render_template("app/create.html",title="Create New Post", titleError=errors["title"], bodyError=errors["body"], oldbody=body.strip(), oldtitle=title, oldtag=tags)


@ todoApp.route('/post',)
def myPosts():
    if("user" not in session):
        return redirect(url_for('login'))
    post = UserPost(session["id"])
    return render_template("app/userPosts.html",title="My Posts", posts=post, postCount=len(post))


@ todoApp.route('/post/<id>/edit')
def putpost(id):
    if("user" not in session):
        return redirect(url_for('login'))
    res = getPostToEdit(id, session["id"])
    if(not res):
        return render_template("errors/404.html", title="Page Not Found")
    postTitle = res[1]
    postBody = res[2]
    postImage = res[0]
    postIsArchived = res[3]
    postTags = res[4]
    return render_template('app/edit.html', title=postTitle, archive=postIsArchived, body=postBody, image=postImage, tags=postTags)


@ todoApp.route('/post/<id>/edit', methods=['POST'])
def editpost(id):
    if("user" not in session):
        return redirect(url_for('login'))
    if('file' in request.files):
        f = request.files['file']
    if(f.filename != ''):
        name = session["user"]+RandomString() + "."+f.filename.split('.')[-1]
        f.save("Resources\static\img\\"+secure_filename(name))
    else:
        name = ''
    title = request.form['title'].strip()
    tags = request.form['tags'].strip()
    body = request.form['body'].strip()
    if 'archived' in request.form:
        archived = 1
    else:
        archived = 0
    body = body.replace('<script>', '').replace('</script>', '')
    errors = {"title": None, "body": None}
    if(CheckAvaliableField(table="posts", field="postTitle", column="postTitle", value=title, condition="AND postID !="+id)):
        errors["title"] = "Title Already Used"
    elif len(title.strip()) > 99:
        errors["title"] = "title At Max Should Have 99 Characters"
    elif len(title.strip()) < 5:
        errors["title"] = "title At Least Should Have 5 Characters"
    elif len(body.strip()) < 10:
        errors["body"] = "Body At Least Should Have 10 Characters"
    else:
        UpdatePost(id, body, title, tags, name, archived, session["id"])
        return redirect(url_for('index'))
    return render_template('app/edit.html', title=title, archive=archived, body=body, image="", tags=tags, titleError=errors["title"], bodyError=errors["body"])


@ todoApp.route('/post/<id>', methods=["DELETE"])
def deletePost(id):
    if('user' not in session):
        return jsonify({"success": False, "message": "Unauthorized"})
    if(DeletePost(id, session["id"])):
        return jsonify({"success": True, "message": "Post Deleted"})
    return jsonify({"success": False, "message": "Post Not Found Or Not Have Permition To Delete It"})


@ todoApp.route('/<slug>')
def slogy(slug):
    post = singlePost(slug)
    if(not post):
        return render_template("errors/404.html", title="Page Not Found")
    singpost = (post[0], post[1],mistune.markdown(post[2]), post[3])
    return render_template("app/show.html",title=post[1] ,post=singpost, comments=getComments(post[1].replace(' ', '-').lower()), commentErr="")


@ todoApp.route('/logout',)
def logoutGet():
    return redirect(url_for('index'))


@ todoApp.route('/post/comment/<id>', methods=['DELETE'])
def deleteComment(id):
    if('user' not in session):
        return jsonify({"status": False, "message": "Unauthorized"})
    else:
        if(DeleteComment(id, session["id"])):
            return jsonify({"status": True, "message": "Comment Deleted"})
    return jsonify({"status": False, "message": "Comment Can't Be Deleted (Maybe it Not Found Or Don't Have Permission)"})


@ todoApp.route('/post/<id>/comment', methods=['POST'])
def Comment(id):
    errorComment = ''
    comm = ''
    if("user" not in session):
        return redirect(url_for('login'))
    comm = request.form["comment"]
    if len(comm) < 6 or len(comm) > 100:
        errorComment = 'Comment Text Should Be Between 6 And 100 Characters'
    else:
        if(addComment(comm, id, session["id"])):
            return redirect(url_for('slogy', slug=id))
    return f"Writr Comment for post {id}"


@ todoApp.route('/user/<username>',)
def user(username):
    res = userInfo(username)
    if(len(res) == 0):
        return render_template("errors/404.html", title="Page Not Found")
    return render_template('app/user.html', title=username, username=username, data=res)

@ todoApp.route('/logout', methods=['POST'])
def logout():
    session.pop("user", '')
    session.pop("id", '')
    return redirect(url_for('index'))


@ todoApp.route('/uploads', methods=['POST'])
def uploads():
    if('user' not in session):
        return jsonify({"success": False, "message": "Unauthorized"})
    if('file' not in request.files):
        return jsonify({"success": False, "message": "No Image Sent"})
    f = request.files['file'] or ""
    name = RandomString() + f.filename[-4:]
    f.save("Resources\static\posts\\"+secure_filename(name))
    return jsonify({"status": True, "imageLink": "\static\posts\\"+name})


@todoApp.route('/archive/<postid>', methods=['PUT'])
def postArchive(postid):
    if('user' not in session):
        return jsonify({"success": False, "message": "Unauthorized"})
    if(ArchivePost(postid, session["id"], 1)):
        return jsonify({"success": True, "message": "Post Archived"})
    return jsonify({"success": False, "message": "Post Not Found Or You D'ont Have Permission"})


@todoApp.route('/unarchive/<postid>', methods=['PUT'])
def postUnArchive(postid):
    if('user' not in session):
        return jsonify({"success": False, "message": "Unauthorized"})
    if(ArchivePost(postid, session["id"], 0)):
        return jsonify({"success": True, "message": "Post UnArchived"})
    return jsonify({"success": False, "message": "Post Not Found Or You D'ont Have Permission"})


@ todoApp.errorhandler(404)
def Error(error):
    return render_template("errors/404.html", title="Page Not Found")


@ todoApp.errorhandler(405)
def Error(error):
    return render_template("errors/404.html", title="Page Not Found")


if(__name__ == "__main__"):
    todoApp.run(port=5000, debug=True)
