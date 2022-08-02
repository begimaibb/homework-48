from django.db import models

from django.core.validators import validate_comma_separated_integer_list

# Create your models here.


class Product(models.Model):
    category_choices = [('other', 'Other'), ('dairy', 'Dairy'), ('soft_drinks', 'Soft Drinks'),
                        ('groceries', 'Groceries')]
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Name")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Description")
    category = models.CharField(max_length=100, choices=category_choices, default='1')
    remainder = models.IntegerField(null=False, blank=False, verbose_name="Remainder")
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, verbose_name="Price")

    def __str__(self):
        return f"{self.id}. {self.name}, {self.description} {self.category} {self.remainder} {self.price}"

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class CartProduct(models.Model):
    product = models.ForeignKey("webapp.Product", on_delete=models.CASCADE, related_name="product")
    quantity = models.IntegerField(null=False, blank=False, verbose_name="Quantity")

    def __str__(self):
        return f"{self.id}. {self.product} {self.quantity}"

    class Meta:
        db_table = "cartproduct"
        verbose_name = "CartProduct"
        verbose_name_plural = "CartProducts"


class Order(models.Model):
    products = models.ManyToManyField('webapp.Product', related_name='products')
    quantities = models.CharField(validators=[validate_comma_separated_integer_list],max_length=200, blank=True, null=True, default='')
    username = models.CharField(max_length=100, null=False, blank=False, verbose_name="Username")
    phone = models.CharField(max_length=100, null=False, blank=False, verbose_name="Phone")
    address = models.CharField(max_length=100, null=False, blank=False, verbose_name="Address")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")


    def __str__(self):
        return f"{self.id}. {self.username} {self.phone} {self.address} {self.created_at} {self.products} " \
               f"{self.quantities}"

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

