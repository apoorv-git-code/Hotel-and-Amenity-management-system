from database import db

collection = db["rooms"]

class Room:
    def __init__(self, room_no, type, price):
        self.room_no = room_no
        self.type = type
        self.price = price


def add_room(room_no, type, price):
    room = {
        "room_no": room_no,
        "type": type,
        "price": price
    }
    collection.insert_one(room)


def view_rooms():
    return collection.find()


def delete_room(room_no):
    collection.delete_one({"room_no": room_no})