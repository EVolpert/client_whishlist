from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from customers.auth import authenticate
from customers.models import Customer
from customers.serializers import CustomerSerializer
from django.middleware.csrf import get_token
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


def login(request):
    email_exists = authenticate(email='teste@teste.com', name='2teste')
    email_doesnot_exist = authenticate(email='naoexisteemail@a.com')

    return HttpResponse(f'{email_exists}\n{email_doesnot_exist}')


def csrf(request):
    return HttpResponse(get_token(request))


class CustomertList(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return response


class CustomerDetail(APIView):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        serializer = CustomerSerializer(customer)

        return Response(serializer.data)

    def put(self, request, customer_id):
        customer = Customer.objects.get(id=customer_id)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return response

    def delete(self, request, customer_id):
        customer = Customer.objects.get(id=customer_id)
        customer.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)