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
    collection.insert_one(amenity)


def view_amenities():
    return collection.find()


def delete_amenity(name):
    collection.delete_one({"name": name})