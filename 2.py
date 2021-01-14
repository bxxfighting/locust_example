import time
from locust import HttpUser, task
from locust.contrib.fasthttp import FastHttpUser


class QuickstartUser(FastHttpUser):
    token = ''

    @task
    def health(self):
        headers = {
            'Content-Type': 'application/json'
        }
        with self.client.get("/health/", headers=headers, catch_response=True) as response:
            if response.status_code == 200 and response.json().get('code') != 0:
                response.failure('返回码不正确')

    def on_start(self):
        data = {
            'username': 'buxingxing',
            'password': '123456',
            'is_ldap': False,
        }
        data = self.client.post("/api/v1/account/user/login/", json=data)
        data = data.json()
        data = data.get('data')
        self.token = data.get('token')
