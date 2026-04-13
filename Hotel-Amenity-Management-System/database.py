from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["hotel_management"]
    print("Database Connected Successfully")
except Exception as e:
    print("Database connection error:", e)
