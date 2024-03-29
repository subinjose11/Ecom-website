
from flask import Flask, request,jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

def db_connection():
    conn=None
    try:                
        conn = pymysql.connect(
        host='localhost',
        database='Ecom',
        user='root',
        password='1131',
        cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(e)
    return conn


# Method to register a new user
@app.route('/register', methods=['POST'])
def register():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        try:
            username = request.form['user_name']
            passcode = request.form['passcode']
            confirm_passcode= request.form['confirm_passcode']
            
        except KeyError as e:
            return jsonify({'error': f'KeyError: {e}'}), 400 
    
    cursor.execute("SELECT * FROM user_details Where username='{}'".format(username)) 
    result=[row for row in cursor.fetchall()]    
        
    if result:
        return jsonify ("Username already exists. Please choose another username.")
    else:
        if passcode!=confirm_passcode:
            return jsonify("Please verify the confirm password")
        else:
            query="INSERT INTO user_details (username, passcode) VALUES ('{}','{}');".format (username, passcode)
            cursor.execute(query)
            conn.commit()
            return jsonify("Registration successful.")


# Method to Post and get customer_details
@app.route('/customer_details', methods=['POST','GET'])
def customer_details():
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        try:
            new_customer_name = request.form['customer_name']
            new_mobile_number = request.form['mobile_number']
            new_dateofbirth = request.form['date_of_birth']
            new_email = request.form['email']
            new_address = request.form['address']
            new_pincode = request.form['pin_code']
            
        except KeyError as e:
            return jsonify({'error': f'KeyError: {e}'}), 400 
                
        query="insert into customer_details (customer_name,mob_number,date_of_birth,email,address,pin_code) values ('{}','{}','{}','{}','{}','{}');".format(new_customer_name,new_mobile_number,new_dateofbirth,new_email,new_address,new_pincode)

        cursor.execute(query)
        conn.commit()
        conn.close()
        return jsonify({'message': 'Customer details registered successfully'}), 200
    
    elif request.method=='GET':
        customers=[]
        cursor.execute("SELECT * FROM customer_details") 
        for row in cursor.fetchall():
            customers.append(row)
        conn.close()
        return jsonify(customers)   
        

if __name__=='__main__':
    app.run(debug=True)