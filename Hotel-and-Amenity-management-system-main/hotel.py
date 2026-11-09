from database import db

collection = db["hotel_data"]

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
            "rating": round(float(rating), 1)
        }
        return collection.insert_one(hotel).inserted_id
    except ValueError:
        print("Error adding hotel: rating must be a number")
        return None
    except Exception as e:
        print("Error adding hotel:", e)
        return None


def view_hotels():
    hotels = list(collection.find())
    for h in hotels:
        if "name" not in h:
            val = h.get("Hotel Name") or h.get("hotel_name") or h.get("hotel name") or h.get("hotel names")
            h["name"] = val if val is not None else "Unknown"
        if "location" not in h:
            val = h.get("Location") or h.get("city_name") or h.get("city name") or h.get("location")
            h["location"] = val if val is not None else "Unknown"
        if "rating" not in h:
            val = h.get("Review Score (1-5)") or h.get("ratings") or h.get("rating")
            h["rating"] = round(float(val), 1) if val is not None else 0.0
        else:
            h["rating"] = round(float(h["rating"]), 1)
    return hotels


def delete_hotel(name):
    return collection.delete_one({"$or": [{"name": name}, {"Hotel Name": name}, {"hotel_name": name}, {"hotel name": name}]})


def update_hotel(name, location=None, rating=None):
    updates = {}
    
    # First find the document to handle diverse key schemas
    target_hotel = collection.find_one({"$or": [{"name": name}, {"Hotel Name": name}, {"hotel_name": name}, {"hotel name": name}]})
    if not target_hotel:
        print("Hotel not found")
        return None

    if location is not None:
        if "Location" in target_hotel:
            updates["Location"] = location
        else:
            updates["location"] = location

    if rating is not None:
        try:
            r_val = round(float(rating), 1)
            if "Review Score (1-5)" in target_hotel:
                updates["Review Score (1-5)"] = r_val
            elif "ratings" in target_hotel:
                updates["ratings"] = r_val
            else:
                updates["rating"] = r_val
        except ValueError:
            print("Error updating hotel: rating must be a number")
            return None

    if not updates:
        print("Nothing to update for hotel")
        return None

    return collection.update_one({"_id": target_hotel["_id"]}, {"$set": updates})

if __name__ == "__main__":
    print("Hotels:")
    for h in view_hotels():
        print(h)
