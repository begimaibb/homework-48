from django.db import models


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


class BasketProduct(models.Model):
    product = models.ForeignKey("webapp.Product", on_delete=models.CASCADE, related_name="product")
    quantity = models.IntegerField(null=False, blank=False, verbose_name="Quantity")

    def __str__(self):
        return f"{self.id}. {self.product} {self.quantity}"

    class Meta:
        db_table = "basketproducts"
        verbose_name = "BasketProduct"
        verbose_name_plural = "BasketProducts"
