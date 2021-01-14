import time
from locust import HttpUser, task


class QuickstartUser(HttpUser):
    token = ''

    @task
    def health(self):
        headers = {
            'Content-Type': 'application/json'
        }
        with self.client.get("/health/", headers=headers, catch_response=True) as response:
            # 因为错误码是我自己控制的，我里面是code为0是正常，然后10000为不可知的异常，其它为可控异常
            if response.status_code == 200 and response.json().get('code') == 10000:
                response.failure('返回码不正确')

    def on_start(self):
        '''
        on_start：设置了多少个用户，就会被调用多少次
        '''
        data = {
            'username': 'buxingxing',
            'password': '123456',
            'is_ldap': False,
        }
        data = self.client.post("/api/v1/account/user/login/", json=data)
        data = data.json()
        data = data.get('data')
        self.token = data.get('token')
