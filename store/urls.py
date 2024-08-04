from django.urls import path
from . import views


urlpatterns = [
    path("products/", views.product_list, name=""),
    path("products/<int:id>", views.product_detail, name=""),
    path("collections/", views.collection_list, name=""),
    path("collections/<int:id>", views.collection_detail, name=""),
]
