from flask import Flask, render_template, make_response, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import html
import hashlib
from secrets import token_urlsafe


app = Flask(__name__) #setting this equal to the file name (web.py)
CORS(app)

#Establish the mongo database
#localhost for localhost mongo for docker
mongo_client = MongoClient('localhost')
db = mongo_client["colosseum"]
chat_collection = db["chat"]
user_collection = db["users"]
auth_token_collection = db["auth_tokens"]
xsrf_token_collection = db["xsrf"]

# Delete collection records. --- ALERT """ FOR TESTING ONLY MAKE SURE TO REMOVE
# chat_collection.delete_many({})
# user_collection.delete_many({})
# auth_token_collection.delete_many({})
# xsrf_token_collection.delete_many({})
# MAKE SURE YOU REMOVE THE LINES ABOVE.

#Set up the home page ----------------------------------------------------------------------------------------------------------------------------
@app.route("/") #index.html
def home():
    #index_html
    #app = Flask(__name__, template_folder='../../client/public')
    response = make_response(render_template("index.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

# @app.route("/<path:file>")
# def pathRoute(file):
#     response = make_response(send_from_directory("static", file), 200)
#     response.headers["X-Content-Type-Options"] = "nosniff"
#     return response

#Set up the registration form ---------------------------------------------------------------------------------------------------------------------
@app.route("/register", methods =['POST'])
def process_register():
    data = request.json
    if user_collection.find_one({"username": data.get("username")}) is None:
        # Store username and salted, hashed password in database
        salt = bcrypt.gensalt()
        the_hash = bcrypt.hashpw(data.get("password").encode(), salt)
        user_collection.insert_one({"username": data.get("username"), "password": the_hash})

        # Possibly create new response headers before returning response
        #response = make_response(render_template("index.html"), 200)
        #response.headers["X-Content-Type-Options"] = "nosniff"
        return jsonify({"message": "User successfully added", "code": 1})
    # If the user already exists, give an error
    else:
        return jsonify({"message": "Username already exists", "code":0})



# CODE BELOW: working register without any authentication
# def process_register():
#     print("Register path reached")
#     data = request.json
#     user_collection.insert_one(data)
#     return jsonify({"message": "User successfully added"})



#Set up the login form-----------------------------------------------------------------------------------------------------------------------------
@app.route("/login", methods =['POST'])
def login():
    print('marco')
    # print(request.get_data()) # -> b'username_login=hi&password_login=here'
    # DB represents database
    print(request)
    data = request.json
    print(data)
    user_database = user_collection.find_one({"username": data['username']})
    if (user_database == None):
        # Make response - NO USERS EXIST YET -> NOT GOOD

        response = make_response('0', 404)
        response.headers["X-Content-Type-Options"] = "nosniff"
    else:
        # Access the password associated with the username
        database_password = user_database.get("password", b'none')
        print(database_password)
        # Access the password associated with what the user gave us
        input_password = data['password'].encode()
        print(input_password)
        # If the user does not exist in the database, then database_password = b"none"
        if (database_password == b'none'):
            # Make response if USER DOES NOT EXIST
            response = make_response('0', 404)
            response.headers["X-Content-Type-Options"] = "nosniff"
        # Compare if the passwords are the same - returns True or False
        elif (bcrypt.checkpw(input_password, database_password)):
            auth_token = token_urlsafe(13)  # creates unique token, the 13 is the entropy

            # Make response if PASSWORDS MATCH
            #response = make_response(render_template("index.html"), 200)
            response = make_response('1',200)

            response.headers["X-Content-Type-Options"] = "nosniff"

            # Set the authentication cookie and add to auth_token database named "auth_tokens"
            auth_token_hashed = hashlib.sha256(auth_token.encode('utf-8')).digest()
            response.set_cookie("auth_token", str(auth_token), max_age=3600, httponly=True)
            response.set_cookie("cookie_name", data['username'])
            auth_token_collection.insert_one(
                {"username": data['username'], "auth_token": auth_token_hashed})
            islogin =1
            return response

        else:
            # Make response if PASSWORDS DO NOT MATCH
            #response = make_response(render_template("index.html"), 404)
            response = make_response(0, 404)
            response.headers["X-Content-Type-Options"] = "nosniff"
            return response
    #response.headers['thierry'] = islogin

    print(response)
    return response


def postsFromDB():
    # Function returns a list of all Posts
    ret_list = []
    all_posts = chat_collection.find({})
    for p in all_posts:
        #Escape HTML in the posts
        p["title"] = html.escape(p["title"])
        p["message"] = html.escape(p["message"])
        p["username"] = html.escape(p["username"])
        ret_list.append(p)
    return ret_list



app.run(host = "0.0.0.0", port = 8080)
