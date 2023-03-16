import os,gridfs,json
from flask import Flask,request
from flask_pymongo import PyMongo

server = Flask(__name__)
server.config["mongo_uri"] = "mongodb://mongo:27017"

mongo = PyMongo(server)
fs = gridfs.GridFS(mongodb)
