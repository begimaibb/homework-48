from django.urls import path
from webapp.views import IndexView, ProductView, CreateProduct, UpdateProduct, DeleteProduct


urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('products/add/', CreateProduct.as_view(), name="create"),
    path('product/<int:pk>/', ProductView.as_view(), name="product_view"),
    path('product/<int:pk>/update', UpdateProduct.as_view(), name="update_product"),
    path('product/<int:pk>/delete', DeleteProduct.as_view(), name="delete_product"),
]