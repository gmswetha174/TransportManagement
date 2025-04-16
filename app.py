from dao.passenger_dao import PassengerDAO 
from dao.booking_dao import BookingDAO 
from dao.trip_dao import TripDAO 
from dao.driver_dao import DriverDAO
from service.booking_service import BookingService 
from entity.passenger import Passenger 
from entity.booking import Booking 
from entity.driver import Driver
from exceptions.exceptions import BookingNotFoundException, InvalidBookingDataException 
from admin.admin import Admin 
from driver.driver_panel import DriverPanel 

# Initialize DAOs and Services 
passenger_dao = PassengerDAO() 
booking_dao = BookingDAO() 
booking_service = BookingService() 
trip_dao = TripDAO()
driver_dao = DriverDAO()

def add_passenger(): 
    try: 
        print("\n📝 Register as a New Customer:") 
        name = input("Enter Name: ") 
        gender = input("Enter Gender (Male/Female/Other): ").capitalize() 
        if gender not in ['Male', 'Female', 'Other']: 
            print("❌ Invalid gender.")
            return 

        try: 
            age = int(input("Enter Age: ").strip()) 
            if age < 0 or age > 120: 
                print("❌ Invalid age.")
                return 
        except ValueError: 
            print("❌ Age must be a number.")
            return 

        email = input("Enter Email: ") 
        contact = input("Enter Contact: ") 
        if not contact.isdigit() or len(contact) < 10 or len(contact) > 15: 
            print("❌ Invalid contact number.")
            return 

        password = input("Set a Password: ").strip()
        if len(password) < 6:
            print("❌ Password must be at least 6 characters.")
            return

        passenger = Passenger(None, name, age, contact)
        passenger.set_gender(gender) 
        passenger.set_email(email) 
        passenger.set_password(password)

        passenger_dao.add_passenger(passenger) 
        print("✅ Registration successful!") 
    except Exception as e: 
        print(f"❌ Error adding passenger: {e}") 

def view_all_data(): 
    try: 
        print("\n🧍‍♂️ Registered Passengers:")
        passengers = passenger_dao.get_all_passengers() 
        for p in passengers: 
            print(p) 
    except Exception as e: 
        print(f"❌ Error fetching passengers: {e}") 

def view_available_trips(): 
    try: 
        print("\n🚌 Available Trips:")
        trips = trip_dao.get_available_trips() 
        if trips: 
            for trip in trips: 
                print(f"TripID: {trip[0]} DepartureDate: {trip[3]}, ArrivalDate: {trip[4]}, MaxPassengers: {trip[7]}\n") 
        else: 
            print("❌ No trips available at the moment.") 
    except Exception as e: 
        print(f"❌ Error fetching trips: {e}") 

def book_trip(): 
    try: 
        view_available_trips() 
        print("\n🚌 Book a Trip:") 
        trip_id = int(input("Enter Trip ID: ")) 
        passenger_id = int(input("Enter Passenger ID: ")) 
        booking_date = input("Enter Booking Date (YYYY-MM-DD): ") 
        status = "Confirmed" 

        booking = Booking(None, trip_id, passenger_id, booking_date, status) 
        booking_id = booking_service.book_ticket(booking) 
        print(f"✅ Booking successful! Your Booking ID is: {booking_id}") 
    except Exception as e: 
        print(f"❌ Error booking trip: {e}") 

def view_my_bookings(passenger_id): 
    try: 
        print("\n📘 Your Latest Booking:")
        booking = booking_service.get_latest_booking_by_passenger_id(passenger_id) 
        if booking: 
            print(booking) 
        else: 
            print("❌ No bookings found.") 
    except Exception as e: 
        print(f"❌ Error fetching bookings: {e}") 

def view_past_trips(passenger_id: int): 
    try: 
        print("\n📚 Your Past Trips:")
        past_trips = booking_service.get_past_bookings_by_passenger_id(passenger_id) 
        if past_trips: 
            for trip in past_trips: 
                print(f"BookingID: {trip[0]}, TripID: {trip[1]}, BookingDate: {trip[3]}, Status: {trip[4]}, "
                      f"DepartureDate: {trip[5]}, ArrivalDate: {trip[6]}, RouteID: {trip[7]}") 
        else: 
            print("❌ No past trips found.") 
    except Exception as e: 
        print(f"❌ Error fetching past trips: {e}") 

