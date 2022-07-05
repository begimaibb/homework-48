from django.urls import path
from webapp.views import index_view, create_product, product_view, update_product, delete_product


urlpatterns = [
    path('', index_view, name="index"),
    path('products/add/', create_product, name="create"),
    path('product/<int:pk>/', product_view, name="product_view"),
    path('product/<int:pk>/update', update_product, name="update_product"),
    path('product/<int:pk>/delete', delete_product, name="delete_product"),
]