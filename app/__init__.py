#init.py -----------------------------------------------------------
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client.get_database('inventory')
inventory_collection = db['inventory']

from app import routes
