from django.urls import path
from . import views


urlpatterns = [
    path("products/", views.ProductList.as_view(), name=""),
    path("products/<int:pk>/", views.ProductDetails.as_view(), name=""),
    path("collections/", views.CollectionList.as_view(), name=""),
    path("collections/<int:pk>/", views.CollectionDetail.as_view(), name=""),
]
