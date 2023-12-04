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

@app.route('/customer/dashboard')
def customer_dashboard():
    if 'loggedin' in session and session.get('role') == 'customer':
        cursor = getCursor()

        # Fetch user details
        cursor.execute("SELECT * FROM customer WHERE username = %s", (session['username'],))
        user_details = cursor.fetchone()

        # Fetch holiday houses
        cursor.execute("SELECT * FROM holiday_houses")
        holiday_houses = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('customer_dashboard.html', user_details=user_details, holiday_houses=holiday_houses)
    else:
        # Redirect to login if not logged in as customer
        return redirect(url_for('login'))

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'loggedin' in session:
        cursor = getCursor()
        role = session.get('role')

        if request.method == 'POST':
     
            name = request.form.get('name')
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')

            # Prepare SQL based on the role
            if role == 'customer':
                address = request.form.get('address')
                update_query = """
                    UPDATE customer 
                    SET name = %s, email = %s, address = %s, phone_number = %s
                    WHERE username = %s
                """
                data_tuple = (name, email, address, phone_number, session['username'])
            elif role == 'staff':
                update_query = """
                    UPDATE staff 
                    SET name = %s, email = %s, phone_number = %s
                    WHERE username = %s
                """
                data_tuple = (name, email, phone_number, session['username'])
            else:
                flash('Invalid role for profile update', 'error')
                return redirect(url_for('login'))

            try:
                # Update SQL query
                cursor.execute(update_query, data_tuple)
                connection.commit()
                flash('Profile updated successfully!', 'success')
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'error')

        # Fetch current user data to pre-fill the form
        if role == 'customer':
            cursor.execute("SELECT * FROM customer WHERE username = %s", (session['username'],))
        elif role == 'staff':
            cursor.execute("SELECT * FROM staff WHERE username = %s", (session['username'],))
        user_details = cursor.fetchone()

        cursor.close()
        connection.close()

        dashboard_route = 'customer_dashboard' if role == 'customer' else 'staff_dashboard'
        return render_template(f'{dashboard_route}.html', user_details=user_details)
    else:
        return redirect(url_for('login'))


@app.route('/change_password', methods=['POST'])
def change_password():
    if 'loggedin' in session:
        new_password = request.form.get('new_password')

        # Hash the new password
        hashed_password = generate_password_hash(new_password)

        cursor = getCursor()
        role = session.get('role')

        if role == 'customer' or role == 'staff':
            table = 'customer' if role == 'customer' else 'staff'
            update_query = f"UPDATE {table} SET password = %s WHERE username = %s"
            data_tuple = (hashed_password, session['username'])

            try:
                cursor.execute(update_query, data_tuple)
                connection.commit()
                flash('Password changed successfully!', 'success')
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'error')
        else:
            flash('Unauthorized access.', 'error')

        cursor.close()
        connection.close()

        dashboard_route = 'customer_dashboard' if role == 'customer' else 'staff_dashboard'
        return redirect(url_for(dashboard_route))
    else:
        return redirect(url_for('login'))


@app.route('/house_details/<int:house_id>')
def house_details(house_id):
    if 'loggedin' in session:
        cursor = getCursor()

        # Fetch house details using house_id
        cursor.execute("SELECT * FROM holiday_houses WHERE house_id = %s", (house_id,))
        house = cursor.fetchone()

        cursor.close()
        connection.close()

        if house:
            return render_template('house_details.html', house=house, role=session['role'])
        else:
            flash('House not found', 'error')
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif session['role'] == 'staff':
                return redirect(url_for('staff_dashboard'))
            else:  
                return redirect(url_for('customer_dashboard'))
    else:
        return redirect(url_for('login'))
    
@app.route('/staff/dashboard')
def staff_dashboard():
    if 'loggedin' in session and session.get('role') == 'staff':
        user_details = get_user_by_username(session['username'], session['role'])
        cursor = getCursor()

        cursor.execute("SELECT * FROM holiday_houses")
        holiday_houses = cursor.fetchall()

        cursor.execute("SELECT * FROM customer")  
        customers = cursor.fetchall()  

        cursor.close()
        connection.close()

        if user_details:
            return render_template('staff_dashboard.html', user_details=user_details, holiday_houses=holiday_houses, customers=customers)
        else:
            flash('User details not found', 'error')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/add_house', methods=['GET', 'POST'])
