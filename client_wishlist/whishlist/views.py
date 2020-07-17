from whishlist.models import Whishlist
from whishlist.serializers import WhishlistSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class WhishListDetailView(APIView):
    def get(self, request, customer_id):
        whishlist = get_object_or_404(Whishlist, customer__id=customer_id)
        serializer = WhishlistSerializer(whishlist)

        return Response(serializer.data)

    def post(self, request, customer_id):
        whishlist_data = request.data
        whishlist_data["customer"] = customer_id

        serializer = WhishlistSerializer(data=whishlist_data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return response

    def delete(self, request, customer_id):
        whishlist = get_object_or_404(Whishlist, customer__id=customer_id)
        whishlist.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)