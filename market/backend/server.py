from flask import Flask, render_template, make_response, url_for, request, send_from_directory, redirect, jsonify
from pymongo import MongoClient
from secrets import token_urlsafe
from flask_cors import CORS
import bcrypt
import hashlib
import json
import html
from bson.binary import Binary
import base64

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

#Set up the home page ----------------------------------------------------------------------------------------------------------------------------
@app.route("/") #index.html
def home():
    response = make_response(render_template("index.html"), 200)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

from class_reg_log import reg_log
#Set up the registration form ---------------------------------------------------------------------------------------------------------------------
@app.route("/register", methods =['GET', 'POST'])
# def process_register():
#     print("Register path reached")
#     data = request.json
#     user_collection.insert_one(data)
#     return jsonify({"message": "User successfully added"})
def register_user():
    data = request.json
    register_obj = reg_log()
    register_obj.register(data)



#Set up the login form-----------------------------------------------------------------------------------------------------------------------------
# @app.route("/login", methods =['GET', 'POST'])

app.run(host = "0.0.0.0", port = 8080)
