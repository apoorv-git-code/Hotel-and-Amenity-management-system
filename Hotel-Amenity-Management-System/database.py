from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["hotel_management"]
hotels = db["hotels"]
rooms = db["rooms"]
amenities = db["amenities"]
bookings = db["bookings"]
customers = db["customers"]
users = db["users"]
