from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('products', views.ProductView, basename='products')
router.register('categories', views.CategoryViewSet, basename='categories')


urlpatterns = router.urls
