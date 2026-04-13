from database import db

collection = db["amenities"]

class Amenity:
    def __init__(self, name, description):
        self.name = name
        self.description = description


def add_amenity(name, description):
    amenity = {
        "name": name,
        "description": description
    }
    return collection.insert_one(amenity).inserted_id


def view_amenities():
    return list(collection.find())


def delete_amenity(name):
    return collection.delete_one({"name": name})
