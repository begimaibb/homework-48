from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from django.shortcuts import redirect

from webapp.models import Product, Cart, Order, OrderProduct
from django.views.generic import ListView, DetailView

from webapp.forms import CartForm, OrderForm


class CartAddView(CreateView):
    model = Cart
    form_class = CartForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        quantity = form.cleaned_data.get("quantity")
        if quantity > product.remainder:
            return HttpResponseBadRequest(
                f"Product quantity {product.name} is {product.remainder}. Adding {quantity} is not possible")
        else:
            # try:
            #     cart_product = Cart.objects.get(product=product)
            #     cart_product.qty += qty
            #     cart_product.save()
            # except Cart.DoesNotExist:
            #     Cart.objects.create(product=product, qty=qty)
            cart_product, is_created = Cart.objects.get_or_create(product=product)
            if is_created:
                cart_product.quantity = quantity
            else:
                cart_product.quantity += quantity
            cart_product.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next = self.request.GET.get("next")
        if next:
            return next
        return reverse("webapp:index")


class CartView(ListView):
    model = Cart
    template_name = "cart/cart_view.html"
    context_object_name = "cart"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['total'] = Cart.get_total()
        context['form'] = OrderForm()
        return context


class CartDeleteView(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart_view')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CartDeleteOneView(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart_view')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        cart = self.object
        cart.quantity -= 1
        if cart.quantity < 1:
            cart.delete()
        else:
            cart.save()
        return HttpResponseRedirect(success_url)


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('webapp:index')

    # def form_valid(self, form):
    #     order = form.save()
    #     for item in Cart.objects.all():
    #         OrderProduct.objects.create(product=item.product, qty=item.qty, order=order)
    #         item.product.amount -= item.qty
    #         item.product.save()
    #         item.delete()
    #
    #     return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        order = form.save()

        products = []
        order_products = []

        for item in Cart.objects.all():
            order_products.append(OrderProduct(product=item.product, quantity=item.quantity, order=order))
            item.product.remainder -= item.quantity
            products.append(item.product)

        OrderProduct.objects.bulk_create(order_products)
        Product.objects.bulk_update(products, ("remainder",))
        Cart.objects.all().delete()
        return HttpResponseRedirect(self.success_url)