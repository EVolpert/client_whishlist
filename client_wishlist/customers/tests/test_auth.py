import json

from django.conf import settings
from django.test import TestCase, Client

import jwt

from customers.models import Customer
from customers.auth import authenticate


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        customer_name = 'Teste'
        customer_email = 'teste@teste.com'
        self.customer = Customer(name=customer_name, email=customer_email)
        self.customer.save()
        self.base_request_data = {
            "name": customer_name,
            "email": customer_email
        }

    def test_valid_response(self):
        data = json.dumps(self.base_request_data)
        response = self.client.post('/login', data, content_type="application/json")

        self.assertEqual(response.status_code, 200)

    def test_invalid_response(self):
        request_data = self.base_request_data
        request_data['name'] = 'Not Test'

        data = json.dumps(request_data)
        response = self.client.post('/login', data, content_type="application/json")

        self.assertEqual(response.status_code, 401)


class AuthenticationTestCase(TestCase):
    def setUp(self):
        customer_name = 'Teste'
        customer_email = 'teste@teste.com'
        self.customer = Customer(name=customer_name, email=customer_email)
        self.customer.save()
        token_payload = {"id": self.customer.id}
        self.token = jwt.encode(token_payload, settings.JWT_SECRET, algorithm='HS256')

    def test_valid_token_decode(self):
        decoded_token = authenticate(customer_id=self.customer.id, token=self.token)

        self.assertTrue(decoded_token)

    def test_invalid_customer_id_for_token(self):
        wrong_id = self.customer.id + 1
        decoded_token = authenticate(customer_id=wrong_id, token=self.token)

        self.assertFalse(decoded_token)

    def test_invalid_token(self):
        wrong_token = self.token[:-1]
        decoded_token = authenticate(customer_id=self.customer.id, token=wrong_token)

        self.assertFalse(decoded_token)