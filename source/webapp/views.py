from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse

# Create your views here.
from webapp.forms import ProductForm
from webapp.models import Product
# from webapp.validate import task_validate


def index_view(request):
    products = Product.objects.order_by("category", "name")
    context = {"products": products}
    return render(request, "index.html", context)


def product_view(request, **kwargs):
    pk = kwargs.get("pk")
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_view.html", {"product": product})


def create_product(request):
    if request.method == "GET":
        form = ProductForm()
        return render(request, "create.html", {"form": form})
    else:
        form = ProductForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            category = form.cleaned_data.get("category")
            remainder = form.cleaned_data.get("remainder")
            price = form.cleaned_data.get("price")
            new_product = Product.objects.create(name=name, description=description, category=category,
                                                 remainder=remainder, price=price)
            return redirect("index")
        return render(request, "create.html", {"form": form})


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "GET":
        form = ProductForm(initial={
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "remainder": product.remainder,
            "price": product.price
        })
        return render(request, "update.html", {"form": form})
    else:
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data.get("name")
            product.description = form.cleaned_data.get("description")
            product.category = form.cleaned_data.get("category")
            product.remainder = form.cleaned_data.get("remainder")
            product.price = form.cleaned_data.get("price")
            product.save()
            return redirect("product_view", pk=product.pk)
        return render(request, "update.html", {"form": form})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "GET":
        pass
    #     return render(request, "delete.html", {"product": product})
    else:
        product.delete()
        return redirect("index")

