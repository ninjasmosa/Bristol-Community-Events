import mysql.connector
from flask import Flask, render_template, request, flash, redirect, url_for, session
from passlib.hash import sha512_crypt
import datetime

app = Flask(__name__)
app.secret_key = '46e95ec4cb18f7dbf326e83102855d3586c41a97851fcc639155bfc73292eed3'

def get_connection():
    '''
    Establishes a connection to the MySQL database.
    This function is used throughout the application whenever a database connection is required
    '''
    try:
        # Connect to the MySQL database using the provided credentials and database name
        # May need to be changed depending on the environment the app is running on
        conn = mysql.connector.connect(host='localhost',                              
                                user='flask',
                                password='FlaskBCE25',
                                database='mydb')
        return conn
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        return None

'''
Endpoints for actions that require user authentication will check if the correct variable is set in the session
Otherwise will prompt the user to log in
Done for both user and admin accouts and actions
'''
# Pages in the account folder
@app.route('/account/settings')
@app.route('/account/settings.html')
def account_settings():
    if 'user-email' in session:
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement_userdetails = 'SELECT * FROM Customers WHERE CustomersEmail = %s;'
            args_userdetails = (session['user-email'],)
            try:
                dbcursor.execute(SQL_statement_userdetails, args_userdetails)
                user = dbcursor.fetchone()
                # print(user)
                return render_template('account/settings.html', user=user) # TODO: display booking info on account page
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                flash('An error occurred while fetching your account details. Please try again.', 'error')
                return render_template('account/settings.html')
            finally:
                dbcursor.close()
                conn.close()
        else:
            flash('Database connection failed. Please try again later.', 'error')
            return render_template('account/settings.html')
    else:
        flash('Please log in to access your account settings.', 'info')
        return redirect(url_for('account_login'))

@app.route('/account/signup')
@app.route('/account/signup.html')
def account_signup():
    if 'user-email' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('/account/settings'))
    else:
        return render_template('account/signup.html')

@app.route('/account/login')
@app.route('/account/login.html')
def account_login():
    if 'user-email' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('/account/settings'))
    else:
        return render_template('account/login.html')

@app.route('/account/resetpassword')
@app.route('/account/resetpassword.html')
def account_reset_password():
    return render_template('account/resetpassword.html')

# Handle account related actions (e.g., login, signup, password reset)
# TODO: Could possibly add salting as well
@app.route('/account/user-signup', methods=['POST'])
def signup_user():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        password_hashed = sha512_crypt.hash(password)
        usertype = request.form['usertype']
        if fname != None and lname != None and email != None and password != None and usertype != None:
            if len(password) < 8:
                flash('Password must be at least 8 characters long.', 'error')
                return redirect(url_for('account_signup'))
            else:
                conn = get_connection()
                if conn != None:
                    print('MySQL Connection is established')                          
                    dbcursor = conn.cursor()
                    SQL_statement = 'INSERT INTO Customers (CustomersFName, CustomersLName, CustomersEmail, CustomersPassword, CustomersType) VALUES (%s, %s, %s, %s, %s);'
                    args = (fname, lname, email, password_hashed, usertype)
                    try:
                        dbcursor.execute(SQL_statement, args)
                        conn.commit()
                        print('User registered successfully.')
                        flash('Signup successful! You can now log in.', 'success')
                        return redirect(url_for('account_login'))
                    except mysql.connector.Error as err:
                        print(f'Error: {err}')
                        flash(f'An error occurred during signup. Please try again.', 'error')
                        return redirect(url_for('account_signup'))
                    finally:
                        dbcursor.close()
                        conn.close()
                else:
                    flash('Database connection failed. Please try again later.', 'error')
                    return redirect(url_for('account_signup'))
        else:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('account_signup'))

