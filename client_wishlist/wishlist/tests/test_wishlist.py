import json

from django.conf import settings
from django.test import TestCase, Client
import jwt

from customers.models import Customer
from wishlist.wishlist_svc import get_or_update


class WishlistDetailTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer_name = 'Teste'
        self.customer_email = 'teste@teste.com'
        self.customer = Customer(name=self.customer_name, email=self.customer_email)
        self.customer.save()
        token_payload = {"id": self.customer.id}
        self.token = jwt.encode(token_payload, settings.JWT_SECRET, algorithm='HS256')
        self.product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'

    def test_get_inexisting_wishlist(self):
        response = self.client.get(f'/customers/{self.customer.id}/wishlist/')

        self.assertEqual(response.status_code, 404)

    def test_get_a_wishlist(self):
        wishlist = get_or_update(customer_id=self.customer.id, product_id=self.product_id)

        response = self.client.get(f'/customers/{self.customer.id}/wishlist',
                                   HTTP_AUTHORIZATION=self.token)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['customer'], self.customer.id)
        self.assertEqual(response_data['wishlist']['count'], wishlist.wishlist['count'])
        self.assertEqual(response_data['wishlist']['products'][0]['id'], self.product_id)

    def test_delete_a_wishlist(self):
        get_or_update(customer_id=self.customer.id, product_id=self.product_id)

        response = self.client.delete(f'/customers/{self.customer.id}/wishlist',
                                      HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 204)


class WishlistUpdateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer_name = 'Teste'
        self.customer_email = 'teste@teste.com'
        self.customer = Customer(name=self.customer_name, email=self.customer_email)
        self.customer.save()
        token_payload = {"id": self.customer.id}
        self.token = jwt.encode(token_payload, settings.JWT_SECRET, algorithm='HS256')
        self.product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'

    def test_create_a_wishlist(self):
        response = self.client.post(f'/customers/{self.customer.id}/wishlist/{self.product_id}',
                                    HTTP_AUTHORIZATION=self.token)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['customer'], self.customer.id)
        self.assertEqual(response_data['wishlist']['count'], 1)
        self.assertEqual(response_data['wishlist']['products'][0]['id'], self.product_id)

    def test_update_a_wishlist(self):
        get_or_update(customer_id=self.customer.id, product_id=self.product_id)
        new_product = '958ec015-cfcf-258d-c6df-1721de0ab6ea'

        response = self.client.post(f'/customers/{self.customer.id}/wishlist/{new_product}',
                                    HTTP_AUTHORIZATION=self.token)
        response_data = json.loads(response.content)

        product_on_list = list(filter(lambda product_wish: product_wish['id'] == new_product,
                                      response_data['wishlist']['products']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['customer'], self.customer.id)
        self.assertEqual(response_data['wishlist']['count'], 2)
        self.assertTrue(product_on_list)

    def test_update_a_wishlist_invalid_product(self):
        get_or_update(customer_id=self.customer.id, product_id=self.product_id)
        new_product = '958ec015-cfcf-258d-c6df-1721de0ab6e'

        response = self.client.post(f'/customers/{self.customer.id}/wishlist/{new_product}',
                                    HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 404)

    def test_remove_a_product_from_wishlist(self):
        get_or_update(customer_id=self.customer.id, product_id=self.product_id)

        response = self.client.delete(f'/customers/{self.customer.id}/wishlist/{self.product_id}',
                                      HTTP_AUTHORIZATION=self.token)

        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['customer'], self.customer.id)
        self.assertEqual(response_data['wishlist']['count'], 0)

    def test_remove_an_invalid_product_from_wishlist(self):
        get_or_update(customer_id=self.customer.id, product_id=self.product_id)

        response = self.client.delete(f'/customers/{self.customer.id}/wishlist/a1',
                                      HTTP_AUTHORIZATION=self.token)

        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)