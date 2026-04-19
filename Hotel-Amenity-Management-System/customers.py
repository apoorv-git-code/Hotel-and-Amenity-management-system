from database import db
from customer_template import Customer

collection = db["customers"]


def add_customer(name, contact, email_id, city):
    c1 = Customer(name, contact, email_id, city)
    return collection.insert_one(c1.to_dict()).inserted_id


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
        return collection.update_one({"name": name}, {"$set": updates})
    return None


def delete_customer(name):
    return collection.delete_one({"name": name})
