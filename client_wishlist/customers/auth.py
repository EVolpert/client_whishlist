from customers.models import Customer


def authenticate(email=None, name=None):
    try:
        customer = Customer.objects.get(email=email, name=name)
    except Customer.DoesNotExist:
        customer = None

    return customer
