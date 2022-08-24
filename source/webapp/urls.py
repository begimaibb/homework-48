from django.urls import path
from webapp.views import IndexView, ProductView, CreateProduct, UpdateProduct, DeleteProduct, \
    CartView, CartAddView, CartDeleteOneView, CartDeleteView, OrderCreate

app_name = "webapp"

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('cart/', CartView.as_view(), name="cart_view"),
    path('products/<int:pk>/add-to-cart/', CartAddView.as_view(), name='add_to_cart'),
    path('products/cart/add/<int:pk>', CartAddView.as_view(), name="create_cart_product"),
    path('products/<int:pk>/delete', CartDeleteView.as_view(), name="delete_cart_product"),
    path('products/<int:pk>/one-delete/', CartDeleteOneView.as_view(), name='remove_one_from_cart'),
    path('products/add/', CreateProduct.as_view(), name="create"),
    path('product/<int:pk>/', ProductView.as_view(), name="product_view"),
    path('product/<int:pk>/update', UpdateProduct.as_view(), name="update_product"),
    path('product/<int:pk>/delete', DeleteProduct.as_view(), name="delete_product"),
    path('order/create/', OrderCreate.as_view(), name='order_create'),
]