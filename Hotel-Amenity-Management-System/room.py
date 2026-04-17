from database import db

collection = db["rooms"]

class Room:
    def __init__(self, room_no, room_type, price):
        self.room_no = room_no
        self.type = room_type
        self.price = price


def add_room(room_no, room_type, price):
    room = {
        "room_no": room_no,
        "type": room_type,
        "price": price
    }
    return collection.insert_one(room).inserted_id


def view_rooms():
    rooms = list(collection.find())
    for r in rooms:
        if "room_no" not in r:
            val = r.get("room_number") or r.get("room number")
            r["room_no"] = val if val is not None else "Unknown"
        if "type" not in r:
            val = r.get("room_type") or r.get("room type")
            r["type"] = val if val is not None else "Unknown"
        if "price" not in r:
            val = r.get("price_per_night") or r.get("price") or r.get("room price")
            r["price"] = float(val) if val is not None else 0.0
    return rooms


def delete_room(room_no):
    return collection.delete_one({"room_no": room_no})