def add_house():
    if 'loggedin' in session and session['role'] in ['staff', 'admin']:
        if request.method == 'POST':
            house_address = request.form['house_address']
            number_of_bedrooms = request.form['number_of_bedrooms']
            number_of_bathrooms = request.form['number_of_bathrooms']
            maximum_occupancy = request.form['maximum_occupancy']
            rental_per_night = request.form['rental_per_night']
            house_image = request.form['house_image']

            # Insert new house into database
            cursor = getCursor()
            cursor.execute(
                "INSERT INTO holiday_houses (house_address, number_of_bedrooms, number_of_bathrooms, maximum_occupancy, rental_per_night, house_image) VALUES (%s, %s, %s, %s, %s, %s)",
                (house_address, number_of_bedrooms, number_of_bathrooms, maximum_occupancy, rental_per_night, house_image)
            )
            connection.commit()

            flash('New holiday house added successfully', 'success')
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('staff_dashboard'))
        return render_template('add_house.html', role=session['role'])  
    else:
        return redirect(url_for('login'))

@app.route('/edit_house/<int:house_id>', methods=['GET', 'POST'])
def edit_house(house_id):
    if 'loggedin' in session and session['role'] in ['staff', 'admin']:
        cursor = getCursor()
        if request.method == 'POST':
            house_address = request.form['house_address']
            number_of_bedrooms = request.form['number_of_bedrooms']
            number_of_bathrooms = request.form['number_of_bathrooms']
            maximum_occupancy = request.form['maximum_occupancy']
            rental_per_night = request.form['rental_per_night']
            house_image = request.form['house_image']

            # Update house in database
            cursor.execute(
                "UPDATE holiday_houses SET house_address = %s, number_of_bedrooms = %s, number_of_bathrooms = %s, maximum_occupancy = %s, rental_per_night = %s, house_image = %s WHERE house_id = %s",
                (house_address, number_of_bedrooms, number_of_bathrooms, maximum_occupancy, rental_per_night, house_image, house_id)
            )
            connection.commit()

            flash('Holiday house updated successfully', 'success')
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('staff_dashboard'))
        else:
            # Fetch current house data to pre-fill the form
            cursor.execute("SELECT house_id, house_address, number_of_bedrooms, number_of_bathrooms, maximum_occupancy, rental_per_night, house_image FROM holiday_houses WHERE house_id = %s", (house_id,))

            house = cursor.fetchone()
            return render_template('add_house.html', house=house, role=session['role'])
    else:
        return redirect(url_for('login'))

@app.route('/delete_house/<int:house_id>', methods=['POST'])
def delete_house(house_id):
    if 'loggedin' in session and session['role'] in ['staff', 'admin']:
        cursor = getCursor()

        # Delete house from database
        cursor.execute("DELETE FROM holiday_houses WHERE house_id = %s", (house_id,))
        connection.commit()

        flash('Holiday house deleted successfully', 'success')
        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('staff_dashboard'))

    else:
        return redirect(url_for('login'))

