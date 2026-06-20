from rest_framework import serializers

from products.serializers import FinancialProductListSerializer
from .models import FavoriteProduct


class FavoriteProductSerializer(serializers.ModelSerializer):
    product = FinancialProductListSerializer(read_only=True)

    class Meta:
        model = FavoriteProduct
        fields = ('id', 'product', 'created_at')