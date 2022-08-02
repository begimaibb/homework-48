from django.urls import path
from webapp.views import IndexView, ProductView, CreateProduct, UpdateProduct, DeleteProduct
from webapp.views import CartProductView, CreateCartProduct, DeleteCartProduct


urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('products/cart', CartProductView.as_view(), name="cart_product_view"),
    path('products/cart/add/<int:pk>', CreateCartProduct.as_view(), name="create_cart_product"),
    path('products/<int:pk>/delete', DeleteCartProduct.as_view(), name="delete_cart_product"),
    path('products/add/', CreateProduct.as_view(), name="create"),
    path('product/<int:pk>/', ProductView.as_view(), name="product_view"),
    path('product/<int:pk>/update', UpdateProduct.as_view(), name="update_product"),
    path('product/<int:pk>/delete', DeleteProduct.as_view(), name="delete_product"),
]