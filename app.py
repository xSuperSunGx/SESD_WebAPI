from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)
#Mysql Connector
def statrt():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Indianer@2004",
        database="sesd_db"
    )

    mycursor = mydb.cursor(prepared=True)

    mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), location VARCHAR(255), plz INT)")
    mydb.commit()

    return mydb, mycursor
mydb, mycursor = statrt()


@app.route('/users', methods=['GET'])
def users():
    mycursor.execute("SELECT name FROM users")
    myresult = mycursor.fetchall()
    return jsonify(myresult)
@app.route('/users/<string:name>', methods=['GET'])
def user(name):
    mycursor.execute("""SELECT * FROM users WHERE name = %s""", (name,))
    myresult = mycursor.fetchall()
    return jsonify(myresult)
@app.route('/users/<string:name>', methods=['DELETE'])
def delete_user(name):
    mycursor.execute("""DELETE FROM users WHERE name = %s""", (name,))
    mydb.commit()
    return jsonify({'message': 'User deleted'})
@app.route('/users', methods=['POST'])
def create_user():
    if existuser(request.json['name']):
        return jsonify({'message': 'User already exists'})
    mycursor.execute("""INSERT INTO users (name, location, plz) VALUES (%s, %s, %s)""", (request.json['name'], request.json['location'], request.json['plz']))
    mydb.commit()
    return jsonify({'message': 'User created'})

def existuser(name):
    mycursor.execute("""SELECT * FROM users WHERE name = %s""", (name,))
    myresult = mycursor.fetchall()
    print(myresult)
    return myresult != []



if __name__ == '__main__':
    app.run()
