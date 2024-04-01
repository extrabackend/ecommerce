from rest_framework import status, permissions as drf_permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models, serializers, permissions


class OrderViewSet(ModelViewSet):
    queryset = models.Order.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return (permissions.HasPermission('orders.add_order'),)

        return (drf_permissions.IsAuthenticated(),)

    def get_queryset(self):
        return models.Order.objects.prefetch_related(
            'user',
        ).filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.OrderRetrieveSerializer

        return serializers.OrderSerializer


class OrderItemViewSet(ModelViewSet):
    queryset = models.OrderItem.objects.order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.OrderItemRetrieveSerializer

        if self.action == 'create':
            return serializers.OrderItemCreateSerializer

        return serializers.OrderItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_item = models.OrderItem.objects.create(
            order=serializer.validated_data['order'],
            product=serializer.validated_data['product'],
            price=serializer.validated_data['product'].price,
        )
        serializer = serializers.OrderItemSerializer(order_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 1. Handlers -> user input, validation, response
# 2. Services -> business logic
# 3. Repositories -> db, cache, api
# 4. Domains -> users, orders, order items ...
