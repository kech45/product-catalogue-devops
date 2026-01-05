from django.urls import path
from .views import product_list_create, product_detail, product_page, delete_product

urlpatterns = [
    path("", product_page, name="product-page"),
    path("delete/<int:pk>/", delete_product, name="delete-product"),
    path('products/', product_list_create),
    path('products/<int:pk>/', product_detail),
]
