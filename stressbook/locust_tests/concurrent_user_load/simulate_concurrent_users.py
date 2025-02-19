from locust import HttpUser, task, between , TaskSet
import random

class UserBehavior(TaskSet):
    user_count = 0  # Shared counter to ensure unique user data

    @task
    def create_user(self):
        # Generate unique user data
        UserBehavior.user_count += 1
        email = f"user_{UserBehavior.user_count:05}@example.com"
        password = "123123"
        name = f"User {UserBehavior.user_count}"

        # Send POST request to create the user
        response = self.client.post(
            "/register",
            data={"name": name, "email": email, "password": password}
        )

        # Check response status
        if response.status_code == 200:
            print(f"User created successfully: {email} with status code {response.status_code}")
        elif response.status_code == 409:  # Assuming 409 means "email already exists"
            print(f"User already exists: {email}")
        else:
            print(f"Failed to create user: {email} with status code {response.status_code}")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)  # Simulates user "thinking time" between requests

