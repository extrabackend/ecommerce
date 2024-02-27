from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('orders', views.OrderViewSet)
router.register('order-items', views.OrderItemViewSet)

urlpatterns = router.urls