@app.route('/customer_details/<customer_number>')
def customer_details(customer_number):
    if 'loggedin' in session and (session['role'] == 'staff' or session['role'] == 'admin'):
        cursor = getCursor()
        cursor.execute("SELECT * FROM customer WHERE customer_number = %s", (customer_number,))
        customer = cursor.fetchone()

        if customer:
            cursor.close()
            connection.close()

            return render_template('customer_details.html', customer=customer)
        else:
            flash('Customer not found', 'error')
            return redirect(url_for('staff_dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'loggedin' in session and session.get('role') == 'admin':
        user_details = get_user_by_username(session['username'], session['role'])

        cursor = getCursor()

        cursor.execute("SELECT * FROM holiday_houses")
        holiday_houses = cursor.fetchall()

        cursor.execute("SELECT * FROM customer")
        customers = cursor.fetchall()

        cursor.execute("SELECT * FROM staff")
        staff_members = cursor.fetchall()

        cursor.close()
        connection.close()

        if user_details:
            return render_template('admin_dashboard.html', user_details=user_details, holiday_houses=holiday_houses, customers=customers, staff_members=staff_members)
        else:
            flash('Admin details not found', 'error')
        return render_template('admin_dashboard.html', user_details=user_details, holiday_houses=holiday_houses, customers=customers, staff_members=staff_members)
    else:
        return redirect(url_for('login'))
    
def generate_customer_number():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(100, 999)
    return f"CUST{timestamp}{random_number}"

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if 'loggedin' in session and session['role'] == 'admin':
        if request.method == 'POST':
            customer_number = generate_customer_number()
            username = request.form.get('username')

            name = request.form.get('name')
            email = request.form.get('email')
            address = request.form.get('address')
            phone_number = request.form.get('phone_number')
            plain_text_password = request.form.get('password')
            hashed_password = generate_password_hash(plain_text_password)

            cursor = getCursor()
            cursor.execute(
                "INSERT INTO customer (name, customer_number, username, address, email, phone_number, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (name, customer_number, username, address, email, phone_number, hashed_password)
            )
            connection.commit()

            flash('New customer added successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('add_customer.html')
    else:
        flash('Unauthorized access', 'error')
        return redirect(url_for('login'))

@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    if 'loggedin' in session and session['role'] == 'admin':
        if request.method == 'POST':
            name = request.form.get('name')
            username = request.form.get('username')
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            plain_text_password = request.form.get('password')
            hashed_password = generate_password_hash(plain_text_password)

            staff_number = 'STAFF' + str(random.randint(100, 999))
            date_joined = datetime.now().strftime('%Y-%m-%d')

            # Insert new staff into database
            cursor = getCursor()
            cursor.execute(
                "INSERT INTO staff (name, staff_number, username, email, phone_number, date_joined, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (name, staff_number, username, email, phone_number, date_joined, hashed_password)
            )
            connection.commit()

            flash('New staff member added successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('add_staff.html')
    else:
        flash('Unauthorized access', 'error')
        return redirect(url_for('login'))

@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = getCursor()
        if request.method == 'POST':
            name = request.form['name']
            username = request.form['username']
            email = request.form['email']
            address = request.form['address']
            phone_number = request.form['phone_number']
            plain_text_password = request.form['password']
            hashed_password = generate_password_hash(plain_text_password) if plain_text_password else None

            update_query = "UPDATE customer SET name = %s, username = %s, email = %s, address = %s, phone_number = %s" + (", password = %s" if hashed_password else "") + " WHERE id = %s"
            data_tuple = (name, username, email, address, phone_number) + ((hashed_password,) if hashed_password else ()) + (customer_id,)

            # Update customer in database
            cursor.execute(update_query, data_tuple)
            connection.commit()

            flash('Customer updated successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            cursor.execute("SELECT * FROM customer WHERE id = %s", (customer_id,))
            customer = cursor.fetchone()
            return render_template('edit_customer.html', customer=customer)
    else:
        return redirect(url_for('login'))

@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = getCursor()

        # Delete customer from database
        cursor.execute("DELETE FROM customer WHERE id = %s", (customer_id,))
        connection.commit()

        flash('Customer deleted successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/edit_staff/<int:staff_id>', methods=['GET', 'POST'])
def edit_staff(staff_id):
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = getCursor()
        if request.method == 'POST':
            name = request.form['name']
            username = request.form['username']
            email = request.form['email']
            phone_number = request.form['phone_number']
            plain_text_password = request.form['password']
            hashed_password = generate_password_hash(plain_text_password) if plain_text_password else None

            update_query = "UPDATE staff SET name = %s, username = %s, email = %s, phone_number = %s" + (", password = %s" if hashed_password else "") + " WHERE id = %s"
            data_tuple = (name, username, email, phone_number) + ((hashed_password,) if hashed_password else ()) + (staff_id,)

            # Update staff in database
            cursor.execute(update_query, data_tuple)
            connection.commit()

            flash('Staff member updated successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            # Fetch current staff data to pre-fill the form
            cursor.execute("SELECT * FROM staff WHERE id = %s", (staff_id,))
            staff_member = cursor.fetchone()
            return render_template('edit_staff.html', staff=staff_member)
    else:
        return redirect(url_for('login'))
    
@app.route('/delete_staff/<int:staff_id>', methods=['POST'])
def delete_staff(staff_id):
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = getCursor()

        # Delete staff from database
        cursor.execute("DELETE FROM staff WHERE id = %s", (staff_id,))
        connection.commit()

        flash('Staff member deleted successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    # Remove session data
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.', 'success')
    # Redirect to login page
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)  
