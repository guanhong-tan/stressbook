from locust import HttpUser, task, between
import random
# Define the events and seating details
EVENTS = [
    {"event_id": "event_id_001", "name": "Music Fest 2024"},
    {"event_id": "event_id_002", "name": "Jazz Night 2024"},
    {"event_id": "event_id_003", "name": "Rock Legends 2024"}
]

SEAT_SECTIONS = [
    {"section": "333", "price": 200}, {"section": "332", "price": 200}, {"section": "309", "price": 200},
    {"section": "331", "price": 300}, {"section": "330", "price": 300}, {"section": "329", "price": 300},
    {"section": "328", "price": 300}, {"section": "327", "price": 300}, {"section": "326", "price": 300},
    {"section": "325", "price": 300}, {"section": "324", "price": 300}, {"section": "323", "price": 300},
    {"section": "322", "price": 300}, {"section": "320", "price": 300}, {"section": "319", "price": 300},
    {"section": "318", "price": 300}, {"section": "314", "price": 300}, {"section": "313", "price": 300},
    {"section": "312", "price": 300}, {"section": "311", "price": 300}, {"section": "310", "price": 300},
    {"section": "233", "price": 300}, {"section": "232", "price": 300}, {"section": "230", "price": 300},
    {"section": "229", "price": 300}, {"section": "213", "price": 300}, {"section": "212", "price": 300},
    {"section": "209", "price": 300}, {"section": "231", "price": 300}, {"section": "210", "price": 300},
    {"section": "211", "price": 300}, {"section": "114", "price": 300}, {"section": "219", "price": 300},
    {"section": "223", "price": 300}, {"section": "128", "price": 300}, {"section": "133", "price": 300},
    {"section": "132", "price": 300}, {"section": "131", "price": 300}, {"section": "130", "price": 300},
    {"section": "129", "price": 300}, {"section": "113", "price": 300}, {"section": "112", "price": 300},
    {"section": "111", "price": 300}, {"section": "110", "price": 300}, {"section": "109", "price": 300},
    {"section": "222", "price": 300}, {"section": "221", "price": 300}, {"section": "220", "price": 300},
    {"section": "228", "price": 300}, {"section": "227", "price": 300}, {"section": "226", "price": 300},
    {"section": "225", "price": 300}, {"section": "224", "price": 300}, {"section": "218", "price": 300},
    {"section": "217", "price": 300}, {"section": "216", "price": 300}, {"section": "215", "price": 300},
    {"section": "214", "price": 300}, {"section": "pa2", "price": 400}, {"section": "pb2", "price": 400},
    {"section": "234", "price": 300}, {"section": "208", "price": 300}, {"section": "pa1", "price": 500},
    {"section": "pb1", "price": 450}, {"section": "134", "price": 500}, {"section": "108", "price": 450}
]
class ConcertBookingUser(HttpUser):
    host = "http://127.0.0.1:5000"  # Replace 5000 with your Flask application's port
    wait_time = between(1, 2)  # Simulates user think time between tasks

    def on_start(self):
        """Simulate user login."""
        # Create 10,000 users if not created
        self.login()

    def login(self):
        """Log in the user."""
        user_id = random.randint(1, 10000)
        email = f"user_{user_id:05}@example.com"
        response = self.client.post("/login", data={"email": email, "password": "123123"})
        if response.status_code == 200:
            print(f"Logged in as {email}")
        else:
            print(f"Failed to log in as {email}")

    @task(3)
    def browse_events(self):
        """Simulate browsing events."""
        response = self.client.get("/events")
        if response.status_code == 200:
            print("Browsed events successfully.")
        else:
            print("Failed to browse events.")

    @task(5)
    def book_ticket(self):
        """Simulate booking tickets."""
        try:
            event = random.choice(EVENTS)
            seat = random.choice(SEAT_SECTIONS)
            quantity = random.randint(1, 4)

            with self.client.post("/booking/process", 
                data={
                    "event_id": event["event_id"],
                    "section": seat["section"],
                    "quantity": quantity,
                    "price": seat["price"]
                },
                catch_response=True) as response:
                
                if response.status_code == 200:
                    if "Booking successful" in response.text:
                        response.success()
                        print(f"Successfully booked {quantity} ticket(s) for {event['name']}")
                    else:
                        response.failure("Booking failed - no success message")
                else:
                    response.failure(f"Booking failed with status {response.status_code}")
        except Exception as e:
            print(f"Error in book_ticket task: {e}")

    @task(1)
    def view_booking(self):
        """Simulate viewing user bookings."""
        response = self.client.get("/user/bookings")
        if response.status_code == 200:
            print("Viewed bookings successfully.")
        else:
            print("Failed to view bookings.")
