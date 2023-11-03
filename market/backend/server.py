#This will be the main file
from flask import Flask, render_template, make_response, url_for, request, send_from_directory, redirect
from pymongo import MongoClient
from secrets import token_urlsafe
import bcrypt
import hashlib
import json
import html
from bson.binary import Binary
import base64

app = Flask(__name__) #setting this equal to the file name (web.py)

#Establish the mongo database
mongo_client = MongoClient('mongo')
db = mongo_client["colosseum"]
chat_collection = db["listing"]
user_collection = db["users"]
auth_token_collection = db["auth_tokens"]