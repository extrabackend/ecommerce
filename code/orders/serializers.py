from rest_framework import serializers

from products.serializers import ProductModelSerializer

from . import models


class OrderItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = ('order', 'product')


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = '__all__'


class OrderItemRetrieveSerializer(serializers.ModelSerializer):
    product = ProductModelSerializer()

    class Meta:
        model = models.OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = '__all__'


class OrderRetrieveSerializer(serializers.ModelSerializer):
    order_items = OrderItemRetrieveSerializer(many=True)

    class Meta:
        model = models.Order
        fields = '__all__'
