from locust import HttpUser, task

class User(HttpUser):
    @task
    def get_index(self):
        self.client.get('/')
        self.client.get('/index.html')
        self.client.get('/201702011.html')
        self.client.get('/notfound.html')
        self.client.get('/mystyle.css')
        self.client.get('/myscript.js')
        self.client.get('/myimage.jpg')
