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
    return list(collection.find())


def delete_room(room_no):
    return collection.delete_one({"room_no": room_no})
