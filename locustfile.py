import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/integral/0/3.14159")
