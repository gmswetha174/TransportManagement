from dao.passenger_dao import PassengerDAO
from entity.passenger import Passenger
from exceptions.exceptions import PassengerNotFoundException, InvalidPassengerDataException

class PassengerService:
    def __init__(self):
        self.passenger_dao = PassengerDAO()

    def add_passenger(self, passenger: Passenger) -> bool:
        if not passenger.get_first_name() or not passenger.get_email() or not passenger.get_phone_number() or not passenger.get_password():
            raise InvalidPassengerDataException("First Name, Email, Phone Number, and Password are required.")
        if passenger.get_gender() not in ['Male', 'Female', 'Other']:
            raise InvalidPassengerDataException("Invalid gender. Allowed values: Male, Female, Other.")
        if passenger.get_age() < 0:
            raise InvalidPassengerDataException("Age must be a non-negative number.")
        return self.passenger_dao.add_passenger(passenger)

    def get_passenger_by_id(self, passenger_id: int) -> Passenger:
        passenger = self.passenger_dao.get_passenger_by_id(passenger_id)
        if not passenger:
            raise PassengerNotFoundException(f"Passenger with ID {passenger_id} not found.")
        return passenger

    


    def get_all_passengers(self):
        return self.passenger_dao.get_all_passengers()

    def update_passenger(self, passenger: Passenger) -> bool:
        if not passenger.get_first_name() or not passenger.get_email() or not passenger.get_password():
            raise InvalidPassengerDataException("First Name, Email, and Password are required.")
        if passenger.get_gender() not in ['Male', 'Female', 'Other']:
            raise InvalidPassengerDataException("Invalid gender. Allowed values: Male, Female, Other.")
        if passenger.get_age() < 0:
            raise InvalidPassengerDataException("Age must be a non-negative number.")
        return self.passenger_dao.update_passenger(passenger)

    def delete_passenger(self, passenger_id: int) -> bool:
        return self.passenger_dao.delete_passenger(passenger_id)

    def login_passenger(self, name: str, password: str) -> Passenger:
        passenger = self.passenger_dao.login_passenger(name, password)
        if not passenger:
            raise PassengerNotFoundException("Invalid name or password.")
        return passenger

    def login_passenger_by_id(self, passenger_id: int, password: str) -> Passenger:
        passenger = self.passenger_dao.login_passenger_by_id(passenger_id, password)
        if not passenger:
            raise PassengerNotFoundException("Invalid Passenger ID or Password.")
        return passenger
