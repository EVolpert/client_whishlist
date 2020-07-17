from rest_framework import serializers
from whishlist.models import Whishlist


class WhishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Whishlist
        fields = '__all__'