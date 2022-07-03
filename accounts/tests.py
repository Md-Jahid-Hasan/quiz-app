from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('accounts:user-list')
TOKEN_URL = reverse('accounts:login')


def create_user(**param):
    return get_user_model().objects.create_user(**param)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        payload = {
            'email': 'jahidhadiu@gmail.com',
            'password': '1234abcd',
            'confirm_password': '1234abcd',
            'username': "jahid"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_token_for_user(self):
        payload = {
            'password': '1234abcd',
            'username': "jahid"
        }
        create_user(**payload, email="jahidhadiu@gmail.com")
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        create_user(username="jahid", email='jahid@gmail.com', password='123456')
        payload = {
            'username': 'jahid',
            'password': '1234abcd',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

