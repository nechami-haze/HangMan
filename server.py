from flask import Flask, request, jsonify, abort, make_response
from flask_cors import CORS, cross_origin
import random
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, supports_credentials=True)

def load_users():
    with open('users.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def save_users(users):
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

@app.route('/say_hello/<name>', methods=['GET'])
def func1(name):
    return f"Hello {name} !"

@app.route('/check_pas/<password>', methods=['GET'])
def func2(password):
    users = load_users()
    for user in users:
        if user['password'] == password:
            response = make_response("אתה כבר מוכר במערכת! הינך מועבר למשחק!", 200)
            # הגדרת קוקי
            expires = datetime.now() + timedelta(minutes=10)  # קוקי יתפוגג לאחר 10 דקות
            response.set_cookie('user_password', password, expires=expires)
            return response
    return (f"אינך רשום במערכת! ולכן עליך להזין מספר פרטים חשובים:"), 500

@app.route('/enrollment/<name>/<password>/<tz>/<phone>', methods=['GET'])
def func3(name, password, tz, phone):
    users = load_users()
    new_user = {
        'name': name,
        'password': password,
        'tz': tz,
        'phone': phone,
        'numGame': 0,
        'numWin': 0,
        'words': []
    }
    users.append(new_user)
    save_users(users)

@app.route('/randomWord/<num>', methods=['GET'])
def func4(num):
    try:
        with open("secret.txt", 'r') as nn:
            vv = nn.read()
            allWords = vv.split(" ")
            if len(allWords) == 0:
                return "No words available", 500
            random.shuffle(allWords)
            w = allWords[(int(num) % int(len(allWords))) - 1]
            return w
    except Exception as e:
        return str(e), 500

@app.route('/options/<option>', methods=['GET'])
def func5(option):
    if option == '1':
        return '1'
    elif option == '2':
        return '2'
    elif option == '3':
        return '3'
    else:
        return ('error')


@cross_origin(app, supports_credentials=True)
@app.route('/set_cookie', methods=['POST'])
def set_cookie():
    try:
        obj = request.json
        # if 'user_name' not in obj:
        #     return make_response("User name is required!", 400)

        response = make_response("Cookie set!", 200)
        response.set_cookie("user", obj['player_name'], max_age=60, httponly=True, secure=False, samesite='None')
        return response
    except Exception as e:
        return make_response(f"An error occurred: {str(e)}", 500)


@app.route('/get_cookie', methods=['GET'])
def func6():
    player_name = request.cookies.get('user')
    if player_name:
        return 'V'
    return 'X'

if __name__ == "__main__":
    app.run(debug=True)
