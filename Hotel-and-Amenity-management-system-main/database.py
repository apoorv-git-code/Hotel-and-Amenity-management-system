from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["hotel_management"]
hotels = db["hotels"]
rooms = db["rooms"]
amenities = db["amenities"]
bookings = db["bookings"]
customers = db["customers"]
users = db["users"]

if __name__ == "__main__":
    print("Connected to MongoDB database:")
    print("Database:", db.name)
    print("Collections:", db.list_collection_names())
