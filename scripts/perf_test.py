from locust import task, HttpUser


class ConverterTasks(HttpUser):

    @task
    def get_intent_static(self):
        self.client.get('/api/intent?sentence=trouve%20des%20toilette')
