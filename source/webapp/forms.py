import re
from django import forms
from webapp.models import Product, CartProduct, Order
from django.core.exceptions import ValidationError
from django.forms import widgets


class UserProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "remainder", "price"]


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ["name", "description", "category", "remainder", "price"]
        widgets = {
            "category": widgets.RadioSelect
        }

    def clean(self):
        name = self.cleaned_data.get("name")
        description = self.cleaned_data.get("description")
        if not re.match("^[a-zA-Zа-яА-Я\s]+$", name):
            self.add_error("name", ValidationError("The name should include only letters"))
        if not re.match("^[a-zA-Zа-яА-Я\s]+$", description):
            self.add_error("description", ValidationError("The description should include only letters"))
        return super().clean()


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Find')


class ProductDeleteForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name"]

    def clean_title(sellf):
        name = self.cleaned_data.get("name")
        if self.instance.name != name:
            raise ValidationError("Names do not match")
        return name


class CartProduct(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = ["product", "quantity"]


class Order(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["products", "quantities", "username", "phone", "address"]

