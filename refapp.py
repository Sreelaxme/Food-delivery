#app.py
<!-- <form method="post" action="{{ url_for('all_restaurant') }}">
          <button class="w3-bar-item w3-button" type="submit">Order Now</a> -->
      <!-- </form> -->
<!-- <form action="{{ url_for('login') }}" method = "post"> -->
<!-- </form> -->
from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
 
 
 
 
 
 
 
 
 
 
 @app.route('/deliver', methods=['POST'])
def deliver():
    if request.form.get('delivered'):
        # The "Delivered" button was clicked
        # Perform the appropriate action here
        return redirect(url_for('some_other_view_function'))
    else:
        # The form was submitted, but the "Delivered" button was not clicked
        # Handle this case as appropriate
        pass
 
 
 
 
 
 
 
 
 
app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 
DB_HOST = "localhost"
DB_NAME = "proj"
DB_USER = "proj_admin"
DB_PASS = "password"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 
@app.route('/')
def home():
  
    return render_template('index.html')
    who = request.form['Type']

    

# def home():
#     # Check if user is loggedin
#     if 'loggedin' in session:
    
#         # User is loggedin show them the home page
#         return render_template('index.html', username=session['username'])
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))
 
@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # Fetch one record and return result
        accountUser = cursor.fetchone()

      
        if accountUser:
            password_rs = accountUser['password']
            print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = accountUser['id']
                session['username'] = accountUser['username']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            cursor.execute('SELECT * FROM deliveryBoy_login WHERE username = %s', (username,))
            # Fetch one record and return result
            accountD = cursor.fetchone()
            if accountD:
                password_rs = accountD['password']
                print(password_rs)
            # If account exists in users table in out database
                if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                    session['loggedin'] = True
                    session['id'] = accountD['id']
                    session['username'] = accountD['username']
                    # Redirect to home page
                    return redirect(url_for('home'))
                else:
                # Account doesnt exist or username/password incorrect
                    flash('Incorrect username/password')
            else :
                cursor.execute('SELECT * FROM restaurant_login WHERE username = %s', (username,))
                # Fetch one record and return result
                accountR = cursor.fetchone()
                if accountR:
                    password_rs = accountR['password']
                    print(password_rs)
                # If account exists in users table in out database
                    if check_password_hash(password_rs, password):
                    # Create session data, we can access this data in other routes
                        session['loggedin'] = True
                        session['id'] = accountR['id']
                        session['username'] = accountR['username']
                        # Redirect to home page
                        return redirect(url_for('home'))
                    else:
                    # Account doesnt exist or username/password incorrect
                        flash('Incorrect username/password')
                else:
            # Account doesnt exist or username/password incorrect

                    flash('Incorrect username/password')
 # evde diff tables indaki ittal, users, deliveryboy and restaurants vere login pattille? 
    return render_template('login.html')
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        who = request.form['Type']

        _hashed_password = generate_password_hash(password)

        if who=="Customers":

            #Check if account exists using MySQL
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            account = cursor.fetchone()
            print(account)
            
            # If account exists show error and validation checks
            if account:
                flash('Account already exists!')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!')
            elif not re.match(r'[A-Za-z0-9]+', username):
                flash('Username must contain only characters and numbers!')
            elif not username or not password or not email:
                flash('Please fill out the form!')
            else:
                # Account doesnt exists and the form data is valid, now insert new account into users table
                cursor.execute("INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)", (fullname, username, _hashed_password, email))
                conn.commit()
                flash('You have successfully registered!')
        elif who == "Deliveryboy":
            #Check if account exists using MySQL
            cursor.execute('SELECT * FROM deliveryBoy_login WHERE username = %s', (username,))
            accountD = cursor.fetchone()
            print(accountD)
            
            # If account exists show error and validation checks
            if accountD:
                flash('Account already exists!')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!')
            elif not re.match(r'[A-Za-z0-9]+', username):
                flash('Username must contain only characters and numbers!')
            elif not username or not password or not email:
                flash('Please fill out the form!')
            else:
                # Account doesnt exists and the form data is valid, now insert new account into users table
                cursor.execute("INSERT INTO deliveryBoy_login (fullname, username, password, email,phone) VALUES (%s,%s,%s,%s,%s)", (fullname, username, _hashed_password, email,phone))
                conn.commit()
                flash('You have successfully registered!')
        elif who =="Restaurants":
            #Check if account exists using MySQL
            cursor.execute('SELECT * FROM restaurant_login WHERE username = %s', (username,))
            accountR = cursor.fetchone()
            print(accountR)
            
            # If account exists show error and validation checks
            if accountR:
                flash('Account already exists!')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!')
            elif not re.match(r'[A-Za-z0-9]+', username):
                flash('Username must contain only characters and numbers!')
            elif not username or not password or not email:
                flash('Please fill out the form!')
            else:
                # Account doesnt exists and the form data is valid, now insert new account into users table
                cursor.execute("INSERT INTO restaurant_login (fullname, username, password, email,phone) VALUES (%s,%s,%s,%s,%s)", (fullname, username, _hashed_password, email,phone))
                conn.commit()
                flash('You have successfully registered!')

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')
   
   
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
  
@app.route('/profile')
def profile(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
 
if __name__ == "__main__":
    app.run(debug=True)