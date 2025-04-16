from service.driver_service import DriverService
from service.trip_service import TripService

class DriverPanel:
    def __init__(self, driver):
        self.driver = driver
        self.driver_id = driver.get_driver_id()
        self.driver_service = DriverService()
        self.trip_service = TripService()

    def show_menu(self):
        while True:
            print(f"\n===== Driver Panel (ID: {self.driver_id} - {self.driver.get_name()}) =====")
            print("1. View My Scheduled Trips")
            print("2. Start Trip")
            print("3. Complete Trip")
            print("4. Report Issue")
            print("5. View My Details")
            print("6. Logout")
            choice = input("Enter choice: ")

            if choice == "1":
                self.view_my_trips()
            elif choice == "2":
                self.start_trip()
            elif choice == "3":
                self.complete_trip()
            elif choice == "4":
                self.report_issue()
            elif choice == "5":
                self.view_my_details()
            elif choice == "6":
                print("👋 Logging out...")
                break
            else:
                print("❌ Invalid choice")

    def view_my_trips(self):
        try:
            trips = self.driver_service.get_driver_trips(self.driver_id)
            if not trips:
                print("No trips assigned")
                return

            print("\n🛣️ Your Scheduled Trips:")
            for trip in trips:
                status = trip.get_status()
                if status == "In Progress":
                    status_display = "✅ In Progress"
                elif status == "Completed":
                    status_display = "🏁 Completed"
                else:
                    status_display = "🕒 Upcoming"
                print(f"Trip {trip.get_trip_id()}: {trip.get_departure_date()} to {trip.get_arrival_date()} [{status_display}]")
        except Exception as e:
            print(f"❌ Error: {e}")

    def start_trip(self):
        trip_id = int(input("Enter Trip ID to start: "))
        try:
            self.driver_service.start_trip(self.driver_id, trip_id)
            self.trip_service.update_trip_status(trip_id, "In Progress")
            print("✅ Trip started successfully")
        except (TripNotFoundException, InvalidDriverDataException) as e:
            print(f"❌ {e}")

    def complete_trip(self):
        trip_id = int(input("Enter Trip ID to complete: "))
        try:
            self.driver_service.complete_trip(self.driver_id, trip_id)
            self.trip_service.update_trip_status(trip_id, "Completed")
            print("✅ Trip completed successfully")
        except (TripNotFoundException, InvalidDriverDataException) as e:
            print(f"❌ {e}")

    def report_issue(self):
        trip_id = input("Enter Trip ID (or leave blank): ")
        issue = input("Describe the issue: ")
        try:
            self.driver_service.report_issue(self.driver_id, issue, trip_id or None)
            print("🚨 Issue reported to dispatch")
        except Exception as e:
            print(f"❌ Failed to report issue: {e}")

    def view_my_details(self):
        try:
            driver = self.driver_service.get_driver_by_id(self.driver_id)
            print(f"\n👤 Your Details:")
            print(f"Name: {driver.get_name()}")
            print(f"License: {driver.get_license_number()}")
            print(f"Status: {driver.get_status()}")
        except Exception as e:
            print(f"❌ Error loading details: {e}")
