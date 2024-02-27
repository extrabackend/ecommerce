from rest_framework import serializers

from . import models


class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    price = serializers.IntegerField()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = '__all__'


class RetrieveCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'created_at', 'updated_at')


class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = '__all__'
