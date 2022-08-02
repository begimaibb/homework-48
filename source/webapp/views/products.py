from django.db.models import Q
from django.shortcuts import  redirect, get_object_or_404
from django.urls import reverse_lazy

# Create your views here.
from django.utils.http import urlencode

from webapp.forms import ProductForm, SearchForm, UserProductForm, ProductDeleteForm
from webapp.models import Product
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView


class IndexView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    ordering = 'category', 'name'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Product.objects.filter(Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Product.objects.all()

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
    template_name = "products/product_view.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # id = self.object.id
        # print(id)
        # context['tasks'] = Task.objects.filter(product_id=id)
        return context


class CreateProduct(CreateView):
    form_class = ProductForm
    template_name = "products/create.html"

    def form_valid(self, form):
        product = form.save(commit=False)
        product.save()
        form.save_m2m()
        return redirect("product_view", pk=product.pk)


class UpdateProduct(UpdateView):
    form_class = ProductForm
    template_name = "products/update.html"
    model = Product

    def get_form_class(self):
        if self.request.GET.get("is_admin"):
            return ProductForm
        return UserProductForm


class DeleteProduct(DeleteView):
    model = Product
    template_name = "products/delete.html"
    success_url = reverse_lazy('index')
    form_class = ProductDeleteForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.get_object())
        if form.is_valid():
            return self.delete(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)

