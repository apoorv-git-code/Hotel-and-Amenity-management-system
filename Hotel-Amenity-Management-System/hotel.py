from database import db

collection = db["hotels"]

class Hotel:
    def __init__(self, name, location, rating):
        self.name = name
        self.location = location
        self.rating = rating


def add_hotel(name, location, rating):
    try:
        hotel = {
            "name": name,
            "location": location,
            "rating": rating
        }
        collection.insert_one(hotel)
    except Exception as e:
        print("Error adding hotel:", e)


def view_hotels():
    return collection.find()


def delete_hotel(name):
    collection.delete_one({"name": name})


def update_hotel(name, location):
    collection.update_one(
        {"name": name},
        {"$set": {"location": location}}
    )