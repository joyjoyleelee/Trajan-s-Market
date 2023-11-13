from flask import Flask, render_template, make_response, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import date, datetime #this is to keep track of the dates
import bcrypt
import hashlib
import html


app = Flask(__name__) #setting this equal to the file name (web.py)
CORS(app)

#Establish the mongo database
mongo_client = MongoClient('localhost')
db = mongo_client["colosseum"]
user_collection = db["users"]
auth_token_collection = db["auth_tokens"]
listings_collection = db["listings"]

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

#Helper function for create listing
def createImage(data, photo_data, content_length, content_type, auth_token):
    if(auth_token != None):
        received_data = b''
        #If the length is less than 2048, we can read it in one go
        if content_length <= 2048:
                received_data = photo_data.body
        #Otherwise we receive the data in chunks
        else:
            received_data = photo_data.body
            been_read = len(photo_data.body)
            while been_read < content_length:
                received_data += photo_data.recv(content_length - len(photo_data.body))
                been_read += (content_length - len(photo_data.body))
        print(f'data received: {received_data}')
        boundary = content_type.split("boundary=")[1]
        print(f'BOUNDARY: {boundary}')
        split_data = received_data.split(boundary.encode())
        user_data = auth_token_collection.find_one({"auth_token": hashlib.sha256(auth_token.encode()).hexdigest()}) #hexdigest turns the bytes to a string    
        current_user = user_data["_id"]
        print(f'current user: {current_user}')

        #If the user exists, parse the image data and add to user database
        if(user_data != None):
            filename = "/market/backend/image/" + str(current_user) + ".jpg" #im lazy and using the username ID as filename
            with open("." + filename, 'wb') as newFile: #write to the end of a new file IN BYTES
                #Get the image bytes from each part
                for eachPart in split_data:
                    print(f'eachPart: {eachPart}')
                    if (b'\r\n\r\n' in eachPart):
                        headers = eachPart.split("\r\n\r\n".encode())[0]
                        print(f'headers: {headers}')
                        if b"Content-Disposition: form-data" in headers:
                            print("WE MADE IT")
                            image_bytes = eachPart.split("\r\n\r\n".encode())[1]
                            data = image_bytes.replace(b'\r\n', b"").replace(b"--", b"")
                            #Save this image as a file on your server
                            newFile.write(data)
                    else:
                        data = eachPart.replace(b'\r\n', b"").replace(b"--", b"")
                        newFile.write(data)

            #Store the filename of this image in your database as part of this user's profile
            user_collection.find_one_and_update({"username": user_data["username"]}, {"$set":{"filename": filename}})

#Create the listings-----------------------------------------------------------------------------------------------------------------------------
@app.route("/create-listing", methods =['GET'])
def createListing():
    # WHAT I NEED IN THE DATA: ********************************************************************************
    # ID, Item name, Item description, Start date, End date, Price, Current user bidding, User who posted listing, 
    # Photo, Headers (in dict)
    data = request.json
    auth_token = data.headers.get("auth_token")
    #If user is authenticated
    user_data = auth_token_collection.find_one({"auth_token": hashlib.sha256(auth_token.encode()).hexdigest()}) #hexdigest turns the bytes to a string    
    if(user_data != None):
        current_user = user_data["_id"]
        #NOTE: gonna need to reformat date in order to compare -> WEBSOCKETS
        listing = {"Item name": data.get("item_name"), 
                    "Item description": data.get("item_description"), 
                    "Start date": str(datetime.now()), 
                    "End date": data.get("end_date"), 
                    "Price": data.get("price"), 
                    "Current user bidding": None, 
                    "User who posted listing": current_user, 
                    }
    addPhoto(listing, data, auth_token)
    listings_collection.insert_one(listing)
    return jsonify(listing)

