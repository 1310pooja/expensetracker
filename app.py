# -- coding: utf-8 --


from flask import Flask, render_template, request, redirect, session 
import sqlite3
import re


app = Flask(__name__)


app.secret_key = 'a'


# Connect to SQLite database
conn = sqlite3.connect('etdb.db')
cursor = conn.cursor()

# Create a table if not exists for user registration
cursor.execute('''CREATE TABLE IF NOT EXISTS register (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    email TEXT,
                    password TEXT)''')

# Create a table if not exists for expenses
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT,
                    date TEXT,
                    expensename TEXT,
                    amount REAL,
                    paymode TEXT,
                    category TEXT)''')

conn.commit()
conn.close()


#HOME--PAGE
@app.route("/home")
def home():
    return render_template("homepage.html")

@app.route("/")
def add():
    return render_template("home.html")

#SIGN--UP--OR--REGISTER
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
        
        conn = sqlite3.connect('etdb.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM register WHERE username = ?', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Name must contain only characters and numbers!'
        else:
            cursor.execute('INSERT INTO register (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            msg = 'You have successfully registered!'
            return render_template('signup.html', msg=msg)
        
        conn.close()
 
#LOGIN--PAGE    
@app.route("/signin")
def signin():
    return render_template("login.html")
        
@app.route('/login',methods =['POST'])
def login():
    msg = ''
   
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('etdb.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM register WHERE username = ? AND password = ?', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['email'] = account[2]
            session['username'] = account[1]
           
            return redirect('/home')
        else:
            msg = 'Incorrect username / password !'
        
        conn.close()

    return render_template('login.html', msg=msg)

#ADDING----DATA
@app.route("/add")
def adding():
    return render_template('add.html')

@app.route('/addexpense', methods=['POST'])
def addexpense():
    email = session['email']
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    paymode = request.form['paymode']
    category = request.form['category']
    
    conn = sqlite3.connect('etdb.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO expenses (email, date, expensename, amount, paymode, category) VALUES (?, ?, ?, ?, ?, ?)',
                   (email, date, expensename, amount, paymode, category))
    conn.commit()
    conn.close()

    return redirect("/display")

#DISPLAY---graph 
@app.route("/display")
def display():
    email = session['email']
    
    conn = sqlite3.connect('etdb.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM expenses WHERE email = ? ORDER BY date DESC', (email,))
    expense = cursor.fetchall()
    cursor.execute('SELECT category, SUM(amount) as total_amount FROM expenses GROUP BY category')
    sums = cursor.fetchall()
    
    conn.close()

    return render_template('display.html', expense=expense, sum=sums)

#delete---the--data
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = sqlite3.connect('etdb.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect("/display")

#UPDATE---DATA
@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    conn = sqlite3.connect('etdb.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM expenses WHERE id = ?', (id,))
    row = cursor.fetchall()
    conn.close()

    return render_template('edit.html', expenses=row[0])

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        date = request.form['date']
        expensename = request.form['expensename']
        amount = request.form['amount']
        paymode = request.form['paymode']
        category = request.form['category']
    
        conn = sqlite3.connect('etdb.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE expenses SET date = ?, expensename = ?, amount = ?, paymode = ?, category = ? WHERE id = ?",
                       (date, expensename, amount, paymode, category, id))
        conn.commit()
        conn.close()

        return redirect("/display")

#log-out
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('username', None)
    return render_template('home.html')

if __name__== "__main__":
     app.run(debug=True)
