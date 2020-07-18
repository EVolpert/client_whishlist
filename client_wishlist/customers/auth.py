from django.conf import settings
from django.shortcuts import get_object_or_404

import jwt


from customers.models import Customer


def generate_token(email=None, name=None):
    try:
        customer = Customer.objects.get(email=email, name=name)
    except Customer.DoesNotExist:
        response = None
    else:
        payload = {"id": customer.id}
        response = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')

    return response


def authenticate(customer_id=None, token=None):
    authenticated = False

    try:
        token_payload = jwt.decode(token, settings.JWT_SECRET, algorithm='HS256')
    except jwt.exceptions.DecodeError:
        pass
    else:
        if token_payload['id'] == customer_id:
            authenticated = True

    return authenticated
