from flask import Flask,request,render_template
from flask_mysqldb import MySQL
import re

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'etdb.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'etdb'
app.config['MYSQL_PASSWORD'] = 'Lkjhg098'
app.config['MYSQL_DB'] = 'etdb'

app = Flask(__name__)
mysql=MySQL(app)

@app.route("/home")
def home():
    return render_template("homepage.html")

@app.route("/")
def add():
    return render_template("home.html")
@app.route("/signup")
def signup():
    return render_template("signup.html")   

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM register WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO register VALUES ( % s, % s, % s)', (username, email,password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('signup.html', msg = msg)
        
        
if __name__ == "__main__":
    app.run(debug=True)