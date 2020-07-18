from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from customers.auth import generate_token, authenticate
from customers.models import Customer
from customers.serializers import CustomerSerializer


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        name = data.get('name')
        token = generate_token(email=email, name=name)

        if token:
            response = Response(token, status=status.HTTP_200_OK)
        else:
            response = Response(status=status.HTTP_401_UNAUTHORIZED)

        return response


class CustomerList(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

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
        try:
            token = request.META['HTTP_AUTHORIZATION']
            authenticated = authenticate(customer_id=customer_id, token=token)
        except KeyError:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if authenticated:
                customer = get_object_or_404(Customer, id=customer_id)
                serializer = CustomerSerializer(customer)
                response = Response(serializer.data, status=status.HTTP_200_OK)
            else:
                response = Response(status=status.HTTP_401_UNAUTHORIZED)
        return response

    def put(self, request, customer_id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            authenticated = authenticate(customer_id=customer_id, token=token)
        except KeyError:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if authenticated:
                customer = get_object_or_404(Customer, id=customer_id)
                serializer = CustomerSerializer(customer, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    response = Response(serializer.data)
                else:
                    response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = Response(status=status.HTTP_401_UNAUTHORIZED)

        return response

    def delete(self, request, customer_id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            authenticated = authenticate(customer_id=customer_id, token=token)
        except KeyError:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if authenticated:
                customer = get_object_or_404(Customer, id=customer_id)
                customer.delete()
                response = Response(status=status.HTTP_204_NO_CONTENT)
            else:
                response = Response(status=status.HTTP_401_UNAUTHORIZED)
            
        return response
