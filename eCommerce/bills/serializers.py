from rest_framework import serializers
from .models import Product, Order, OrderDetail


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    order_id = OrderSerializer()
    product_id = ProductSerializer()
    
    
    class Meta:
        model = OrderDetail
        ## exclude = ('id', )
        fields = "__all__"

