# Dadda-Soft Simple Blog

## Features

- Create Post
- Archive Post & Unarchive (Save as Draft)
- Edit Post
- add Comment
- Delete Comment
- Security (parse html and escape js)
- Authentication System ( Login Register )

## included Libraries

- Bootstrap
- SweetAlert

### dependencies

> Python 3.6+ Check [Python Website](https://python.org)

> mistune (markdown parser) : run **pip install mistune**

> flask : run **pip install flask**

> mysql-connector (driver of mysql) : run **pip install mysql-connector**

post image directory : **Resources/static/posts**

---

## Setup The App

- You should have a mysql-Server installed or install phpmyadmin (Use Xampp That includes all this)
- Create new Database name it As you like

![m](screenshot/create-db.jpg)

- After Select the database you created
  ![alt](screenshot/select-db.jpg)
  click on import click on browse and navigate to the project folder you will find a folder called db inside it there is a SQL file choose it and click go
- after done go back to the project rename the file .env.Example to .env and change database config

![alt](screenshot/env.jpg)

> Note : app Secret Should be in Strong Format and not show it to any one (it's used to hash and encrypt passwords and cookies )

## Start The Server

open a new Terminal and Navigate To The Project Folder and Run
`python server.py`

- python Should be installed and included in system path

# ENJOY IT

### Posts Cards

![text](screenshot/posts-card.jpg)

### Users Posts

![text](screenshot/user-post-card.jpg)

### follow me

[facebook](https://fb.com/daddasoft)
[instagram](https://instagram.com/daddasoft)
[Twitter](https://twitter.com/daddasoft)
