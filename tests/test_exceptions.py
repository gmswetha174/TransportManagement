import unittest

from exceptions.InvalidVehicleDataException import InvalidVehicleDataException
from exceptions.TripNotFoundException import TripNotFoundException

class TestCustomExceptions(unittest.TestCase):

    def test_invalid_vehicle_data_exception(self):
        with self.assertRaises(InvalidVehicleDataException):
            raise InvalidVehicleDataException("Invalid vehicle data provided.")

    def test_trip_not_found_exception(self):
        with self.assertRaises(TripNotFoundException):
            raise TripNotFoundException("Trip not found in database.")

if __name__ == '__main__':
    unittest.main()
