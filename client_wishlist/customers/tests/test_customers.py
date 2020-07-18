import json

from django.conf import settings
from django.test import TestCase, Client

import jwt

from customers.models import Customer


class CustomerListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer_name_1 = 'Teste'
        self.customer_email_1 = 'teste@teste.com'
        self.customer_1 = Customer(name=self.customer_name_1, email=self.customer_email_1)
        self.customer_1.save()
        customer_name_2 = 'Testando'
        customer_email_2 = 'test@ando.com'
        self.customer_2 = Customer(name=customer_name_2, email=customer_email_2)
        self.customer_2.save()
        token_payload = {"id": self.customer_1.id}
        self.token = jwt.encode(token_payload, settings.JWT_SECRET, algorithm='HS256')

    def test_get_customer_list(self):
        response = self.client.get('/customers/')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(response_data))
        self.assertIn('name', response_data[0])
        self.assertIn('email', response_data[1])
        self.assertNotIn('id', response_data[0])

    def test_get_customer_list(self):
        response = self.client.get('/customers/')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(response_data))
        self.assertIn('name', response_data[0])
        self.assertIn('email', response_data[1])
        self.assertNotIn('id', response_data[0])

    def test_create_customer(self):
        request_data = {
            "name": 'created',
            "email": 'created@email.com'
        }
        response = self.client.post('/customers/', request_data, content_type="application/json")
        response_data = json.loads(response.content)

        created_customer = Customer.objects.get(name=request_data['name'])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(request_data['name'], response_data['name'])
        self.assertEqual(request_data['email'], response_data['email'])
        self.assertTrue(created_customer)

    def test_create_customer_with_existing(self):
        request_data = {
            "name": 'created',
            "email": self.customer_email_1
        }
        response = self.client.post('/customers/', request_data, content_type="application/json")
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual({'email': ['customer with this Email already exists.']}, response_data)


class CustomerDetailTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer_name = 'Teste'
        self.customer_email = 'teste@teste.com'
        self.customer = Customer(name=self.customer_name, email=self.customer_email)
        self.customer.save()
        token_payload = {"id": self.customer.id}
        self.token = jwt.encode(token_payload, settings.JWT_SECRET, algorithm='HS256')

    def test_get_customer_detail_without_headers(self):
        response = self.client.get(f'/customers/{self.customer.id}/')

        self.assertEqual(response.status_code, 400)

    def test_get_customer_detail_valid_token(self):
        response = self.client.get(f'/customers/{self.customer.id}/', HTTP_AUTHORIZATION=self.token)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.customer.name, response_data['name'])
        self.assertEqual(self.customer.email, response_data['email'])

    def test_get_customer_detail_invalid_token(self):
        invalid_token = 'ayJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.-aLaOKeSHBU2cul6JzhHn1mmXANz1QGL2KYIhOBHpQc'
        response = self.client.get(f'/customers/{self.customer.id}/', HTTP_AUTHORIZATION=invalid_token)

        self.assertEqual(response.status_code, 401)

    def test_get_customer_detail_token_from_another_user(self):
        new_customer = Customer(name='a', email='a@a.com')
        new_customer.save()
        response = self.client.get(f'/customers/{new_customer.id}/', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 401)

    def test_update_customer(self):
        data = {"name": "New test name"}
        response = self.client.put(f'/customers/{self.customer.id}/', data, content_type="application/json",
                                   HTTP_AUTHORIZATION=self.token)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response_data['email'], self.customer.email)

    def test_update_email_existing_email(self):
        new_customer = Customer(name='a', email='a@a.com')
        new_customer.save()

        data = {"email": new_customer.email}
        response = self.client.put(f'/customers/{self.customer.id}/', data, content_type="application/json",
                                   HTTP_AUTHORIZATION=self.token)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, {'email': ['customer with this Email already exists.']})

    def test_delete_customer(self):
        response = self.client.delete(f'/customers/{self.customer.id}/', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 204)

        with self.assertRaises(Customer.DoesNotExist):
            Customer.objects.get(name=self.customer_name, email=self.customer_email)