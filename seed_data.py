import csv
from pathlib import Path

from pymongo import UpdateOne

from database import clear_data_cache, db

DATASET_PATH = Path(__file__).with_name("hotel_dataset.csv")
hotel_collection = db["hotel_data"]
room_collection = db["rooms"]


def load_hotel_dataset(path=DATASET_PATH):
    hotels_by_name = {}
    rooms = []
    required_fields = {
        "hotel_name",
        "location",
        "rating",
        "room_number",
        "room_type",
        "price_per_night",
    }

    with path.open(newline="", encoding="utf-8-sig") as dataset_file:
        reader = csv.DictReader(dataset_file)
        if not reader.fieldnames or not required_fields.issubset(reader.fieldnames):
            raise ValueError(
                f"{path} must contain these columns: {', '.join(sorted(required_fields))}"
            )

        for row_number, row in enumerate(reader, start=2):
            name = row["hotel_name"].strip()
            location = row["location"].strip()
            room_no = row["room_number"].strip()
            room_type = row["room_type"].strip()
            if not all((name, location, room_no, room_type)):
                raise ValueError(
                    f"Missing required hotel or room value on row {row_number}"
                )

            try:
                rating = float(row["rating"])
                price = float(row["price_per_night"])
            except ValueError as error:
                raise ValueError(
                    f"Invalid rating or price on row {row_number}"
                ) from error

            if not 0 <= rating <= 5 or price < 0:
                raise ValueError(f"Rating or price out of range on row {row_number}")

            hotel = {"name": name, "location": location, "rating": rating}
            existing_hotel = hotels_by_name.setdefault(name, hotel)
            if existing_hotel != hotel:
                raise ValueError(
                    f"Inconsistent hotel details for {name} on row {row_number}"
                )

            rooms.append(
                {
                    "hotel_name": name,
                    "room_no": room_no,
                    "type": room_type,
                    "price": price,
                }
            )

    if not hotels_by_name or not rooms:
        raise ValueError(f"{path} does not contain any hotel rooms")

    return list(hotels_by_name.values()), rooms


def seed_hotel_dataset():
    hotels, rooms = load_hotel_dataset()

    hotel_operations = [
        UpdateOne(
            {
                "$or": [
                    {"name": hotel["name"]},
                    {"Hotel Name": hotel["name"]},
                    {"hotel_name": hotel["name"]},
                    {"hotel name": hotel["name"]},
                ]
            },
            {"$setOnInsert": hotel},
            upsert=True,
        )
        for hotel in hotels
    ]
    room_operations = [
        UpdateOne(
            {
                "$and": [
                    {
                        "$or": [
                            {"hotel_name": room["hotel_name"]},
                            {"hotel name": room["hotel_name"]},
                            {"Hotel Name": room["hotel_name"]},
                        ]
                    },
                    {
                        "$or": [
                            {"room_no": room["room_no"]},
                            {"room_number": room["room_no"]},
                            {"room number": room["room_no"]},
                        ]
                    },
                ]
            },
            {"$setOnInsert": room},
            upsert=True,
        )
        for room in rooms
    ]

    hotel_collection.bulk_write(hotel_operations, ordered=False)
    room_collection.bulk_write(room_operations, ordered=False)
    clear_data_cache()
    return len(hotels), len(rooms)
