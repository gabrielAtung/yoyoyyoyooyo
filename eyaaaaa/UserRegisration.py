from flask import Flask, redirect, render_template, request, url_for
import sqlite3

app = Flask(__name__)

@app.route('/success/<name>', methods=['GET'] )
def success(name):
    return 'Proses data user : %s berhasil' % name

@app.route('/userlist')
def userList():
    users = getAllUser()
    print(users)
    return render_template('userlist.html', title='Daftar User', listuser=users)

@app.route('/')
def login_page():
    return render_template('loginform.html')

@app.route('/register')
def register_page():
    return render_template('registerUser.html')

@app.route("/login", methods=['POST']) 
def login():
    username = request.form['username']
    password = request.form['password']

    connection = sqlite3.connect("user.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT username FROM user WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cursor.fetchone()
    connection.close()

    if user:
        return redirect(url_for('success', name=username))
    else:
        return "Login gagal! Username atau password salah"

@app.route("/registeruser", methods=['POST']) 
def registeruser():
    realname = request.form['realname']
    pob = request.form['pob']
    username = request.form['username']
    password = request.form['password']

    connection = sqlite3.connect("user.db")
    cursor = connection.cursor()

    # cek apakah username sudah ada
    cursor.execute(
        "SELECT username FROM user WHERE username = ?",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        connection.close()
        return "Username sudah terdaftar!"

    cursor.execute(
        "INSERT INTO user (realname, pob, username, password) VALUES (?, ?, ?, ?)",
        (realname, pob, username, password)
    )

    connection.commit()
    connection.close()

    return redirect(url_for('success', name=username))    

def getAllUser():
    # Open database connection
    connection = sqlite3.connect("user.db")
    cursor = connection.cursor()
    # Execute the query
    cursor.execute("SELECT realname, pob, username, password FROM user;")    

    # convert it into dictionary
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))  
        for row in cursor.fetchall()]
    # Close the connection
    connection.close()
    return data

if __name__ == '__main__':
    app.run()
