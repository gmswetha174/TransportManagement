import unittest
from unittest.mock import MagicMock
from service.driver_service import DriverService
from entity.driver import Driver
from exceptions.exceptions import DriverNotFoundException, InvalidDriverDataException

class TestDriverService(unittest.TestCase):
    def setUp(self):
        self.service = DriverService()
        self.service.driver_dao = MagicMock()

    def test_add_driver_valid(self):
        driver = Driver(1, "John", "LIC123", "Available")
        self.service.driver_dao.add_driver.return_value = True
        result = self.service.add_driver(driver)
        self.assertTrue(result)

    def test_add_driver_invalid_name(self):
        driver = Driver(1, "", "LIC123", "Available")
        with self.assertRaises(InvalidDriverDataException):
            self.service.add_driver(driver)

    def test_get_driver_by_id_found(self):
        driver = Driver(1, "John", "LIC123", "Available")
        self.service.driver_dao.get_driver_by_id.return_value = driver
        self.assertEqual(self.service.get_driver_by_id(1), driver)

    def test_get_driver_by_id_not_found(self):
        self.service.driver_dao.get_driver_by_id.return_value = None
        with self.assertRaises(DriverNotFoundException):
            self.service.get_driver_by_id(1)

    def test_start_trip_with_valid_status(self):
        driver = Driver(1, "John", "LIC123", "Available")
        self.service.driver_dao.get_driver_by_id.return_value = driver
        self.service.driver_dao.update_driver_status.return_value = None
        self.assertTrue(self.service.start_trip(1, 101))

    def test_complete_trip_invalid_status(self):
        driver = Driver(1, "John", "LIC123", "Available")
        self.service.driver_dao.get_driver_by_id.return_value = driver
        with self.assertRaises(InvalidDriverDataException):
            self.service.complete_trip(1, 101)

if __name__ == '__main__':
    unittest.main()
