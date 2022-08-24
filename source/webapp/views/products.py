from django.db.models import Q
from django.shortcuts import  redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

# Create your views here.
from django.utils.http import urlencode

from webapp.forms import ProductForm, SearchForm
from webapp.models import Product
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from webapp.views.base_view import SearchView


class IndexView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    ordering = 'category', 'name'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(remainder__gt=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class ProductView(DetailView):
    model = Product
    template_name = 'products/product_view.html'
    queryset = Product.objects.filter(remainder__gt=0)


class CreateProduct(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})


class UpdateProduct(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/update.html'

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})


class DeleteProduct(DeleteView):
    model = Product
    template_name = 'products/delete.html'
    success_url = reverse_lazy('webapp:index')

