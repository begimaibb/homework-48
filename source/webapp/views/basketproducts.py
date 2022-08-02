from webapp.models import BasketProduct, Product


class BasketAdd:

    def __init__(self):
        Product.remainder = self.product.remainder

    @staticmethod
    def add_to_basket(product):
        basket = 0
        if product.remainder == 0:
            return
        if BasketProduct.objects.filter(product=product).exists():
            basket + 1
        if