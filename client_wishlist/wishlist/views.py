from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from wishlist.models import Wishlist
from wishlist.serializers import WishlistSerializer
from wishlist.wishlist_svc import get_or_update, delete_product_from_whishlist


class WhishListDetailView(APIView):
    def get(self, request, customer_id):
        whishlist = get_object_or_404(Wishlist, customer__id=customer_id)
        serializer = WishlistSerializer(whishlist)

        return Response(serializer.data)

    def post(self, request, customer_id):
        whishlist_data = request.data
        whishlist_data["customer"] = customer_id

        serializer = WishlistSerializer(data=whishlist_data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return response

    def delete(self, request, customer_id):
        whishlist = get_object_or_404(Wishlist, customer__id=customer_id)
        whishlist.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class WhislistUpdateView(APIView):
    def post(self, request, customer_id, product_id):
        whishlist = get_or_update(customer_id, product_id)
        serializer = WishlistSerializer(whishlist)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, customer_id, product_id):
        whishlist = delete_product_from_whishlist(customer_id, product_id)
        serializer = WishlistSerializer(whishlist)

        return Response(serializer.data, status=status.HTTP_200_OK)

