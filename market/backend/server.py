
from flask import Flask, render_template, make_response, url_for, request, send_from_directory, redirect
from pymongo import MongoClient
from secrets import token_urlsafe
import bcrypt
import hashlib
import json
import html
from bson.binary import Binary
import base64

from flask import Flask, render_template, make_response, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import html



app = Flask(__name__) #setting this equal to the file name (web.py)
CORS(app)

#Establish the mongo database
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

def check_auth(auth_tok, username, collection_from_db):
    #auth_tok => string (from request)
    #username => string (from request)
    #collection_from_db => auth_token_collection (collection object)
    #good_or_nah = 0
    record = collection_from_db.find_one({"username": username})
    if record == None:
        return 0
    elif record['auth_token'] == auth_tok:
        return 1
    else:
        return 0

@app.route("/check_auth")
def smd():
    data = request.json
    #not sure if auth_token can be accessed by data['auth_token'}{
    return check_auth(data['auth_token'], data['username'],data['password'])



    #return good_or_nah


#Set up the home page ----------------------------------------------------------------------------------------------------------------------------
@app.route("/") #index.html
def home():

    response = make_response(render_template("index.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    print (response)
    return response


@app.route("/<path:file>")
def pathRoute(file):
    response = make_response(send_from_directory("static", file), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

#Set up the registration form ---------------------------------------------------------------------------------------------------------------------
#Set up the login form-----------------------------------------------------------------------------------------------------------------------------
#@app.route("/login", methods =['GET', 'POST'])

@app.route("/chat-message", methods = ["POST"])
def makePost():
    post = request.data.decode() # Request post as a string
    post = json.loads(post) # Load Post as a Dictionary in format title: message: xsrf:
    username = "Guest"

    # Verify user via authentication token
    authToken = request.cookies.get("auth_token", "")

    if authToken == "":
        # User is a Guest -> Do not allow him to send.
        response = make_response("User is not logged Authenticated", 401)
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    # User is authenticated -> Allow him to send message.
    authToken_hashed = hashlib.sha256(authToken.encode('utf-8')).digest()
    userToken = auth_token_collection.find_one({"auth_token": authToken_hashed})
    username = userToken["username"]
    # Store Post to Database
    db_obj = post # Object that will be sent to the database
    db_obj["username"] = username # Add username to the object
    db_obj["_id"] = token_urlsafe(16) # Randomly generate messageID
    db_obj['id'] = token_urlsafe(16)
    db_obj["likes"] = 0 # Adds a tracker for the number of likes

    db_obj["liked_users"] = [] #Adds a tracker for the users who have liked the messageu
    chat_collection.insert_one(db_obj)

    # Respond with message
    response = make_response("Post sent:" + str(post), 200)
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
            # response = make_response(render_template("index.html"), 200)
            # response.headers["X-Content-Type-Options"] = "nosniff"
            return jsonify({"message": "User successfully added", "code": 1})
        # If the user already exists, give an error
        else:
            return jsonify({"message": "Username already exists", "code": 0})

'''
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

'''



#Set up the login form-----------------------------------------------------------------------------------------------------------------------------
@app.route("/login", methods =['POST'])
def login():
    print('marco')
    # print(request.get_data()) # -> b'username_login=hi&password_login=here'
    # DB represents database
    print(request)
    data = request.json
    print(data)
    islogin = 0
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


@app.route("/chat-history", methods = ["GET"])
def readPost():
    all_posts = postsFromDB()
    response = make_response(json.dumps(all_posts), 200)
    return response

@app.route("/chat-likes", methods = ["POST"])
def addLike():
    request_data = request.data
    message_id = request_data.decode("utf-8")
    message_id = message_id[1:-1]
    mess = chat_collection.find_one({"id":message_id}) #Gets the message data from the message ID
    likes = mess["likes"] #Finds the number of likes using message id
    userLikes = mess["liked_users"] #Finds the list of users using message ID
    filter = {"id": message_id} #Temporary filter item for updating message later
    auth_token = request.cookies.get("auth_token", "") #Finds the auth token from cookies
    #BELOW finds the user from the auth token
    authToken_hashed = hashlib.sha256(auth_token.encode('utf-8')).digest()
    userToken = auth_token_collection.find_one({"auth_token": authToken_hashed})
    user = userToken["username"]
    if user in userLikes:

        userLikes.remove(user) #Removes user name from list of users
        newLikes = likes - 1
        update = {"$set":{"likes": newLikes, "liked_users": userLikes}}
        result = chat_collection.update_one(filter, update)
    else:
        userLikes.append(user)  # Adds user name from list of users
        newLikes = likes + 1
        update = {"$set": {"likes": newLikes, "liked_users": userLikes}}
        result = chat_collection.update_one(filter, update)
    response = make_response("Likes updated", 200)
    return response




app.run(host = "0.0.0.0", port = 8080, debug = True)
