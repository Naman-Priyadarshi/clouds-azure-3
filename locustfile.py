from locust import HttpUser, task, between

class WebAppUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def home(self):
        self.client.get("/")

    @task(2)
    def numerical_integral(self):
        self.client.get("/numericalintegral/0/3.14")
