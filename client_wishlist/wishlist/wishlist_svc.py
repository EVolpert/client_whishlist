from django.http import Http404
from django.shortcuts import get_object_or_404

import requests

from customers.models import Customer
from wishlist.models import Wishlist


def get_product(product_id=None):
    product_data = requests.get(f'http://challenge-api.luizalabs.com/api/product/{product_id}/')

    if product_data.status_code == 404:
        raise Http404("Product does not exist")
    else:
        product = product_data.json()

    return product


def get_or_update(customer_id=None, product_id=None):
    customer = get_object_or_404(Customer, id=customer_id)
    product = get_product(product_id)
    wishlist_template = {'count': 1, 'products': [product]}
    wishlist, created = Wishlist.objects.get_or_create(customer=customer, defaults={"wishlist": wishlist_template})

    if created:
        pass
    else:
        product_exist = list(filter(lambda product_wish: product_wish['id'] == product_id, wishlist.wishlist['products']))

        if product_exist:
            pass
        else:
            wishlist.whishlist['products'].append(product)
            wishlist.whishlist['count'] = len(wishlist.whishlist['products'])
            wishlist.save()

    return wishlist

def delete_product_from_whishlist(customer_id, product_id):
    customer = get_object_or_404(Customer, id=customer_id)
    wishlist = get_object_or_404(Wishlist, customer=customer)
    wishlist_products = wishlist.wishlist['products']

    product_exist = list(filter(lambda product_wish: product_wish['id'] == product_id, wishlist_products))

    if product_exist:
        index = wishlist_products.index(product_exist[0])
        del wishlist_products[index]
    else:
        raise Http404('Product does not exist in wishlist')
    return wishlist
