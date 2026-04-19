from database import db

collection = db["rooms"]

class Room:
    def __init__(self, room_no, room_type, price):
        self.room_no = room_no
        self.type = room_type
        self.price = price


def add_room(hotel_name, room_no, room_type, price):
    # Prevent duplicate room numbers WITHIN THE SAME HOTEL
    if collection.find_one({
        "$and": [
            { "$or": [{"hotel_name": hotel_name}, {"hotel name": hotel_name}] },
            { "$or": [{"room_no": room_no}, {"room_number": room_no}, {"room number": room_no}] }
        ]
    }):
        return "duplicate"

    room = {
        "hotel_name": hotel_name,
        "room_no": room_no,
        "type": room_type,
        "price": price
    }
    return collection.insert_one(room).inserted_id


def view_rooms(hotel_name=None):
    query = {}
    if hotel_name:
        query = {"$or": [{"hotel_name": hotel_name}, {"hotel name": hotel_name}]}
        
    rooms = list(collection.find(query))
    unique_rooms = {}
    
    for r in rooms:
        if "hotel_name" not in r:
            val = r.get("hotel name") or r.get("Hotel Name")
            r["hotel_name"] = val if val is not None else "Global"
            
        if "room_no" not in r:
            val = r.get("room_number") or r.get("room number")
            r["room_no"] = val if val is not None else "Unknown"
        if "type" not in r:
            val = r.get("room_type") or r.get("room type")
            r["type"] = val if val is not None else "Unknown"
        if "price" not in r:
            val = r.get("price_per_night") or r.get("price") or r.get("room price")
            r["price"] = float(val) if val is not None else 0.0
            
        r_no = str(r["room_no"])
        
        # Unique across hotel and room_no
        unique_key = f"{r['hotel_name']}_{r_no}"
        
        # Filter out and auto-clean corrupted entries that lack basic identifying room numbers
        if r_no == "Unknown" or r_no.strip() == "":
            try:
                collection.delete_one({"_id": r["_id"]})
            except Exception:
                pass
            continue
            
        if unique_key not in unique_rooms:
            unique_rooms[unique_key] = r
            
    return list(unique_rooms.values())


def delete_room(room_no):
    return collection.delete_one({"room_no": room_no})
