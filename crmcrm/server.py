from flask import Flask, session, render_template, redirect, request, url_for
from flaskext.mysql import MySQL
import pyautogui
 
mysql = MySQL()
app = Flask(__name__)
 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = "ABCDEFG"
mysql.init_app(app)
 
@app.route('/', methods=['GET', 'POST'])
def main():
    error = None
 
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
 
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT id FROM user_info WHERE id = %s AND pw = %s"
        value = (id, pw)
        cursor.execute("set names utf8")
        cursor.execute(sql, value)
 
        data = cursor.fetchall()
        cursor.close()
        conn.close()
 
        for row in data:
            data = row[0]
 
        if data:
            session['login_user'] = id
            return redirect(url_for('home'))
        else:
            pyautogui.alert("errorrrrr")
            error = 'invalid input data detected !'
    return render_template('main.html', error = error)
 
 
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        id = request.form['regi_id']
        pw = request.form['regi_pw']
 
        conn = mysql.connect()
        cursor = conn.cursor()
 
        sql = "INSERT INTO user_info VALUES ('%s', '%s')" % (id, pw)
        cursor.execute(sql)
 
        data = cursor.fetchall()
 
        if not data:
            conn.commit()
            return redirect(url_for('main'))
        else:
            conn.rollback()
            return "Register Failed"
 
        cursor.close()
        conn.close()
    return render_template('register.html', error=error)
 
@app.route('/home.html', methods=['GET', 'POST'])
def home():
    error = None
    id = session['login_user']
    return render_template('/home.html', error=error, name=id)
 
if __name__ == '__main__':
    app.run()
