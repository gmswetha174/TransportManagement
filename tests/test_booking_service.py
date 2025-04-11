import unittest
from unittest.mock import MagicMock
from service.booking_service import BookingService
from entity.booking import Booking
from exceptions.exceptions import BookingNotFoundException, InvalidBookingDataException

class TestBookingService(unittest.TestCase):
    def setUp(self):
        self.service = BookingService()
        self.service.booking_dao = MagicMock()

    def test_book_ticket_valid(self):
        booking = Booking(1, 2, 3, "2024-01-01", "Confirmed")
        self.service.booking_dao.book_ticket.return_value = None
        self.assertTrue(self.service.book_ticket(booking))

    def test_book_ticket_invalid_status(self):
        booking = Booking(1, 2, 3, "2024-01-01", "Waiting")
        with self.assertRaises(InvalidBookingDataException):
            self.service.book_ticket(booking)

    def test_get_booking_by_id_valid(self):
        booking = Booking(1, 2, 3, "2024-01-01", "Confirmed")
        self.service.booking_dao.get_booking_by_id.return_value = booking
        self.assertEqual(self.service.get_booking_by_id(1, 3), booking)

    def test_get_booking_by_id_wrong_passenger(self):
        booking = Booking(1, 2, 4, "2024-01-01", "Confirmed")
        self.service.booking_dao.get_booking_by_id.return_value = booking
        with self.assertRaises(InvalidBookingDataException):
            self.service.get_booking_by_id(1, 3)

    def test_cancel_booking_already_cancelled(self):
        booking = Booking(1, 2, 3, "2024-01-01", "Cancelled")
        self.service.booking_dao.get_booking_by_id.return_value = booking
        with self.assertRaises(InvalidBookingDataException):
            self.service.cancel_booking(1, 3)

if __name__ == '__main__':
    unittest.main()
