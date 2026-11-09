import unittest
from unittest.mock import patch

from booking import add_booking


class AddBookingTests(unittest.TestCase):
    @patch("booking.clear_data_cache")
    @patch("booking.collection.insert_one")
    def test_saves_hotel_name_for_room_availability(self, insert_one, clear_data_cache):
        insert_one.return_value.inserted_id = "booking-id"

        result = add_booking(
            "Guest",
            "101",
            "2026-11-10",
            "2026-11-11",
            booked_by="guest-user",
            hotel_name="Harbor Hotel",
        )

        self.assertEqual(result, "booking-id")
        self.assertEqual(
            insert_one.call_args.args[0],
            {
                "customer": "Guest",
                "room_no": "101",
                "date": "2026-11-10",
                "checkout_date": "2026-11-11",
                "booked_by": "guest-user",
                "hotel_name": "Harbor Hotel",
            },
        )
        clear_data_cache.assert_called_once_with()

    @patch("booking.clear_data_cache")
    @patch("booking.collection.insert_one")
    def test_keeps_existing_call_shape(self, insert_one, clear_data_cache):
        insert_one.return_value.inserted_id = "booking-id"

        add_booking("Guest", "101", "2026-11-10")

        self.assertNotIn("hotel_name", insert_one.call_args.args[0])
        clear_data_cache.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
