import gui
from customers import (add_customer,view_customers,find,update,delete)
from rooms import view_rooms
while(True):
    print("1. Add \n2. View all customers \n3. view particular customer \n4.update \n5.delete \n6.view rooms \n7.exit")
    choice=int(input("Enter your choice : "))
    if(choice==1):
        add_customer()
    elif(choice==2):
        view_customers()
    elif(choice==3):
        find()
    elif(choice==4):
        update()
    elif(choice==5):
        delete()
    elif(choice==6):
        view_rooms()
    elif(choice==7):
        break
    else:
        print("Invalid choice")


