from django.db import models
from django.urls import reverse

from django.core.validators import validate_comma_separated_integer_list

# Create your models here.


class Product(models.Model):
    category_choices = [('other', 'Other'), ('dairy', 'Dairy'), ('soft_drinks', 'Soft Drinks'),
                        ('groceries', 'Groceries')]
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Name")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Description")
    category = models.CharField(max_length=100, choices=category_choices, default='1')
    remainder = models.PositiveIntegerField(null=False, blank=False, verbose_name="Remainder")
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, verbose_name="Price")

    def __str__(self):
        return f'{self.name} - {self.remainder}'

    def get_absolute_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.pk})

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Cart(models.Model):
    product = models.ForeignKey("webapp.Product", on_delete=models.CASCADE, related_name="product")
    quantity = models.PositiveIntegerField(verbose_name="Quantity", default=1)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

    class Meta:
        verbose_name = "Product in cart"
        verbose_name_plural = "Products in cart"

    def get_product_total(self):
        return self.quantity * self.product.price

    @classmethod
    def get_total(cls):
        total = 0
        for cart in cls.objects.all():
            total += cart.get_product_total()
        return total


class Order(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Name")
    phone = models.CharField(max_length=100, null=False, blank=False, verbose_name="Phone")
    address = models.CharField(max_length=100, null=False, blank=False, verbose_name="Address")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    products = models.ManyToManyField('webapp.Product', related_name='orders', verbose_name='Products',
                                      through='webapp.OrderProduct', through_fields=['order', 'product'])

    def __str__(self):
        return f'{self.name} - {self.phone}'

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderProduct(models.Model):
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE,
                                verbose_name='Product', related_name='order_products')
    order = models.ForeignKey('webapp.Order', on_delete=models.CASCADE,
                              verbose_name='Order', related_name='order_products')
    quantity = models.PositiveIntegerField(verbose_name='Quantity')

    def __str__(self):
        return f'{self.product.name} - {self.order.name}'

    class Meta:
        verbose_name = 'Product in order'
        verbose_name_plural = 'Products in order'

