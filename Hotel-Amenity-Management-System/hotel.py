from database import db

collection = db["hotels"]

class Hotel:
    def __init__(self, name, location, rating, _id=None):
        self.name = name
        self.location = location
        self.rating = rating
        self.id = _id


def add_hotel(name, location, rating):
    try:
        hotel = {
            "name": name,
            "location": location,
            "rating": float(rating)
        }
        return collection.insert_one(hotel).inserted_id
    except ValueError:
        print("Error adding hotel: rating must be a number")
        return None
    except Exception as e:
        print("Error adding hotel:", e)
        return None


def view_hotels():
    return list(collection.find())


def delete_hotel(name):
    return collection.delete_one({"name": name})


def update_hotel(name, location=None, rating=None):
    updates = {}
    if location is not None:
        updates["location"] = location
    if rating is not None:
        try:
            updates["rating"] = float(rating)
        except ValueError:
            print("Error updating hotel: rating must be a number")
            return None

    if not updates:
        print("Nothing to update for hotel")
        return None

    return collection.update_one({"name": name}, {"$set": updates})
