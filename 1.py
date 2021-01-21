import math
import time
from locust import HttpUser, task, constant
from locust import LoadTestShape


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


class DoubleWave(LoadTestShape):
    """
    A shape to immitate some specific user behaviour. In this example, midday
    and evening meal times.
    Settings:
        min_users -- minimum users
        peak_one_users -- users in first peak
        peak_two_users -- users in second peak
        time_limit -- total length of test
    """

    min_users = 20
    peak_one_users = 60
    peak_two_users = 40
    time_limit = 600

    def tick(self):
        run_time = round(self.get_run_time())

        if run_time < self.time_limit:
            user_count = (
                (self.peak_one_users - self.min_users)
                * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 5) ** 2)
                + (self.peak_two_users - self.min_users)
                * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 10) ** 2)
                + self.min_users
            )
            return (round(user_count), round(user_count))
        else:
            return None
