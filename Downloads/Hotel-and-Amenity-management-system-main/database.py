import os

import streamlit as st
from pymongo import MongoClient

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("MONGODB_DATABASE", "hotel_management")


@st.cache_resource
def get_client(uri: str) -> MongoClient:
    return MongoClient(
        uri,
        appname="HotelAmenityManagement",
        connectTimeoutMS=5000,
        serverSelectionTimeoutMS=5000,
        maxPoolSize=50,
    )


def clear_data_cache() -> None:
    st.cache_data.clear()


client = get_client(MONGODB_URI)
db = client[DATABASE_NAME]
hotels = db["hotel_data"]
rooms = db["rooms"]
amenities = db["amenities"]
bookings = db["bookings"]
customers = db["customers"]
users = db["users"]

if __name__ == "__main__":
    client.admin.command("ping")
    print("Connected to MongoDB database:")
    print("Database:", db.name)
    print("Collections:", db.list_collection_names())
