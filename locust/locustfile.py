from locust import HttpUser, task, between
import random


class DeviceMonitorUser(HttpUser):
    wait_time = between(1, 3)
    token: str = None

    def on_start(self):
        self.register_and_login()

    def register_and_login(self):
        username = f"user_{random.randint(1, 999999)}"
        password = "testpass123"

        self.client.post("/auth/register/", json={
            "username": username,
            "password": password,
            "confirm_password": password
        })

        response = self.client.post("/auth/login/", json={
            "username": username,
            "password": password
        })

        self.token = response.cookies.get("user_access_token")
        self.device_id = self.create_device()

    def create_device(self) -> str | None:
        response = self.client.post(
            "/devices/",
            json={"name": f"device_{random.randint(1, 9999)}"},
            cookies={"user_access_token": self.token}
        )
        if response.status_code == 200:
            return response.json().get("id")
        return None

    @task(5)
    def send_measurement(self):
        if not self.device_id:
            return
        self.client.post(
            f"/devices/{self.device_id}/stats/",
            json={
                "x": random.uniform(-100, 100),
                "y": random.uniform(-100, 100),
                "z": random.uniform(-100, 100)
            },
            cookies={"user_access_token": self.token}
        )

    @task(1)
    def get_stats(self):
        if not self.device_id or not self.token:
            return
        with self.client.get(
            f"/devices/{self.device_id}/stats/",
            cookies={"user_access_token": self.token},
            catch_response=True
        ) as response:
            if response.status_code in (200, 404):
                response.success()

    @task(1)
    def get_aggregated_stats(self):
        with self.client.get(
            "/users/me/stats/",
            cookies={"user_access_token": self.token},
            catch_response=True
        ) as response:
            if response.status_code in (200, 404):
                response.success()
