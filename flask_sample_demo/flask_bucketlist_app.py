from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'newuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
@app.route('/main')
def hello_world():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    """ read the posted values from the UI """
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _name = request.form['inputName']
        _username = request.form['inputUserName']
        _password = request.form['inputPassword']
        
        # Write Functions to validate the Name, Email and password
        if _name and _password and _username:
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _username, _hashed_password))
            data = cursor.fetchall()
            
            if not len(data):
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'Error': 'Enter the fields correctly !'})
        
    except Exception as error:
        cursor.close()
        conn.close()
        return json.dumps({'error': str(error)})
    
    finally:
        cursor.close()
        conn.close()
        
if __name__ == '__main__':
    app.run()

