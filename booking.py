import streamlit as st
from bson.errors import InvalidId
from bson.objectid import ObjectId

from database import clear_data_cache, db

collection = db["bookings"]


class Booking:
    def __init__(self, customer, room_no, date, checkout_date=None, booked_by=None):
        self.customer = customer
        self.room_no = room_no
        self.date = date
        self.checkout_date = checkout_date
        self.booked_by = booked_by


def add_booking(
    customer, room_no, date, checkout_date=None, booked_by=None, hotel_name=None
):
    booking = {
        "customer": customer,
        "room_no": room_no,
        "date": date,
        "checkout_date": checkout_date,
    }
    if booked_by:
        booking["booked_by"] = booked_by
    if hotel_name:
        booking["hotel_name"] = hotel_name
    result = collection.insert_one(booking).inserted_id
    clear_data_cache()
    return result


@st.cache_data(ttl=30, show_spinner=False)
def view_bookings():
    return list(collection.find())


def cancel_booking(booking_id):
    try:
        result = collection.delete_one({"_id": ObjectId(booking_id)})
    except InvalidId:
        return None
    if result.deleted_count:
        clear_data_cache()
    return result


if __name__ == "__main__":
    print("Bookings:")
    for b in view_bookings():
        print(b)
