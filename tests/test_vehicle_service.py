import unittest
from unittest.mock import MagicMock
from service.vehicle_service import VehicleService
from entity.vehicle import Vehicle
from exceptions.exceptions import InvalidVehicleDataException, VehicleNotFoundException

class TestVehicleService(unittest.TestCase):
    def setUp(self):
        self.service = VehicleService()
        self.service.vehicle_dao = MagicMock()

    def test_add_vehicle_valid(self):
        vehicle = Vehicle(1, "Volvo", "Truck", 5, "Available")
        self.service.vehicle_dao.add_vehicle.return_value = None
        self.assertTrue(self.service.add_vehicle(vehicle))

    def test_add_vehicle_invalid_capacity(self):
        vehicle = Vehicle(1, "Volvo", "Truck", -1, "Available")
        with self.assertRaises(InvalidVehicleDataException):
            self.service.add_vehicle(vehicle)

    def test_get_vehicle_by_id_found(self):
        vehicle = Vehicle(1, "Volvo", "Van", 5, "Available")
        self.service.vehicle_dao.get_vehicle_by_id.return_value = vehicle
        self.assertEqual(self.service.get_vehicle_by_id(1), vehicle)

    def test_get_vehicle_by_id_not_found(self):
        self.service.vehicle_dao.get_vehicle_by_id.return_value = None
        with self.assertRaises(VehicleNotFoundException):
            self.service.get_vehicle_by_id(1)

    def test_update_vehicle_invalid_type(self):
        vehicle = Vehicle(1, "Tesla", "Bike", 3, "Available")
        with self.assertRaises(InvalidVehicleDataException):
            self.service.update_vehicle(vehicle)

if __name__ == '__main__':
    unittest.main()
