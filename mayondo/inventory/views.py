from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Stock
from .forms import ProductForm, StockForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.decorators.http import require_POST



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
    



from django.db.models import Sum, F, ExpressionWrapper, DecimalField, OuterRef, Subquery

class StockLevelReportView(ListView):
    model = Product
    template_name = 'stock_level_report.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        # Create a subquery for each product’s aggregated stock quantity and selling price
        stock_subquery = Stock.objects.filter(product=OuterRef('pk'))

        queryset = Product.objects.annotate(
            quantity=Subquery(
                stock_subquery.annotate(qty=Sum('quantity')).values('qty')[:1]
            ),
            # Alias 'unit_price' to Stock.selling_price using Sum()
            unit_price=Subquery(
                stock_subquery.annotate(price=Sum('selling_price')).values('price')[:1]
            ),
        ).annotate(
            # Compute total stock value (quantity * unit_price)
            stock_value=ExpressionWrapper(
                F('quantity') * F('unit_price'),
                output_field=DecimalField()
            )
        ).order_by('name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']

        # Aggregate summary statistics
        context['total_stock_value'] = sum((p.stock_value or 0) for p in products)
        context['low_stock_count'] = sum(1 for p in products if p.quantity and 1 <= p.quantity <= 5)
        context['out_of_stock_count'] = sum(1 for p in products if (p.quantity or 0) == 0)
        context['available_count'] = sum(1 for p in products if (p.quantity or 0) > 5)
        return context
#class StockLevelReportView(ListView):
#    model = Product
#    template_name = 'stock_level_report.html'
#    context_object_name = 'products'
#    paginate_by = 20  # Optional

#    def get_queryset(self):
#        queryset = Product.objects.all().annotate(
#            stock_value=ExpressionWrapper(
#                F('quantity') * F('unit_price'),
#                output_field=DecimalField()
#            )
#        ).order_by('name')
#        return queryset#

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        products = context['products']

#        context['total_stock_value'] = sum([p.stock_value for p in products])
#        context['low_stock_count'] = sum(1 for p in products if 1 <= p.quantity <= 5)
#        context['out_of_stock_count'] = sum(1 for p in products if p.quantity == 0)
#        context['available_count'] = sum(1 for p in products if p.quantity > 5)
#        return context


