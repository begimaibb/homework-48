from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, F


class Product(models.Model):
    category_choices = [('other', 'Other'), ('dairy', 'Dairy'), ('soft_drinks', 'Soft Drinks'),
                        ('groceries', 'Groceries')]
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Name")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Description")
    category = models.CharField(max_length=100, choices=category_choices, default='1')
    remainder = models.PositiveIntegerField(verbose_name="Remainder")
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, verbose_name="Price")

    def __str__(self):
        return f'{self.name} - {self.remainder}'

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Order(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Name")
    phone = models.CharField(max_length=100, null=False, blank=False, verbose_name="Phone")
    address = models.CharField(max_length=100, null=False, blank=False, verbose_name="Address")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    products = models.ManyToManyField('webapp.Product', related_name='orders', verbose_name='Products',
                                      through='webapp.OrderProduct', through_fields=['order', 'product'])
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="orders",
                             verbose_name='User', null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.phone}'

    def get_total(self):
        total = self.order_products.aggregate(total=Sum(F("qty") * F("product__price")))
        print(total)
        return total["total"]

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderProduct(models.Model):
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE,
                                verbose_name='Product', related_name='order_products')
    order = models.ForeignKey('webapp.Order', on_delete=models.CASCADE,
                              verbose_name='Order', related_name='order_products')
    qty = models.PositiveIntegerField(verbose_name='Qty')

    def __str__(self):
        return f'{self.product.name} - {self.order.name}'

    def get_sum(self):
        return self.qty * self.product.price

    class Meta:
        verbose_name = 'Product in order'
        verbose_name_plural = 'Products in order'

