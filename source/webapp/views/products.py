from django.urls import reverse_lazy, reverse
from webapp.forms import ProductForm, SearchForm
from webapp.models import Product
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from webapp.views.base_view import SearchView


class IndexView(SearchView):
    model = Product
    template_name = 'products/index.html'
    ordering = ['category', 'name']
    search_fields = ['name__icontains']
    paginate_by = 6
    context_object_name = 'products'

    def get_queryset(self):
        return super().get_queryset().filter(remainder__gt=0)


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

    def has_permission(self):
        return self.request.user.has_perm("webapp.add_product")


class UpdateProduct(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/update.html'

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return self.request.user.has_perm("webapp.change_product")


class DeleteProduct(DeleteView):
    model = Product
    template_name = 'products/delete.html'
    success_url = reverse_lazy('webapp:index')

    def has_permission(self):
        return self.request.user.has_perm("webapp.delete_product")

