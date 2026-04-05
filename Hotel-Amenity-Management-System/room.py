from db import rooms

rooms.insert_many([
    {"room_no":"101", "type":"single" , "price":1234},
    {"room_no":"102", "type":"double" , "price":2345},
    {"room_no":"103", "type":"triple" , "price":3456},
    
    {"room_no":"201", "type":"single" , "price":1456},
    {"room_no":"202", "type":"double" , "price":2654},
    {"room_no":"203", "type":"triple" , "price":3987},
                
    {"room_no":"301", "type":"single" , "price":1098},
    {"room_no":"302", "type":"double" , "price":2987},
    {"room_no":"303", "type":"triple" , "price":3789},     
       ])

def view_rooms():
    all_rooms=rooms.find()

    for i in all_rooms:
        print("Room no.=",i["room_no"])
        print("type of room =",i["type"])
        print("Price=",i["price"],"\n")
