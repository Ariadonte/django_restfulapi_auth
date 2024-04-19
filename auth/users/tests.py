from django.test import TestCase
import random
import requests
import json


class TestUsers(TestCase):
    email = f'user{random.random() * 100}@example.com'

    def test_users(self):
        headers = {
            'Content-Type': 'application/json',
        }

        json_data = {
            'password': 'password',
            'email': self.email,
        }

        response = requests.post('http://localhost:8000/api/register/', headers=headers, json=json_data)
        self.assertEqual(response.status_code, 200)

        headers = {
            'Content-Type': 'application/json',
        }

        json_data = {
            'email': self.email,
            'password': 'password',
        }
        response = requests.post('http://localhost:8000/api/login/', headers=headers, json=json_data)
        response_dict = json.loads(response.text)
        self.refresh_token = response_dict["refresh_token"]
        self.assertEqual(response.status_code, 200)

        headers = {
            'Content-Type': 'application/json',
        }

        json_data = {
            'refresh_token': self.refresh_token,
        }

        response = requests.post('http://localhost:8000/api/refresh/', headers=headers, json=json_data)
        response_dict = json.loads(response.text)
        self.refresh_token = response_dict["refresh_token"]
        self.access_token = response_dict["access_token"]
        self.assertEqual(response.status_code, 200)

        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }

        response = requests.get('http://localhost:8000/api/me/', headers=headers)
        self.assertEqual(response.status_code, 200)

        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }

        json_data = {
            'email': self.email,
        }

        response = requests.get('http://localhost:8000/api/me/', headers=headers, json=json_data)
        self.assertEqual(response.status_code, 200)

        headers = {
            'Content-Type': 'application/json',
        }

        json_data = {
            'refresh_token': self.refresh_token,
        }

        response = requests.post('http://localhost:8000/api/logout/', headers=headers, json=json_data)
        self.assertEqual(response.status_code, 200)
