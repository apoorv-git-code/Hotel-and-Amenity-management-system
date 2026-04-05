from db import customers
from customer_template import customer

def add_customer():
    name=input("Enter your name : ")
    contact=input("Enter your contact number : ")
    id=input("Enter your id : ")
    c1=customer(name,contact,id)
    customers.insert_one(c1.conversion_to_dict())
    print("Customer added successfully")

def view_customers():
     all_customers=customers.find()
     for i in all_customers:
        print("Name:",i["name"])
        print("contact:",i["contact"])
        print("id:",i["id"])

def find():
     key=input("Enter the name of the customer:")
     searched_person=customers.find_one({"name":key})
     if(searched_person):   # if person doesnot exist in database then it returns none so here we are checking whether there exists the person with the given name or not
      print(searched_person["name"])
      print(searched_person["id"])
      print(searched_person["contact"])
     else:
      print("Person does not exist ")

def update():
      name = input("Enter the name of the customer whose details is to be changed:")
      searched_person=customers.find_one({"name":name})
      if(searched_person):
        change=int(input("Enter the detail to be changed(1. contact  2. id)"))
        if(change==1):
          new_contact=input("Enter new contact number:")
          result=customers.update_one(
            {"name":name},
            {"$set":{"contact":new_contact}})
        elif(change==2):
          new_id=input("Enter new id:")
          result=customers.update_one(
            {"name":name},
            {"$set":{"id":new_id}})
        else:
          print("Invaid choice")
    
      else:
        print("User doesnot exist")
    
def delete():
      name=input("Enter the name of the customer to be deleted:")
      searched_person=customers.find_one({"name":name})
      if(searched_person):

        result=customers.delete_one({"name":name})
      else:
        print("Person not in database")
