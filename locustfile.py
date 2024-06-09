from locust import HttpUser, TaskSet, task, between, constant


class MasterClassTasks(TaskSet):
    @task(100)
    def get_all_masterclasses(self):
        self.client.get("/api/masterclasses/")

    @task(100)
    def get_all_categories(self):
        self.client.get("/api/masterclasses/categories/")

    @task(80)
    def get_cities(self):
        self.client.get("/api/masterclasses/cities/")

    @task(40)
    def filter_masterclasses_by_category(self):
        self.client.get("/api/masterclasses/?categories=1")

    @task(40)
    def filter_masterclasses_by_locality(self):
        self.client.get("/api/masterclasses/?locality=Тольятти")

    @task(40)
    def filter_masterclasses_by_time(self):
        self.client.get("/api/masterclasses/?start_date=2024-06-01T00:00:00Z&end_date=2024-06-30T23:59:59Z")

    @task(20)
    def filter_masterclasses_by_combination(self):
        self.client.get("/api/masterclasses/?categories=1&locality=Тольятти&start_date=2024-06-01T00:00:00Z&end_date=2024-06-30T23:59:59Z")

    @task(50)
    def search_masterclasses(self):
        self.client.get("/api/masterclasses/?search=программирование")


class WebsiteUser(HttpUser):
    tasks = [MasterClassTasks]
    wait_time = between(0, 0.02)
    host = "http://localhost:8000"


if __name__ == "__main__":
    import os

    os.system("locust -f your_script_name.py --users 100 --spawn-rate 100")
