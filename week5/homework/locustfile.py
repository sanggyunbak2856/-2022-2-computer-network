from locust import HttpUser, between, task

class User(HttpUser):
    
    wait_time = between(1, 5)
    
    @task
    def get_index(self):
        self.client.get('/')
        self.client.get('/index.html')
        self.client.get('/201702011.html')
        self.client.get('/notfound.html')
        self.client.get('/mystyle.css')
        self.client.get('/myscript.js')
        self.client.get('/myimage.jpg')
