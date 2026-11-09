import streamlit as st

from customer_template import Customer
from database import clear_data_cache, db

collection = db["customers"]


def add_customer(name, contact, email_id, city):
    c1 = Customer(name, contact, email_id, city)
    result = collection.insert_one(c1.to_dict()).inserted_id
    clear_data_cache()
    return result


@st.cache_data(ttl=30, show_spinner=False)
def view_customers():
    return list(collection.find())


def find_customer(name):
    return collection.find_one({"name": name})


def update_customer(name, new_contact=None, new_email=None, new_city=None):
    updates = {}
    if new_contact:
        updates["contact"] = new_contact
    if new_email:
        updates["email_id"] = new_email
    if new_city:
        updates["city"] = new_city
    if updates:
        result = collection.update_one({"name": name}, {"$set": updates})
        if result.modified_count:
            clear_data_cache()
        return result
    return None


def delete_customer(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count:
        clear_data_cache()
    return result


if __name__ == "__main__":
    print("Customers:")
    for c in view_customers():
        print(c)
