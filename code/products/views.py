import logging
import uuid

from django.conf import settings
from django.db.models import F
from rest_framework.viewsets import ModelViewSet

from products import models, serializers

logger = logging.getLogger(__name__)


class CategoryViewSet(ModelViewSet):

    def get_serializer_class(self):
        if settings.DEBUG:
            print('request action:', self.action)

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

# 1. Caching +
# 2. Session and Cookies (Middleware) +
# 3. Localization +
# 4. Testing +
# 5. Logging +
# 6. Timezone +
# 7. Normalization and Denormalization +
# 8. Async / WS
# 9. Multiple Databases +
# 11. Container and Docker +
# 12. Microservices
