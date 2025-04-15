from util.db_connection import DBConnUtil
from entity.passenger import Passenger

class PassengerDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def add_passenger(self, passenger: Passenger):
        query = "INSERT INTO Passengers (FirstName, Gender, Age, Email, PhoneNumber, Password) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (
            passenger.get_first_name(),
            passenger.get_gender(),
            passenger.get_age(),
            passenger.get_email(),
            passenger.get_phone_number(),
            passenger.get_password()
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_all_passengers(self):
        query = "SELECT PassengerID, FirstName, Age, PhoneNumber, Gender, Email FROM Passengers"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        passengers = []
        for row in rows:
            passenger = Passenger(
                passenger_id=row[0],
                first_name=row[1],
                age=row[2],
                phone_number=row[3],
                gender=row[4],
                email=row[5]
            )
            passengers.append(passenger)
        return passengers

    def get_passenger_by_id(self, passenger_id: int):
        query = "SELECT PassengerID, FirstName, Gender, Age, Email, PhoneNumber, Password FROM Passengers WHERE PassengerID = %s"
        self.cursor.execute(query, (passenger_id,))
        row = self.cursor.fetchone()
        if row:
            passenger = Passenger(
                passenger_id=row[0],
                first_name=row[1],
                gender=row[2],
                age=row[3],
                email=row[4],
                phone_number=row[5],
                password=row[6]
            )
            return passenger
        return None

    def update_passenger(self, passenger: Passenger):
        query = """
            UPDATE Passengers
            SET FirstName = %s, Gender = %s, Age = %s, Email = %s, PhoneNumber = %s, Password = %s
            WHERE PassengerID = %s
        """
        values = (
            passenger.get_first_name(),
            passenger.get_gender(),
            passenger.get_age(),
            passenger.get_email(),
            passenger.get_phone_number(),
            passenger.get_password(),
            passenger.get_passenger_id()
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_passenger(self, passenger_id: int):
        query = "DELETE FROM Passengers WHERE PassengerID = %s"
        self.cursor.execute(query, (passenger_id,))
        self.conn.commit()

    def login_passenger_by_id(self, passenger_id: int, password: str):
        query = """
            SELECT PassengerID, FirstName, Gender, Age, Email, PhoneNumber, Password 
            FROM Passengers 
            WHERE PassengerID = %s AND Password = %s
        """
        self.cursor.execute(query, (passenger_id, password))
        row = self.cursor.fetchone()
        if row:
            return Passenger(
                passenger_id=row[0],
                first_name=row[1],
                gender=row[2],
                age=row[3],
                email=row[4],
                phone_number=row[5],
                password=row[6]
            )
        return None