#Create the photo-----------------------------------------------------------------------------------------------------------------------------
@app.route("/add-photo", methods =['GET'])
def addPhoto(listing, data, auth_token):
    content_length = data.headers.get("content_length")
    content_type = data.headers.get("content_type")
    #If a photo was uploaded AND user is authenticated -> create listing
    user_data = auth_token_collection.find_one({"auth_token": hashlib.sha256(auth_token.encode()).hexdigest()}) #hexdigest turns the bytes to a string    
    if(user_data != None):
        if(request.body != b''):
            photo = createImage(data, request.body, content_length, content_type, auth_token)
            listing["Photo": photo]
        else:
            return jsonify({"message": "No image uploaded"})

#Helper function for the 3 auction pages - returns ALL listings 
def postsFromDB():
    # Function returns a list of all listings
    ret_list = []
    all_posts = listings_collection.find({})
    for p in all_posts:
        #Escape HTML in the posts
        p["item_name"] = html.escape(p["item_name"])
        p["item_description"] = html.escape(p["item_description"])
        p["current_user_bidding"] = html.escape(p["current_user_bidding"])
        p["user_posted"] = html.escape(p["user_posted"])
        ret_list.append(jsonify(p))
    return ret_list

#Helper function for the 3 auction pages - determines whether an auction has ended or not
#TRUE - if auction has ended, FALSE - if auction is ongoing
def auctionEnded(dict):
    #Auction date in the format: YYYY/MM/DD/HR/MN
    end = dict.get("end_date")
    end_list = end.split("/") #[year, month, day, hour, minute]
    #Current date using datetime imports
    now = str(datetime.now()).split(" ") #['2023-11-11', '18:37:21.560362']
    current_date = now[0].split('-') # ['2023', '11', '11']
    current_time = now[1].split(':') # ['18', '38', '33.673144']

    #Compare current year with auction year
    if current_date[0] < end_list[0]:
        return False
    elif current_date[0] == end_list[0]:
        #Compare current month with auction month
        if current_date[1] < end_list[1]:
            return False
        elif current_date[1] == end_list[1]:
            #Compare current day with auction day
            if current_date[2] < end_list[2]:
                return False
            elif current_date[2] == end_list[2]:
                #Compare current hour with auction hour
                if current_time[0] < end_list[3]:
                    return False
                elif current_time[0] == end_list[3]:
                    #Compare current min with auction min
                    if current_time[1] < end_list[4]:
                        return False
                    else:
                        return True
                else:
                    return True
            else:
                return True
        else:
            return True
    else:
        return True
#Set up the 3 listing pages-----------------------------------------------------------------------------------------------------------------------------
#SEND BACK A LIST OF JSON DICTS - EACH DICT IS A LISTING
@app.route("/winnings", methods =['GET'])
#find user through auth cookie
def postWinnings():
    # WHAT I NEED IN THE DATA: **********************
    #{"headers": {all the headers}}
    data = request.json
    auth_token = data.get("auth_token")
    user_data = auth_token_collection.find_one({"auth_token": hashlib.sha256(auth_token.encode()).hexdigest()}) #hexdigest turns the bytes to a string    
    #If the user is authenticated, then find all their won auctions
    if (user_data != None):
        current_user = user_data["_id"]

        actually_won = []
        maybe_won = listings_collection.find({"Current user bidding": current_user})
        for listing in maybe_won:
            #If the auction has ended, then added to user's auctions won list
            if auctionEnded(listing.get("end_date")):
                actually_won.append(listing)
        return jsonify({"message": "Won auctions found", "auctions": actually_won})
    else:
        return jsonify({"message": "No auctions found"})

@app.route("/postedAuctions", methods =['GET'])
#find user through auth cookie
def userPostedAuctions():
    # WHAT I NEED IN THE DATA: **********************
    #{"headers": {all the headers}}
    data = request.json


@app.route("/auctions", methods =['GET'])
#start with sending ALL auctions - might need to change to just the ones still running later
def totalAuctions():
    allposts = postsFromDB()
    return jsonify({"message": "All auctions found", "auctions": allposts}) #should be a list of JSON dicts






app.run(host = "0.0.0.0", port = 8080)