def cancel_booking(passenger_id: int): 
    try: 
        print("\n🛑 Cancel a Booking:") 
        booking_id = int(input("Enter Booking ID to cancel: ")) 
        booking_service.cancel_booking(booking_id, passenger_id) 
        print(f"✅ Booking with ID {booking_id} has been successfully canceled.") 
    except BookingNotFoundException as e: 
        print(f"❌ {e}") 
    except InvalidBookingDataException as e: 
        print(f"❌ {e}") 
    except Exception as e: 
        print(f"❌ Error canceling booking: {e}") 

def customer_menu(): 
    try: 
        print("\n👤 Welcome to Customer Login!") 
        is_new_user = input("Are you a new user? (yes/no): ").strip().lower() 

        if is_new_user == "yes": 
            add_passenger() 
            book_now = input("Do you want to book a trip? (yes/no): ").strip().lower() 
            if book_now == "yes": 
                book_trip() 
            return 

        elif is_new_user == "no": 
            pid = int(input("Enter your Passenger ID: ")) 
            password = input("Enter your Password: ").strip()
            passenger = passenger_dao.login_passenger_by_id(pid, password)
            if not passenger:
                print("❌ Invalid credentials.")
                return
            print(f"\n👋 Welcome back, {passenger.get_first_name()}!") 
            while True: 
                print("\n===== Customer Panel =====") 
                print("1. 🚌 Book a Trip") 
                print("2. 🛑 Cancel Booking") 
                print("3. 📚 View Past Trips") 
                print("4. 📘 View Latest Trip") 
                print("5. 🚪 Logout") 
                choice = input("Enter choice: ") 

                if choice == "1": 
                    book_trip() 
                elif choice == "2": 
                    cancel_booking(pid) 
                elif choice == "3": 
                    view_past_trips(pid) 
                elif choice == "4": 
                    view_my_bookings(pid) 
                elif choice == "5": 
                    print("👋 Logging out. Have a nice day!") 
                    break 
                else: 
                    print("❌ Invalid choice. Try again.") 
        else: 
            print("❌ Invalid input. Please enter 'yes' or 'no'.") 
    except Exception as e: 
        print(f"❌ Error in customer menu: {e}") 

def driver_menu():
    try:
        print("\n🧑‍✈️ Welcome to Driver Login!")
        driver_id = int(input("Enter your Driver ID: "))
        password = input("Enter your Password: ").strip()
        driver = driver_dao.validate_driver_login(driver_id, password)
        if not driver:
            print("❌ Invalid credentials.")
            return
        print(f"\n👋 Welcome, {driver.get_name()}!")
        DriverPanel(driver).show_menu()
    except Exception as e:
        print(f"❌ Error in driver menu: {e}")

def admin_menu():
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()
    if username != "admin" or password != "admin123":
        print("❌ Invalid admin credentials.")
        return

    while True: 
        print("\n===== Admin Menu =====") 
        print("1. Manage Trips") 
        print("2. Manage Bookings") 
        print("3. Manage Passengers") 
        print("4. Manage Vehicles") 
        print("5. Manage Routes") 
        print("6. Manage Drivers") 
        print("7. Reports and Analytics") 
        print("8. Logout") 
        choice = input("Enter choice: ") 

        if choice == "1":
            Admin.manage_trips()
        elif choice == "2":
            Admin.manage_bookings()
        elif choice == "3":
            Admin.manage_passengers()
        elif choice == "4":
            Admin.manage_vehicles()
        elif choice == "5":
            Admin.manage_routes()
        elif choice == "6":
            Admin.manage_drivers()
        elif choice == "7":
            Admin.reports_and_analytics()
        elif choice == "8":
            print("👋 Logging out of Admin panel.")
            break
        else:
            print("❌ Invalid choice.")

def main():
    while True:
        print("\n====== 🚍 Transport System Management ======")
        print("1. Admin Login")
        print("2. Customer Login")
        print("3. Driver Login")
        print("4. Exit")
        option = input("Select an option: ")

        if option == "1":
            admin_menu()
        elif option == "2":
            customer_menu()
        elif option == "3":
            driver_menu()
        elif option == "4":
            print("👋 Exiting system. Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
