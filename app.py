import json, sqlite3, functools, os, hashlib,time, random, sys, hmac
from flask import Flask, current_app, g, session, redirect, render_template, url_for, request




### DATABASE FUNCTIONS ###

def connect_db():
    return sqlite3.connect(app.database)

def init_db():
    """Initializes the database with our great SQL schema"""
    conn = connect_db()
    db = conn.cursor()
    db.executescript("""

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS notes;

CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assocUser INTEGER NOT NULL,
    dateWritten DATETIME NOT NULL,
    note TEXT NOT NULL,
    publicID INTEGER NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    salt TEXT NOT NULL
);

INSERT INTO notes VALUES(null,2,"1993-09-23 10:10:10","hello my friend",1234567890);
INSERT INTO notes VALUES(null,2,"1993-09-23 12:10:10","i want lunch pls",1234567891);

""")
    salt, password_hash = gen_password_hash("qweasdzxc")
    db.execute("INSERT INTO users(id, username, password, salt) VALUES(null, ?, ?, ?);", ("admin", password_hash, salt))
    salt, password_hash = gen_password_hash("omgMPC")
    db.execute("INSERT INTO users(id, username, password, salt) VALUES(null, ?, ?, ?);", ("bernardo", password_hash, salt))
    conn.commit()
    conn.close()

def gen_password_hash(password: str, salt: str = ""):
    if not salt: salt=os.urandom(15).hex()
    password_hash=hashlib.sha256(str.encode(password+salt)).hexdigest()
    return salt, password_hash

def compare_password(expected: str, actual: str, salt: str):
    _, actual_hash = gen_password_hash(actual, salt)
    return actual_hash == expected

### APPLICATION SETUP ###
app = Flask(__name__)
app.database = "db.sqlite3"
app.secret_key = os.urandom(32)

### ADMINISTRATOR'S PANEL ###
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return redirect(url_for('notes'))


@app.route("/notes/", methods=('GET', 'POST'))
@login_required
def notes():
    importerror=""
    #Posting a new note:
    if request.method == 'POST':
        if request.form['submit_button'] == 'add note':
            note = request.form['noteinput']
            db = connect_db()
            c = db.cursor()
            c.execute(
                """INSERT INTO notes(id, assocUser, dateWritten, note, publicID) VALUES(null, ?, ?, ?, ?);""",
                (session['userid'], time.strftime('%Y-%m-%d %H:%M:%S'), note, random.randrange(1000000000, 9999999999))
            )
            db.commit()
            db.close()
        elif request.form['submit_button'] == 'import note':
            noteid = request.form['noteid']
            db = connect_db()
            c = db.cursor()
            c.execute("SELECT * from NOTES where publicID = ?", (noteid,))
            result = c.fetchone()
            if result:
                c.execute(
                    """INSERT INTO notes(id, assocUser, dateWritten, note, publicID) VALUES(null, ?, ?, ?, ?);""",
                    (session['userid'], result[2], result[3], result[4])
                )
            else:
                importerror="No such note with that ID!"
            db.commit()
            db.close()
    
    db = connect_db()
    c = db.cursor()
    c.execute("SELECT * FROM notes WHERE assocUser = ?;", (session['userid'],))
    notes = c.fetchall()
    
    return render_template('notes.html',notes=notes,importerror=importerror)


@app.route("/login/", methods=('GET', 'POST'))
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = connect_db()
        c = db.cursor()
        c.execute("SELECT id, username, password, salt FROM users WHERE username = ?", (username, ))
        result = c.fetchone()
        if result and compare_password(result[2], password, result[3]):
            session.clear()
            session['logged_in'] = True
            session['userid'] = result[0]
            session['username']=result[1]
            return redirect(url_for('index'))
        else:
            error = "Wrong username or password! Please contact admin if in trouble!"
    return render_template('login.html',error=error)


@app.route("/register/", methods=('GET', 'POST'))
def register():
    errored = False
    usererror = ""
    passworderror = ""
    if request.method == 'POST':
        

        username = request.form['username']
        password = request.form['password']
        db = connect_db()
        c = db.cursor()

        #Check if the length of the password and username is at least one.
        if(len(username) <= 0 or len(password) <= 0):
            errored = True
            usererror = "Username and Password must have a length of at least 1!"

        #Check if username already exists.
        c.execute("SELECT * FROM users WHERE username = ?;", (username,))
        if c.fetchone():
            errored = True
            usererror = "That username is already in use by someone else!"

        if(not errored):
            salt, password_hash = gen_password_hash(password)
            c.execute("INSERT INTO users(id, username, password, salt) VALUES(null, ?, ?, ?);", (username, password_hash, salt))
            db.commit()
            db.close()
            return f"""<html>
                        <head>
                            <meta http-equiv="refresh" content="2;url=/" />
                        </head>
                        <body>
                            <h1>SUCCESS!!! Redirecting in 2 seconds...</h1>
                        </body>
                        </html>
                        """
        
        db.commit()
        db.close()
    return render_template('register.html',usererror=usererror,passworderror=passworderror)


@app.route("/logout/")
@login_required
def logout():
    """Logout: clears the session"""
    session.clear()
    return redirect(url_for('index'))

with app.app_context():
    if not os.path.exists(app.database):
        init_db()
if __name__ == "__main__":
    #create database if it doesn't exist yet
    if not os.path.exists(app.database):
        init_db()
    runport = 5000
    if(len(sys.argv)==2):
        runport = int(sys.argv[1])  #Here the port is casted as an int, to make sure it is nothing else.
    try:
        app.run(host='0.0.0.0', port=runport) # runs on machine ip address to make it visible on netowrk
    except:
        print("Something went wrong. the usage of the server is either")
        print("'python3 app.py' (to start on port 5000)")
        print("or")
        print("'sudo python3 app.py 80' (to run on any other port)")
