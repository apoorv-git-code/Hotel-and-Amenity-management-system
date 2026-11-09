import unittest
from unittest.mock import patch

from seed_data import load_hotel_dataset, seed_hotel_dataset


class HotelDatasetTests(unittest.TestCase):
    def test_loads_bundled_hotels_and_rooms(self):
        hotels, rooms = load_hotel_dataset()

        self.assertEqual(len(hotels), 8)
        self.assertEqual(len(rooms), 29)
        self.assertEqual(
            hotels[0],
            {"name": "Taj Palace", "location": "Mumbai", "rating": 5.0},
        )
        self.assertEqual(
            rooms[0],
            {
                "hotel_name": "Taj Palace",
                "room_no": "101",
                "type": "Single",
                "price": 4500.0,
            },
        )

    @patch("seed_data.clear_data_cache")
    @patch("seed_data.room_collection.bulk_write")
    @patch("seed_data.hotel_collection.bulk_write")
    @patch("seed_data.UpdateOne", side_effect=lambda *args, **kwargs: (args, kwargs))
    def test_seeds_idempotent_upserts(
        self, update_one, hotel_bulk_write, room_bulk_write, clear_data_cache
    ):
        result = seed_hotel_dataset()

        self.assertEqual(result, (8, 29))
        self.assertEqual(hotel_bulk_write.call_count, 1)
        self.assertEqual(room_bulk_write.call_count, 1)
        self.assertEqual(len(hotel_bulk_write.call_args.args[0]), 8)
        self.assertEqual(len(room_bulk_write.call_args.args[0]), 29)
        self.assertEqual(update_one.call_count, 37)
        self.assertTrue(
            all(
                call.kwargs["upsert"]
                for call in update_one.call_args_list
            )
        )
        self.assertTrue(
            all(
                "$setOnInsert" in call.args[1]
                for call in update_one.call_args_list
            )
        )
        clear_data_cache.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
