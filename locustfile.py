from locust import HttpUser, task, between
from locust import SequentialTaskSet, LoadTestShape

# User behavior for a banking application, defined using SequentialTaskSet
class BankingUserBehavior(SequentialTaskSet):

    @task
    def view_account(self):
        self.client.get("/", name="View Account Details")

    @task
    def perform_transaction(self):
        self.client.post("/", {"amount": "100", "to_account": "12345"}, name="Perform Transaction")

    @task
    def browse_offers(self):
        self.client.get("/", name="Browse Offers")

    # Simulating different availability zones with task weights
    @task(5)
    def load_az1(self):
        self.client.get("/?az=1", name="Load AZ1")

    @task(3)
    def load_az2(self):
        self.client.get("/?az=2", name="Load AZ2")

    @task(2)
    def load_az3(self):
        self.client.get("/?az=3", name="Load AZ3")

# The user class, defining the wait time and task set
class BankingUser(HttpUser):
    host = "http://127.0.0.1:55015"
    wait_time = between(1, 2)
    tasks = [BankingUserBehavior]

# A staged load shape to simulate different stages of load during the test
class StagedLoadShape(LoadTestShape):

    stages = [
    {"duration": 30, "users": 20, "spawn_rate": 1.0},
    {"duration": 60, "users": 40, "spawn_rate": 1.0},
    {"duration": 45, "users": 60, "spawn_rate": 1.0},
    {"duration": 120, "users": 80, "spawn_rate": 1.0},
    {"duration": 30, "users": 10, "spawn_rate": ""},
    {"duration": 50, "users": 0, "spawn_rate": 0.0}
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])
        return None
