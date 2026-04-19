from database import db
from bson.objectid import ObjectId

collection = db["bookings"]

class Booking:
    def __init__(self, customer, room_no, date, checkout_date=None):
        self.customer = customer
        self.room_no = room_no
        self.date = date
        self.checkout_date = checkout_date

def add_booking(customer, room_no, date, checkout_date=None):
    booking = {
        "customer": customer,
        "room_no": room_no,
        "date": date,
        "checkout_date": checkout_date
    }
    return collection.insert_one(booking).inserted_id


def view_bookings():
    return list(collection.find())


def cancel_booking(booking_id):
    try:
        return collection.delete_one({"_id": ObjectId(booking_id)})
    except:
        return None
