from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import random
from datetime import datetime
from mysql.connector import FieldType
from . import connect  

app = Flask(__name__)
app.secret_key = '12345'  

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(
        user=connect.dbuser, 
        password=connect.dbpass, 
        host=connect.dbhost, 
        database=connect.dbname, 
        autocommit=True
    )
    dbconn = connection.cursor(dictionary=True)
    return dbconn

@app.route("/")
def home():
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        provided_password = request.form.get('password')
        role = request.form.get('role')

        print("Username:", username)
        print("Role:", role)

        user = get_user_by_username(username, role)
        print("User from DB:", user)

        # Check if user exists and verify password
        if user:
            print("DB Password:", user['password'])
            print(generate_password_hash('12345'))

            if check_password_hash(user['password'], provided_password):
                # User authenticated, set session and redirect
                session['loggedin'] = True
                session['username'] = username
                session['role'] = role
                # Redirect based on role
                if role == 'customer':
                    return redirect(url_for('customer_dashboard'))
                elif role == 'staff':
                    return redirect(url_for('staff_dashboard'))
                elif role == 'admin':
                    return redirect(url_for('admin_dashboard'))
            else:
                print("Password mismatch")
        else:
            print("User not found")

        flash('Invalid username or password')

    return render_template('login.html')

def get_user_by_username(username, role):
    cursor = getCursor()
    table = 'customer' if role == 'customer' else 'staff' if role == 'staff' else 'admin'
    query = f"SELECT * FROM {table} WHERE username = %s"
    cursor.execute(query, (username,))
    # Make sure to fetch the 'password' column
    return cursor.fetchone()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        plain_text_password = request.form.get('password')
        role = request.form.get('role')
        hashed_password = generate_password_hash(plain_text_password)

        print(f"Registering User: {username}, Role: {role}")  

        cursor = getCursor()

        if role == 'customer':
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            random_number = random.randint(100, 999)
            customer_number = f"CUST{timestamp}{random_number}"
            address = request.form.get('address')
            insert_query = "INSERT INTO customer (name, customer_number, username, address, email, phone_number, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data_tuple = (name, customer_number, username, address, email, phone_number, hashed_password)
        elif role == 'staff':
            random_number = random.randint(100, 999)
            date_joined = datetime.now().strftime('%Y-%m-%d') 
            staff_number = f"CUST{date_joined}{random_number}"
            insert_query = "INSERT INTO staff (name, staff_number, username, email, phone_number, date_joined, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data_tuple = (name, staff_number, username, email, phone_number, date_joined, hashed_password)
        elif role == 'admin':
            insert_query = "INSERT INTO admin (name, username, email, phone_number, password) VALUES (%s, %s, %s, %s, %s)"
            data_tuple = (name, username, email, phone_number, hashed_password)
        else:
            flash('Invalid role selected.')
            return redirect(url_for('register'))

        try:
            print(f"Executing query: {insert_query}")  
            print(f"Data: {data_tuple}") 

            cursor.execute(insert_query, data_tuple)
            connection.commit()
            print('Registration sucessful.')  
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            print(f"Error: {err}")  
            flash(f'An error occurred: {err}', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'loggedin' in session and session.get('role') == 'admin':
        return render_template('admin_dashboard.html')
    return redirect(url_for('login'))

@app.route('/customer/dashboard')
def customer_dashboard():
    if 'loggedin' in session and session.get('role') == 'customer':
        return render_template('customer_dashboard.html')
    return redirect(url_for('login'))

@app.route('/staff/dashboard')
def staff_dashboard():
    if 'loggedin' in session and session.get('role') == 'staff':
        return render_template('staff_dashboard.html')
    return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    # Remove session data
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('role', None)
    # Redirect to login page
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)  
