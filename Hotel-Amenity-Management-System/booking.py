from database import db

collection = db["bookings"]

class Booking:
    def __init__(self, customer, room_no, date):
        self.customer = customer
        self.room_no = room_no
        self.date = date


def add_booking(customer, room_no, date):
    booking = {
        "customer": customer,
        "room_no": room_no,
        "date": date
    }
    collection.insert_one(booking)


def view_bookings():
    return collection.find()


def cancel_booking(customer):
    collection.delete_one({"customer": customer})
