from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tamil_2005'  # Your MySQL password here
app.config['MYSQL_DB'] = 'contact_management'

mysql = MySQL(app)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Insert new contact into the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contacts (name, email, phone) VALUES (%s, %s, %s)', 
                       (name, email, phone))
        mysql.connection.commit()
        cursor.close()

        flash('Contact added successfully!')
        return redirect(url_for('contacts'))

    # Fetch all contacts from the database
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    cursor.close()

    return render_template('contacts.html', contacts=contacts)

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Insert new contact into the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contacts (name, email, phone) VALUES (%s, %s, %s)', 
                       (name, email, phone))
        mysql.connection.commit()
        cursor.close()

        flash('Contact added successfully!')
        return redirect(url_for('contacts'))

    return render_template('add_contact.html')

@app.route('/delete_contact/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = %s', (contact_id,))
    mysql.connection.commit()
    cursor.close()

    flash('Contact deleted successfully!')
    return redirect(url_for('contacts'))

@app.route('/edit_contact/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Update contact in the database
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE contacts SET name = %s, email = %s, phone = %s WHERE id = %s',
                       (name, email, phone, contact_id))
        mysql.connection.commit()
        cursor.close()

        flash('Contact updated successfully!')
        return redirect(url_for('contacts'))

    # Fetch the contact details
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = %s', (contact_id,))
    contact = cursor.fetchone()
    cursor.close()

    return render_template('edit_contact.html', contact=contact)

@app.route('/search', methods=['GET'])
def search_contacts():
    query = request.args.get('query', '')

    # Search contacts by name, email, or phone
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT * FROM contacts WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s',
        (f'%{query}%', f'%{query}%', f'%{query}%')
    )
    contacts = cursor.fetchall()
    cursor.close()

    return jsonify([{'id': c[0], 'name': c[1], 'email': c[2], 'phone': c[3]} for c in contacts])

if __name__ == '__main__':
    # Create the table if it doesn't exist
    with app.app_context():  # Establish an application context
        cursor = mysql.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            phone VARCHAR(20)
        )''')
        mysql.connection.commit()
        cursor.close()

    app.secret_key = 'your_secret_key'
    app.run(debug=True)
