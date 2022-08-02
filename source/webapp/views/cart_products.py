from django.shortcuts import redirect

from webapp.models import Product, CartProduct
from django.views.generic import ListView, DetailView


class CartProductView(ListView):
    template_name = "products/cart_product_view.html"
    model = CartProduct

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_products = CartProduct.objects.all()
        total_sum = 0
        for cart_product in cart_products:
            total_sum += cart_product.quantity * cart_product.product.price
            cart_product.sum = cart_product.quantity * cart_product.product.price
        context['total_sum'] = total_sum
        context["cart_products"] = cart_products
        return context


class CreateCartProduct(DetailView):
    modem = Product

    def get_queryset(self):
        return Product.objects.all()

    def get(self, request, *args, **kwargs):
        product = self.get_object()

        if product.remainder == 0:
            return

        product.remainder -= 1
        product.save()

        cart_product = CartProduct.objects.filter(product=product)
        if cart_product:
            cart_product.quantity += 1
            cart_product.save()
        else:
            CartProduct.objects.create(product=product, quantity=1)
        return redirect("index")


class DeleteCartProduct(DetailView):
    model = CartProduct

    def get_queryset(self):
        return CartProduct.objects.all()

    def get(self, request, *args, **kwargs):
        cart_product = self.get_object()
        cart_product.delete()
        return redirect("index")