@app.route('/account/user-login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email != None and password != None:
            conn = get_connection()
            if conn != None:
                dbcursor = conn.cursor()
                SQL_statement = 'SELECT * FROM Customers WHERE CustomersEmail = %s;'
                args = (email,)
                try:
                    dbcursor.execute(SQL_statement, args)
                    result = dbcursor.fetchone()
                    if result != None:
                        # Verify the password
                        if sha512_crypt.verify(password, result[3]):
                            session['user-email'] = email
                            session['user-type'] = result[4]
                            print('User logged in successfully.')
                            return redirect(url_for('account_settings'))
                        else:
                            flash('Invalid email or password. Please try again.', 'error')
                        return redirect(url_for('account_login'))
                    else:
                        flash('Invalid email or password. Please try again.', 'error')
                        return redirect(url_for('account_login'))
                except mysql.connector.Error as err:
                    print(f'Error: {err}')
                    flash('An error occurred during login. Please try again.', 'error')
                    return redirect(url_for('account_login'))
                finally:
                    dbcursor.close()
                    conn.close()
            else:
                flash('Database connection failed.', 'error')
                return redirect(url_for('account_login'))
        else:
            flash('Please enter both email and password.', 'error')
            return redirect(url_for('account_login'))

@app.route('/account/update-name', methods=['POST'])
def update_name():
    if 'user-email' in session:
        fname = request.form['fname']
        lname = request.form['lname']
        if fname != None and lname != None:
            conn = get_connection()
            if conn != None:
                dbcursor = conn.cursor()
                SQL_statement = 'UPDATE Customers SET CustomersFName = %s, CustomersLName = %s WHERE CustomersEmail = %s;'
                args = (fname, lname, session['user-email'])
                try:
                    dbcursor.execute(SQL_statement, args)
                    conn.commit()
                    flash('Name updated successfully.', 'success')
                    return redirect(url_for('account_settings'))
                except mysql.connector.Error as err:
                    print(f'Error: {err}')
                    flash('An error occurred while updating your name. Please try again.', 'error')
                    return redirect(url_for('account_settings'))
                finally:
                    dbcursor.close()
                    conn.close()
            else:
                flash('Database connection failed. Please try again later.', 'error')
                return redirect(url_for('account_settings'))
        else:
            flash('Please enter both first and last name.', 'error')
            return redirect(url_for('account_settings'))
    else:
        flash('Please log in to update your name.', 'info')
        return redirect(url_for('account_login'))

@app.route('/account/update-email', methods=['POST'])
def update_email():
    if 'user-email' in session:
        email = request.form['email']
        if email != None:
            conn = get_connection()
            if conn != None:
                dbcursor = conn.cursor()
                SQL_statement = 'UPDATE Customers SET CustomersEmail = %s WHERE CustomersEmail = %s;'
                args = (email, session['user-email'])
                try:
                    dbcursor.execute(SQL_statement, args)
                    conn.commit()
                    session['user-email'] = email
                    flash('Email updated successfully.', 'success')
                    return redirect(url_for('account_settings'))
                except mysql.connector.Error as err:
                    print(f'Error: {err}')
                    flash('An error occurred while updating your email. Please try again.', 'error')
                    return redirect(url_for('account_settings'))
                finally:
                    dbcursor.close()
                    conn.close()
            else:
                flash('Database connection failed. Please try again later.', 'error')
                return redirect(url_for('account_settings'))
        else:
            flash('Please enter an email address.', 'error')
            return redirect(url_for('account_settings'))
    else:
        flash('Please log in to update your email.', 'info')
        return redirect(url_for('account_login'))
    
@app.route('/account/update-type', methods=['POST'])
def update_type():
    if 'user-email' in session:
        user_type = request.form['user_type']
        if user_type != None:
            conn = get_connection()
            if conn != None:
                dbcursor = conn.cursor()
                SQL_statement = 'UPDATE Customers SET CustomersType = %s WHERE CustomersEmail = %s;'
                args = (user_type, session['user-email'])
                try:
                    dbcursor.execute(SQL_statement, args)
                    conn.commit()
                    session['user-type'] = user_type
                    flash('User type updated successfully.', 'success')
                    return redirect(url_for('account_settings'))
                except mysql.connector.Error as err:
                    print(f'Error: {err}')
                    flash('An error occurred while updating your user type. Please try again.', 'error')
                    return redirect(url_for('account_settings'))
                finally:
                    dbcursor.close()
                    conn.close()
            else:
                flash('Database connection failed. Please try again later.', 'error')
                return redirect(url_for('account_settings'))
        else:
            flash('Please select a user type.', 'error')
            return redirect(url_for('account_settings'))
    else:
        flash('Please log in to update your user type.', 'info')
        return redirect(url_for('account_login'))
    
# TODO: Implement changing password
@app.route('/account/update-password', methods=['POST'])
def update_password():
    if 'user-email' in session:
        SQL_statement_current_password = 'SELECT CustomersPassword FROM Customers WHERE CustomersEmail = %s;'
        current_password_hashed = request.form['current_password']
        new_password = sha512_crypt.hash(request.form['new_password'])
        if new_password:
            conn = get_connection()
            if conn:
                dbcursor = conn.cursor()
                dbcursor.execute(SQL_statement_current_password, (session['user-email'],))
                current_password_row = dbcursor.fetchone()
                if current_password_row and sha512_crypt.verify(current_password_hashed, current_password_row[0]):
                    SQL_statement = 'UPDATE Customers SET CustomersPassword = %s WHERE CustomersEmail = %s;'
                    args = (new_password, session['user-email'])
                    try:
                        dbcursor.execute(SQL_statement, args)
                        conn.commit()
                        flash('Password updated successfully.', 'success')
                    except mysql.connector.Error as err:
                        print(f'Error: {err}')
                        flash('An error occurred while updating your password. Please try again.', 'error')
                    finally:
                        dbcursor.close()
                        conn.close()
                else:
                    flash('Current password is incorrect. Please try again.', 'error')
                    return redirect(url_for('account_settings'))
        else:
            flash('Please enter a valid password.', 'error')
    else:
        flash('Please log in to update your password.', 'info')
    return redirect(url_for('account_settings'))

@app.route('/account/delete', methods=['POST'])
def delete_account():
    if 'user-email' in session:
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement_user = 'DELETE FROM Customers WHERE CustomersEmail = %s;'
            SQL_statement_booking = 'DELETE FROM Bookings WHERE CustomerEmail = %s;'
            args = (session['user-email'],)
            try:
                dbcursor.execute(SQL_statement_user, args)
                conn.commit()
                dbcursor.execute(SQL_statement_booking, args)
                conn.commit()
                session.pop('user-email', None)
                flash('Account deleted successfully.', 'success')
                return redirect(url_for('home'))
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                flash('An error occurred while deleting your account. Please try again.', 'error')
                return redirect(url_for('account_settings'))
            finally:
                dbcursor.close()
                conn.close()
        else:
            flash('Database connection failed. Please try again later.', 'error')
            return redirect(url_for('account_settings'))
    else:
        flash('Please log in to delete your account.', 'info')
        return redirect(url_for('account_login'))

@app.route('/account/logout')
def logout_user():
    session.pop('user-email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Handle bookings for an account
@app.route('/account/bookings')
def account_bookings():
    SQL_statement = 'SELECT Bookings.idBookings, Events.EventsName, Bookings.Tickets, Bookings.PricePaid, Bookings.DateTimeofBooking, Events.idEvents FROM Bookings JOIN Events ON Bookings.EventID = Events.idEvents WHERE Bookings.CustomerEmail = %s;'
    args = (session['user-email'],)
    conn = get_connection()
    if 'user-email' in session:
        if conn != None:
            dbcursor = conn.cursor()
            try:
                dbcursor.execute(SQL_statement, args)
                bookings = dbcursor.fetchall()
                return render_template('account/bookings.html', bookings=bookings)
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                flash('An error occurred while fetching your bookings. Please try again.', 'error')
                return redirect(url_for('account_settings'))
            finally:
                dbcursor.close()
                conn.close()
    else:
        flash('Please log in to view your bookings.', 'info')
        return redirect(url_for('account_login'))

@app.route('/account/cancel-booking/<int:booking_id>', methods=['POST', 'GET'])
def cancel_booking(booking_id):
    SQL_statement = 'DELETE FROM Bookings WHERE idBookings = %s AND CustomerEmail = %s;'
    args = (booking_id, session['user-email'])
    conn = get_connection()
    if 'user-email' in session:
        if conn != None:
            dbcursor = conn.cursor()
            try:
                dbcursor.execute(SQL_statement, args)
                conn.commit()
                flash('Booking cancelled successfully.', 'success')
                return redirect(url_for('account_bookings'))
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                flash('An error occurred while cancelling your booking. Please try again.', 'error')
                return redirect(url_for('account_bookings'))
            finally:
                dbcursor.close()
                conn.close()
        else:
            flash('Database connection failed. Please try again later.', 'error')
            return redirect(url_for('account_bookings'))
    else:
        flash('Please log in to cancel your bookings.', 'info')
        return redirect(url_for('account_login'))

# Pages in the admin folder
@app.route('/admin')
def admin_index():
    if 'admin-email' in session:
        return redirect(url_for('admin_settings'))
    else:        
        return redirect(url_for('admin_login'))

@app.route('/admin/login')
@app.route('/admin/login.html')
def admin_login():
    if 'admin-email' in session:
        return redirect(url_for('admin_settings'))
    else:
        return render_template('admin/login.html')
    
@app.route('/admin/admin-login', methods=['POST'])
def admin_login_post():
    email = request.form['email']
    password = request.form['password']
    if email and password:
        conn = get_connection()
        if conn:
            dbcursor = conn.cursor()
            SQL_statement = 'SELECT * FROM admins WHERE AdminsEmail = %s;'
            args = (email,)
            try:
                dbcursor.execute(SQL_statement, args)
                result = dbcursor.fetchone()
                if result != None:
                    if sha512_crypt.verify(password, result[3]):
                        session['admin-email'] = email
                        flash('Admin logged in successfully.', 'success')
                        return redirect(url_for('admin_settings'))
                    else:
                        flash('Invalid email or password.', 'error')
                        return redirect(url_for('admin_login'))
                else:
                    flash('Invalid email or password.', 'error')
                    return redirect(url_for('admin_login'))
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                flash('An error occurred during login. Please try again.', 'error')
                return redirect(url_for('admin_login'))
            finally:
                dbcursor.close()
                conn.close()
    else:
        flash('Please enter both email and password.', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin-email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/admin/settings')
@app.route('/admin/settings.html')
def admin_settings():
    if 'admin-email' in session:
        sql = 'SELECT * FROM admins WHERE AdminsEmail = %s;'
        args = (session['admin-email'],)
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            try:
                dbcursor.execute(sql, args)
                admin = dbcursor.fetchone()
                return render_template('admin/settings.html', admin=admin)
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                flash('An error occurred while fetching your account details. Please try again.', 'error')
                return render_template('admin/settings.html')
            finally:
                dbcursor.close()
                conn.close()
    elif 'user-email' in session:
        flash('You do not have permission to access the admin settings.', 'error')
        return redirect(url_for('account_settings'))
    else:
        flash('Please log in as an admin to access the admin settings.', 'info')
        return redirect(url_for('admin_login'))

# TODO: implement changing admin name email and passwod
@app.route('/admin/update-name', methods=['POST'])
def admin_update_name():
    if 'admin-email' in session:
        fname = request.form['fname']
        lname = request.form['lname']
        if fname and lname:
            conn = get_connection()
            if conn:
                dbcursor = conn.cursor()
                SQL_statement = 'UPDATE admins SET AdminsFName = %s, AdminsLName = %s WHERE AdminsEmail = %s;'
                args = (fname, lname, session['admin-email'])
                try:
                    dbcursor.execute(SQL_statement, args)
                    conn.commit()
                    flash('Admin name updated successfully.', 'success')
                except mysql.connector.Error as err:
                    print(f'Error: {err}')
                    flash('An error occurred while updating the admin name. Please try again.', 'error')
                finally:
                    dbcursor.close()
                    conn.close()
        else:
            flash('Please enter a valid name.', 'error')
    else:
        flash('Please log in as an admin to access the admin settings.', 'info')
    return redirect(url_for('admin_settings'))

@app.route('/admin/update-email', methods=['POST'])
def admin_update_email():
    if 'admin-email' in session:
        email = request.form['email']
        if email:
            conn = get_connection()
            if conn:
                dbcursor = conn.cursor()
                SQL_statement = 'UPDATE admins SET AdminsEmail = %s WHERE AdminsEmail = %s;'
                args = (email, session['admin-email'])
                try:
                    dbcursor.execute(SQL_statement, args)
                    conn.commit()
                    session['admin-email'] = email
                    flash('Admin email updated successfully.', 'success')
                except mysql.connector.Error as err:
                    print(f'Error: {err}')
                    flash('An error occurred while updating the admin email. Please try again.', 'error')
                finally:
                    dbcursor.close()
                    conn.close()
        else:
            flash('Please enter a valid email address.', 'error')
    else:
        flash('Please log in as an admin to access the admin settings.', 'info')
    return redirect(url_for('admin_settings'))

@app.route('/admin/update-password', methods=['POST'])
def admin_update_password():
    if 'admin-email' in session:
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        if current_password and new_password:
            conn = get_connection()
            if conn:
                dbcursor = conn.cursor()
                SQL_statement = 'SELECT AdminsPassword FROM admins WHERE AdminsEmail = %s;'
                args = (session['admin-email'],)
                try:
                    dbcursor.execute(SQL_statement, args)
                    result = dbcursor.fetchone()
                    if result and sha512_crypt.verify(current_password, result[0]):
                        new_password_hashed = sha512_crypt.hash(new_password)
                        SQL_statement = 'UPDATE admins SET AdminsPassword = %s WHERE AdminsEmail = %s;'
                        args = (new_password_hashed, session['admin-email'])
                        dbcursor.execute(SQL_statement, args)
                        conn.commit()
                        flash('Admin password updated successfully.', 'success')
                    else:
                        flash('Current password is incorrect.', 'error')
                except mysql.connector.Error as err:
                    print(f'Error: {err}')
                    flash('An error occurred while updating the admin password. Please try again.', 'error')
                finally:
                    dbcursor.close()
                    conn.close()
        else:
            flash('Please enter both current and new passwords.', 'error')
    else:
        flash('Please log in as an admin to access the admin settings.', 'info')
    return redirect(url_for('admin_settings'))

# Manage users page
@app.route('/admin/manage-users')
@app.route('/admin/manage-users.html')
def admin_manage_users():
    if 'admin-email' in session:
        return render_template('admin/manage-users.html')
    elif 'user-email' in session:
        flash('You do not have permission to access the admin settings.', 'error')
        return redirect(url_for('account_settings'))
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_login'))

@app.route('/admin/all_users')
def admin_all_users():
    if 'admin-email' in session:
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement = 'SELECT CustomersFName, CustomersLName, CustomersEmail, CustomersType FROM Customers;'
            try:
                dbcursor.execute(SQL_statement)
                users = dbcursor.fetchall()
                return render_template('admin/all-users.html', users=users)
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                return render_template('admin/manage-users.html', message='An error occurred while fetching users.')
            finally:
                dbcursor.close()
                conn.close()
        else:
            flash('Database connection failed. Please try again later.', 'error')
            return render_template('admin/manage-users.html', message='Database connection failed.')
    elif 'user-email' in session:
        flash('You do not have permission to access the admin settings.', 'error')
        return redirect(url_for('account_settings'))
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_login'))

@app.route('/admin/add_user', methods=['POST', 'GET'])
def admin_add_user():
    if 'admin-email' in session:
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement = 'INSERT INTO Customers (CustomersFName, CustomersLName, CustomersEmail, CustomersPassword, CustomersType) VALUES (%s, %s, %s, %s, %s);'
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            password = sha512_crypt.hash(request.form['password'])
            type = request.form['type']
            args = (fname, lname, email, password, type)
            try:
                dbcursor.execute(SQL_statement, args)
                conn.commit()
                flash('User added successfully.', 'success')
                return redirect(url_for('admin_manage_users'))
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                flash('An error occurred while adding the user. Please try again.', 'error')
                return redirect(url_for('admin_manage_users'))
            finally:
                dbcursor.close()
                conn.close()  
    elif 'user-email' in session:
        flash('You do not have permission to access the admin settings.', 'error')
        return redirect(url_for('account_settings'))
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_login'))

@app.route('/admin/edit_user', methods=['POST', 'GET'])
def admin_edit_user():
    if 'admin-email' in session:
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement = 'UPDATE Customers SET CustomersFName = %s, CustomersLName = %s, CustomersType = %s, CustomersPassword = %s WHERE CustomersEmail = %s;'
            email = request.form['email']
            fname = request.form['fname']
            lname = request.form['lname']
            type = request.form['type']
            password = sha512_crypt.hash(request.form['password'])
            args = (fname, lname, type, password, email)
            try:
                dbcursor.execute(SQL_statement, args)
                conn.commit()
                flash('User updated successfully.', 'success')
                return admin_manage_users()
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                flash('An error occurred while updating the user. Please try again.', 'error')
                return admin_manage_users()
            finally:
                dbcursor.close()
                conn.close()
        else:
            flash('Database connection failed. Please try again later.', 'error')
            return admin_manage_users()
    elif 'user-email' in session:
        flash('You do not have permission to access the admin settings.', 'error')
        return redirect(url_for('account_settings'))
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_login'))
    
@app.route('/admin/delete_user', methods=['POST', 'GET'])
def admin_delete_user():
    if 'admin-email' in session:
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement_user = 'DELETE FROM Customers WHERE CustomersEmail = %s;'
            SQL_statement_booking = 'DELETE FROM Bookings WHERE CustomerEmail = %s;'
            email = request.form['email']
            args = (email,)
            try:
                dbcursor.execute(SQL_statement_user, args)
                conn.commit()
                dbcursor.execute(SQL_statement_booking, args)
                conn.commit()
                flash('User deleted successfully.', 'success')
                return admin_manage_users()
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                flash('An error occurred while deleting the user. Please try again.', 'error')
                return admin_manage_users()
            finally:
                dbcursor.close()
                conn.close()
        else:
            flash('Database connection failed. Please try again later.', 'error')
            return admin_manage_users()
    elif 'user-email' in session:
        flash('You do not have permission to access the admin settings.', 'error')
        return redirect(url_for('account_settings'))
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_login'))

# Manage events page
@app.route('/admin/manage-events')
def admin_manage_events():
    if 'admin-email' in session:
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement_venues = 'SELECT VenueName FROM Venues;'
            SQL_statement_types = 'SELECT * FROM EventTypes;'
            try:
                dbcursor.execute(SQL_statement_venues)
                venues = dbcursor.fetchall()
                dbcursor.execute(SQL_statement_types)
                event_types = dbcursor.fetchall()
                return render_template('admin/manage-events.html', venues=venues, event_types=event_types)
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                return render_template('admin/manage-events.html', message='An error occurred while fetching venues.')
    elif 'user-email' in session:
        return redirect(url_for('account_settings'))
    else:
        return redirect(url_for('account_login'))

@app.route('/admin/all_events')
def admin_all_events():
    after_date = request.args.get('after-date')
    max_price = request.args.get('max-price')
    venue = request.args.get('venue')
    etype = request.args.get('type')

    isWhere = False # Flag to track if any filters are applied

    where = []
    params = []
    if after_date:
        where.append('EventsDate >= %s')
        params.append(after_date)
        isWhere = True
    if max_price:
        where.append('BasePrice <= %s')
        params.append(max_price)
        isWhere = True
    if venue:
        where.append('Venue = %s')
        params.append(venue)
        isWhere = True
    if etype:
        where.append('EventType = %s')
        params.append(etype)
        isWhere = True

    where_sql = 'WHERE ' + ' AND '.join(where) if isWhere else ''
    print(where_sql)

    conn = get_connection()
    if conn != None:
        dbcursor = conn.cursor()
        SQL_statement_events = 'SELECT * FROM Events ' + where_sql + ';'
        SQL_statement_venues = 'SELECT VenueName FROM Venues;'
        SQL_statement_types = 'SELECT * FROM EventTypes;'
        try:
            dbcursor.execute(SQL_statement_events, tuple(params))
            events = dbcursor.fetchall()
            dbcursor.execute(SQL_statement_venues)
            venues = dbcursor.fetchall()
            dbcursor.execute(SQL_statement_types)
            types = dbcursor.fetchall()
            return render_template('admin/all-events.html', events=events, venues=venues, types=types)
        except mysql.connector.Error as err:
            print(f'Error: {err}')
            return render_template('admin/manage-events.html', message='An error occurred while fetching events.')
        finally:
            dbcursor.close()
            conn.close()
    else:
        flash('Database connection failed. Please try again later.', 'error')
        return render_template('admin/manage-events.html', message='Database connection failed.')

@app.route('/admin/add_event', methods=['POST', 'GET'])
def admin_add_event():
    if request.method == 'POST':
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement = 'INSERT INTO Events (EventsName, EventsDescription, EventType, BasePrice, EventsConditions, Venue, EventsDate, EventsTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
            event_name = request.form['event_name']
            event_description = request.form['event_description']
            event_type = request.form['event_type']
            base_price = request.form['base_price']
            event_conditions = request.form['event_conditions']
            venue = request.form['event_venue']
            event_date = request.form['event_date']
            event_time = request.form['event_time']
            args = (event_name, event_description, event_type, base_price, event_conditions, venue, event_date, event_time)
            try:
                dbcursor.execute(SQL_statement, args)
                conn.commit()
                flash('Event added successfully.', 'success')
                return redirect(url_for('admin_manage_events'))
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                flash('An error occurred while adding the event. Please try again.', 'error')
                return redirect(url_for('admin_manage_events'))
            finally:
                dbcursor.close()
                conn.close()

@app.route('/admin/edit_event', methods=['POST'])
def admin_edit_event():                
    if request.method == 'POST':
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement = 'UPDATE Events SET EventsName = %s, EventsDescription = %s, EventType = %s, BasePrice = %s, Venue = %s, EventsDate = %s WHERE idEvents = %s;'
            event_id = request.form['event_id']
            event_name = request.form['event_name']
            event_description = request.form['event_description']
            event_type = request.form['event_type']
            base_price = request.form['base_price']
            venue = request.form['event_venue']
            event_date = request.form['event_date']
            args = (event_name, event_description, event_type, base_price, venue, event_date, event_id)
            try:
                dbcursor.execute(SQL_statement, args)
                conn.commit()
                flash('Event updated successfully.', 'success')
                return redirect(url_for('admin_manage_events'))
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                flash('An error occurred while updating the event. Please try again.', 'error')
                return redirect(url_for('admin_manage_events'))
            finally:
                dbcursor.close()
                conn.close()

@app.route('/admin/delete_event', methods=['POST'])
def admin_delete_event():
    if request.method == 'POST':
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement = 'DELETE FROM Events WHERE idEvents = %s;'
            event_id = request.form['event_id']
            args = (event_id,)
            try:
                dbcursor.execute(SQL_statement, args)
                conn.commit()
                flash('Event deleted successfully.', 'success')
                return redirect(url_for('admin_manage_events'))
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                flash('An error occurred while deleting the event. Please try again.', 'error')
                return redirect(url_for('admin_manage_events'))
            finally:
                dbcursor.close()
                conn.close()

@app.route('/admin/all_event_types')
def admin_all_event_types():
    if 'admin-email' in session:
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement = 'SELECT * FROM EventTypes;'
            try:
                dbcursor.execute(SQL_statement)
                event_types = dbcursor.fetchall()
                return render_template('admin/all-event-types.html', event_types=event_types)
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                return render_template('admin/manage-event-types.html', message='An error occurred while fetching event types.')
            finally:
                dbcursor.close()
                conn.close()
        else:
            flash('Database connection failed. Please try again later.', 'error')
            return render_template('admin/manage-event-types.html', message='Database connection failed.')
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_login'))

# Manage venues page
@app.route('/admin/manage-venues')
def admin_manage_venues():
    if 'admin-email' in session:
        return render_template('admin/manage-venues.html')
    elif 'user-email' in session:
        flash('You do not have permission to access the admin settings.', 'error')
        return redirect(url_for('account_settings'))
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_login'))

@app.route('/admin/all_venues')
def admin_all_venues():
    if 'admin-email' in session:
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement = 'SELECT * FROM Venues;'
            try:
                dbcursor.execute(SQL_statement)
                venues = dbcursor.fetchall()
                return render_template('admin/all-venues.html', venues=venues)
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                return render_template('admin/manage-venues.html', message='An error occurred while fetching venues.')
            finally:
                dbcursor.close()
                conn.close()
        else:
            flash('Database connection failed. Please try again later.', 'error')
            return render_template('admin/manage-venues.html', message='Database connection failed.')
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_login'))
    
@app.route('/admin/add_venue', methods=['POST'])
def admin_add_venue():
    if 'admin-email' in session:
        if request.method == 'POST':
            conn = get_connection()
            if conn != None:
                dbcursor = conn.cursor()
                SQL_statement = 'INSERT INTO Venues (VenueName, VenueCapacity, VenueSuitability) VALUES (%s, %s, %s);'
                venue_name = request.form['venue_name']
                venue_capacity = request.form['venue_capacity']
                venue_suitability = request.form['venue_suitability']
                args = (venue_name, venue_capacity, venue_suitability)
                try:
                    dbcursor.execute(SQL_statement, args)
                    conn.commit()
                    flash('Venue added successfully.', 'success')
                    return redirect(url_for('admin_manage_venues'))
                except mysql.connector.Error as err:
                    print(f'Error: {err}')
                    flash('An error occurred while adding the venue. Please try again.', 'error')
                    return redirect(url_for('admin_manage_venues'))
                finally:
                    dbcursor.close()
                    conn.close()
    flash('Please log in to access settings.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/delete_venue', methods=['POST'])
def admin_delete_venue():
    if 'admin-email' in session:
        if request.method == 'POST':
            conn = get_connection()
            if conn != None:
                dbcursor = conn.cursor()
                SQL_statement = 'DELETE FROM Venues WHERE VenueName = %s;'
                venue_name = request.form['venue_name']
                args = (venue_name,)
                try:
                    dbcursor.execute(SQL_statement, args)
                    conn.commit()
                    flash('Venue deleted successfully.', 'success')
                    return redirect(url_for('admin_manage_venues'))
                except mysql.connector.Error as err:
                    print(f'Error: {err}')
                    flash('An error occurred while deleting the venue. Please try again.', 'error')
                    return redirect(url_for('admin_manage_venues'))
                finally:
                    dbcursor.close()
                    conn.close()
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_manage_venues'))

@app.route('/admin/edit_venue', methods=['POST'])
def admin_edit_venue():
    if 'admin-email' in session:
        if request.method == 'POST':
            conn = get_connection()
            if conn != None:
                dbcursor = conn.cursor()
                SQL_statement = 'UPDATE Venues SET VenueCapacity = %s, VenueSuitability = %s WHERE VenueName = %s;'
                venue_name = request.form['venue_name']
                venue_capacity = request.form['venue_capacity']
                venue_suitability = request.form['venue_suitability']
                args = (venue_capacity, venue_suitability, venue_name)
                try:
                    dbcursor.execute(SQL_statement, args)
                    conn.commit()
                    flash('Venue updated successfully.', 'success')
                    return redirect(url_for('admin_manage_venues'))
                except mysql.connector.Error as err:
                    print(f'Error: {err}')
                    flash('An error occurred while updating the venue. Please try again.', 'error')
                    return redirect(url_for('admin_manage_venues'))
                finally:
                    dbcursor.close()
                    conn.close()
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_login'))

# Managing bookings
@app.route('/admin/manage-bookings')
def admin_manage_bookings():
    if 'admin-email' in session:
        return render_template('admin/manage-bookings.html')
    elif 'user-email' in session:
        flash('You do not have permission to access the admin settings.', 'error')
        return redirect(url_for('account_settings'))
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_login'))

@app.route('/admin/all_bookings')
def admin_all_bookings():
    if 'admin-email' in session:
        customer = request.args.get('customer')
        event = request.args.get('event')

        isWhere = False # Flag to track if any filters are applied
        where = []
        params = []
        if customer:
            where.append('Customers.CustomersEmail = %s')
            params.append(customer)
            isWhere = True
        if event:
            where.append('Events.EventsName = %s')
            params.append(event)
            isWhere = True

        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            SQL_statement_bookings = 'SELECT Bookings.idBookings, Customers.CustomersEmail, Events.idEvents, Events.EventsName, Bookings.Tickets, Bookings.PricePaid, Bookings.DateTimeofBooking FROM Bookings JOIN Customers ON Bookings.CustomerEmail = Customers.CustomersEmail JOIN Events ON Bookings.EventID = Events.idEvents'
            if isWhere:
                SQL_statement_bookings += ' WHERE ' + ' AND '.join(where)
            SQL_statement_bookings += ' ORDER BY Bookings.DateTimeofBooking DESC;'
            SQL_statement_events = 'SELECT idEvents, EventsName FROM Events;'
            SQL_statement_customers = 'SELECT CustomersEmail FROM Customers;'
            try:
                dbcursor.execute(SQL_statement_bookings, tuple(params))
                bookings = dbcursor.fetchall()
                dbcursor.execute(SQL_statement_events)
                events = dbcursor.fetchall()
                dbcursor.execute(SQL_statement_customers)
                customers = dbcursor.fetchall()
                return render_template('admin/all-bookings.html', bookings=bookings, events=events, customers=customers)
            except mysql.connector.Error as err:
                print(f'Error: {err}')
                return render_template('admin/manage-bookings.html', message='An error occurred while fetching bookings.')
            finally:
                dbcursor.close()
                conn.close()
        else:
            flash('Database connection failed. Please try again later.', 'error')
            return render_template('admin/manage-bookings.html', message='Database connection failed.')
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_login'))

@app.route('/admin/delete_booking', methods=['POST', 'GET'])
def admin_delete_booking():
    if 'admin-email' in session:
        if request.method == 'POST':
            conn = get_connection()
            if conn != None:
                dbcursor = conn.cursor()
                SQL_statement = 'DELETE FROM Bookings WHERE idBookings = %s;'
                booking_id = request.form['booking_id']
                args = (booking_id,)
                try:
                    dbcursor.execute(SQL_statement, args)
                    conn.commit()
                    flash('Booking deleted successfully.', 'success')
                    return redirect(url_for('admin_manage_bookings'))
                except mysql.connector.Error as err:
                    print(f'Error: {err}')
                    flash('An error occurred while deleting the booking. Please try again.', 'error')
                    return redirect(url_for('admin_manage_bookings'))
                finally:
                    dbcursor.close()
                    conn.close()
    else:
        flash('Please log in to access settings.', 'info')
        return redirect(url_for('admin_login'))

# Pages in the root of the folder
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/events', methods=['GET'])
def events():

    '''
    Before fetching events from the database, we check if any filters have been applied by the user.
    Dynamically construct a WHERE clause based on filters provided by the user, which is appended to the SQL statement that fetches the events.
    Then display the list of fetched events, which will be filtred based on user preferences.
    '''

    after_date = request.args.get('after-date')
    max_price = request.args.get('max-price')
    venue = request.args.get('venue')
    etype = request.args.get('type')

    isWhere = False # Flag to track if any filters are applied

    where = []
    params = []
    if after_date:
        where.append('EventsDate >= %s')
        params.append(after_date)
        isWhere = True
    if max_price:
        where.append('BasePrice <= %s')
        params.append(max_price)
        isWhere = True
    if venue:
        where.append('Venue = %s')
        params.append(venue)
        isWhere = True
    if etype:
        where.append('EventType = %s')
        params.append(etype)
        isWhere = True

    where_sql = 'WHERE ' + ' AND '.join(where) if isWhere else ''
    print(where_sql)

    # Fetch and display events
    conn = get_connection()
    if conn != None:
        dbcursor = conn.cursor()
        SQL_statement_events = (f'SELECT idEvents, EventsName, EventsDescription, EventType, BasePrice, Venue, EventsDate FROM Events {where_sql} ORDER BY EventsDate;')
        SQL_statement_venues = 'SELECT VenueName FROM Venues;'
        SQL_statement_types = 'SELECT * FROM EventTypes;'
        try:
            dbcursor.execute(SQL_statement_events, tuple(params))
            events = dbcursor.fetchall()
            dbcursor.execute(SQL_statement_venues)
            venues = dbcursor.fetchall()
            dbcursor.execute(SQL_statement_types)
            types = dbcursor.fetchall()
            return render_template('events.html', events=events, venues=venues, types=types)
        except mysql.connector.Error as err:
            print(f'Error: {err}')
            return render_template('events.html', message='An error occurred while fetching events.')
        finally:
            dbcursor.close()
            conn.close()
    return render_template('events.html')

@app.route('/event/<int:event_id>', methods=['GET'])
def event_details(event_id):
    conn = get_connection()
    if conn != None:
        cur = conn.cursor()
        cur.execute("""SELECT idEvents, EventsName, BasePrice, EventsConditions, EventsDescription, Venue, EventsDate, EventsTime, EventType
                    FROM Events WHERE idEvents = %s;""", (event_id,))
        row = cur.fetchone()
        cur.close(); conn.close()
        if not row:
            flash('Event not found.', 'error')
            return redirect(url_for('index'))
        return render_template('event-details.html', event=row)
    else:
        flash('Database connection failed. Please try again later.', 'error')
        return redirect(url_for('index'))
    

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user-email' in session:
        event_id = request.form['event_id']
        event_name = request.form['event_name']
        user_email = request.form['user_email']
        baseprice = float(request.form['price'])
        quantity = int(request.form['quantity'])
        event_date = request.form['date']
        dateandtime = datetime.datetime.now()
        price = baseprice * quantity
        if session['user-type'] == 'Student':
            price *= 0.9  # Apply 10% discount for students

        if event_date < dateandtime.strftime('%Y-%m-%d'):
            flash('You cannot book an event that has already occurred.', 'error')
            return redirect(url_for('events'))
        else:

            conn = get_connection()
            if conn != None:
                dbcursor = conn.cursor()
                SQL_statement = 'INSERT INTO Bookings (CustomerEmail, EventID, Tickets, PricePaid, DateTimeofBooking) VALUES (%s, %s, %s, %s, %s)'
                args = (user_email, event_id, quantity, price, dateandtime)
                try:
                    dbcursor.execute(SQL_statement, args)
                    conn.commit()
                    print('Booking successful.')
                    flash(f'You have successfully booked {quantity} ticket(s) for event {event_name}.', 'success')
                    return render_template('booking-finished.html', event_id=event_id, event_name=event_name, user_email=user_email, price=price, quantity=quantity)
                except mysql.connector.Error as err:
                    print(f'Error: {err}')
                    flash('An error occurred during booking. Please try again.', 'error')
                    return redirect(url_for('events'))
                finally:
                    dbcursor.close()
                    conn.close()
            else:
                flash('Database connection failed. Please try again later.', 'error')
                return redirect(url_for('events'))
    else:
        flash('Please log in to book an event.', 'info')
        return redirect(url_for('account_login'))

@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) # remove debug=True in production
