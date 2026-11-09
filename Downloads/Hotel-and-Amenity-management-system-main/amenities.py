import streamlit as st

from database import clear_data_cache, db

collection = db["amenities"]


class Amenity:
    def __init__(self, name, description):
        self.name = name
        self.description = description


def add_amenity(name, description):
    amenity = {"name": name, "description": description}
    result = collection.insert_one(amenity).inserted_id
    clear_data_cache()
    return result


@st.cache_data(ttl=30, show_spinner=False)
def view_amenities():
    return list(collection.find())


def delete_amenity(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count:
        clear_data_cache()
    return result


if __name__ == "__main__":
    print("Amenities:")
    for a in view_amenities():
        print(a)
