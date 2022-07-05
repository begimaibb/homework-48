from django import forms
from django.forms import widgets


class ProductForm(forms.Form):
    category_choices = [('other', 'Other'), ('dairy', 'Dairy'), ('soft_drinks', 'Soft Drinks'),
                        ('groceries', 'Groceries')]
    name = forms.CharField(max_length=100, required=True, label='Name')
    description = forms.CharField(max_length=2000, required=False, label='Description',
                                  widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
    category = forms.CharField(label='Category', widget=forms.Select(choices=category_choices))
    remainder = forms.IntegerField(min_value=0, required=True, label='Remainder')
    price = forms.DecimalField(required=True, label='Price')