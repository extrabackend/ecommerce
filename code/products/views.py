import time

from django.db.models import Count, F
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from products import models, serializers


class CategoryViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.RetrieveCategorySerializer

        return serializers.CategorySerializer

    def get_queryset(self):
        locale = self.request.META.get('HTTP_ACCEPT_LANGUAGE')
        return models.Category.objects.annotate(name=F(f'name_{locale}')).defer(
            'name_kk', 'name_ru', 'name_en',
        )


class ProductView(ModelViewSet):

    def get_serializer_class(self):
        return serializers.ProductModelSerializer

    def get_queryset(self):
        return models.Product.objects.select_related(
            'subcategory',
            'subcategory__category'
        )

    @action(detail=False, url_path='analytics')
    def analytics(self, request, *args, **kwargs):
        start = time.monotonic()
        #...
        qs = models.Product.objects.annotate(
            count_order_items=Count(
                'order_items__id'
            )
        )
        #...
        end = time.monotonic()
        print(end - start)
        return qs

# 1. Caching +
# 2. Session and Cookies (Middleware) +
# 3. Localization +
# 4. Testing
# 5. Logging
# 6. Async (WS and FastAPI)
# 7. Container and Docker
# 8. Multiple Databases, Normalization and Denormalization
# 9. Microservices
