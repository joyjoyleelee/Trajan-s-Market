from flask import Flask, render_template, make_response, url_for, request, send_from_directory, redirect
from pymongo import MongoClient
from secrets import token_urlsafe
import bcrypt
import hashlib
import json
import html
from bson.binary import Binary
import base64

class reg_log:

    def register():
        #print(request.form.get('username_reg')) # -> gets the username input
        #print(request.get_data()) # -> b'username_reg=hi&password_reg=here'
        if (request.method == 'POST'):
            #Check if the user does not exist yet -> valid
            if (user_collection.find_one({"username": request.form['username_reg']}) == None):
                #Store username and salted, hashed password in database
                #print("this is a test")
                print(request)
                salt = bcrypt.gensalt()
                the_hash = bcrypt.hashpw(request.form['password_reg'].encode(), salt)
                user_collection.insert_one({"username": request.form['username_reg'], "password": the_hash})

                #Make response - USER DOES NOT EXIST -> GOOD
                response = make_response(render_template("index.html"), 200)
                response.headers["X-Content-Type-Options"] = "nosniff"
            #If the user already exists, give an error
            else:
                #Make response - USER ALREADY EXISTS -> NOT GOOD
                response = make_response("User already exists", 404)
                response.headers["X-Content-Type-Options"] = "nosniff"
            return response


    def login():
        #print(request.get_data()) # -> b'username_login=hi&password_login=here'
        #DB represents database
        user_database = user_collection.find_one({"username": request.form['username_login']})
        if(user_database == None):
            #Make response - NO USERS EXIST YET -> NOT GOOD
            response = make_response("Nothing in database", 404)
            response.headers["X-Content-Type-Options"] = "nosniff"
        else:
            #Access the password associated with the username
            database_password = user_database.get("password", b'none')
            print(database_password)
            #Access the password associated with what the user gave us
            input_password = request.form['password_login'].encode()
            print(input_password)
            #If the user does not exist in the database, then database_password = b"none"
            if (database_password == b'none'):
                #Make response if USER DOES NOT EXIST
                response = make_response("User does not exist", 404)
                response.headers["X-Content-Type-Options"] = "nosniff"
            #Compare if the passwords are the same - returns True or False
            elif (bcrypt.checkpw(input_password, database_password)):
                auth_token = token_urlsafe(13) #creates unique token, the 13 is the entropy

                #Make response if PASSWORDS MATCH
                response = make_response(render_template("index.html"), 200)
                response.headers["X-Content-Type-Options"] = "nosniff"

                #Set the authentication cookie and add to auth_token database named "auth_tokens"
                auth_token_hashed = hashlib.sha256(auth_token.encode('utf-8')).digest()
                response.set_cookie("auth_token", str(auth_token), max_age= 3600, httponly=True)
                response.set_cookie("cookie_name", request.form['username_login'])
                auth_token_collection.insert_one({"username": request.form['username_login'], "auth_token": auth_token_hashed})

            else:
                #Make response if PASSWORDS DO NOT MATCH
                response = make_response(render_template("index.html"), 404)
                response.headers["X-Content-Type-Options"] = "nosniff"
        return response