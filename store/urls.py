from django.urls import path, include
# from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('charts', views.CartViewSet)

product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')

product_router.register('reviews', views.ReviewViewSet,
                        basename='product-review')

urlpatterns = router.urls + product_router.urls
