from pymongo import MongoClient 
client=MongoClient("mongodb://localhost:27017/")
db=client.hotel_db        # creating a database named hotel_db
customers=db.customers    # creating a collection named customers  
rooms=db.rooms            # creating a collection named rooms 
bookings=db.bookings      # creating a collection named bookings 
amenities=db.amenities    # creating a collection named amenities

