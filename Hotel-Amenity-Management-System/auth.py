from database import db
import hashlib

collection = db["users"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if collection.find_one({"username": username}):
        return False, "Username already exists"
    
    hashed_password = hash_password(password)
    user = {"username": username, "password": hashed_password}
    collection.insert_one(user)
    return True, "Registration successful"

def authenticate_user(username, password):
    user = collection.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        return True, "Login successful"
    return False, "Invalid username or password"
