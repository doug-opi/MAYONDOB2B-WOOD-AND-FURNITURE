from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Stock
from .forms import ProductForm, StockForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages



# -------------------- Product Views --------------------

class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"


class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("product_list")
    success_message = "Product was created successfully!"


class ProductUpdateView(SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("product_list")
    success_message = "Product was updated successfully!"


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("product_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Product was deleted successfully.")
        return super().delete(request, *args, **kwargs)


# -------------------- Stock Views --------------------

class StockListView(ListView):
    model = Stock
    template_name = "stock_list.html"
    context_object_name = "stocks"


class StockCreateView(SuccessMessageMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = "stock_form.html"
    success_url = reverse_lazy("stock_list")
    success_message = "Stock was Added successfully!"


class StockUpdateView(SuccessMessageMixin, UpdateView):
    model = Stock
    form_class = StockForm
    template_name = "stock_form.html"
    success_url = reverse_lazy("stock_list")
    success_message = "Stock was updated successfully!"


class StockDeleteView(DeleteView):
    model = Stock
    template_name = "stock_confirm_delete.html"
    success_url = reverse_lazy("stock_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Stock was deleted successfully.")
        return super().delete(request, *args, **kwargs)
    
