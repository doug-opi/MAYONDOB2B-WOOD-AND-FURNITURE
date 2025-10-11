from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Stock
from .forms import ProductForm, StockForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_manager()

class AttendantRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_attendant()

class ManagerOrAttendantRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated and
            (user.is_manager() or user.is_attendant())
        )




# -------------------- Product Views --------------------

class ProductListView(ManagerRequiredMixin, ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"


class ProductCreateView(ManagerRequiredMixin,SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("product_list")
    success_message = "Product was created successfully!"


class ProductUpdateView(ManagerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("product_list")
    success_message = "Product was updated successfully!"


class ProductDeleteView(ManagerRequiredMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("product_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Product was deleted successfully.")
        return super().delete(request, *args, **kwargs)


# -------------------- Stock Views --------------------

class StockListView(ManagerOrAttendantRequiredMixin,ListView):
    model = Stock
    template_name = "stock_list.html"
    context_object_name = "stocks"


class StockCreateView(ManagerRequiredMixin, SuccessMessageMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = "stock_form.html"
    success_url = reverse_lazy("stock_list")
    success_message = "Stock was Added successfully!"


class StockUpdateView(ManagerRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Stock
    form_class = StockForm
    template_name = "stock_form.html"
    success_url = reverse_lazy("stock_list")
    success_message = "Stock was updated successfully!"


class StockDeleteView(ManagerRequiredMixin, DeleteView):
    model = Stock
    template_name = "stock_confirm_delete.html"
    success_url = reverse_lazy("stock_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Stock was deleted successfully.")
        return super().delete(request, *args, **kwargs)
    



from django.db.models import Sum, F, ExpressionWrapper, DecimalField, OuterRef, Subquery

class StockLevelReportView(ManagerRequiredMixin, ListView):
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

from django.http import HttpResponse
from django.views import View
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from django.db.models import Sum, F, DecimalField, ExpressionWrapper, OuterRef, Subquery
from .models import Product, Stock


class StockReportPDFView(ManagerRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        # === Create HTTP response ===
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="stock_report.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        # === Title and header ===
        p.setFont("Helvetica-Bold", 16)
        p.drawString(180, height - 50, "MAYONDO WOOD & FURNITURE LTD")
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 80, "Stock Level Report")
        p.drawString(50, height - 100, "Generated Report of Current Stock Levels")

        # === Fetch data ===
        stock_subquery = Stock.objects.filter(product=OuterRef("pk")).values("product")
        products = Product.objects.annotate(
            total_quantity=Subquery(
                stock_subquery.annotate(qty=Sum("quantity")).values("qty")[:1]
            ),
            unit_price=Subquery(
                stock_subquery.annotate(price=Sum("selling_price")).values("price")[:1]
            ),
        ).annotate(
            stock_value=ExpressionWrapper(
                F("total_quantity") * F("unit_price"),
                output_field=DecimalField()
            )
        ).order_by("name")

        # === Table header ===
        y = height - 140
        p.setFont("Helvetica-Bold", 11)
        p.drawString(50, y, "Product")
        p.drawString(250, y, "Quantity")
        p.drawString(350, y, "Unit Price (UGX)")
        p.drawString(480, y, "Stock Value (UGX)")

        y -= 20
        p.line(50, y, 550, y)
        y -= 15

        # === Table content ===
        p.setFont("Helvetica", 10)
        total_value = 0

        for product in products:
            if y < 80:  # start new page
                p.showPage()
                y = height - 80
                p.setFont("Helvetica-Bold", 11)
                p.drawString(50, y, "Product")
                p.drawString(250, y, "Quantity")
                p.drawString(350, y, "Unit Price (UGX)")
                p.drawString(480, y, "Stock Value (UGX)")
                y -= 20
                p.line(50, y, 550, y)
                y -= 15
                p.setFont("Helvetica", 10)

            quantity = product.total_quantity or 0
            price = product.unit_price or 0
            stock_value = (quantity * price)
            total_value += stock_value

            p.drawString(50, y, product.name[:25])
            p.drawString(260, y, str(quantity))
            p.drawRightString(420, y, f"{price:,.0f}")
            p.drawRightString(550, y, f"{stock_value:,.0f}")
            y -= 18

        # === Footer summary ===
        y -= 15
        p.line(50, y, 550, y)
        p.setFont("Helvetica-Bold", 11)
        y -= 20
        p.drawString(400, y, "Total Stock Value:")
        p.drawRightString(550, y, f"{total_value:,.0f} UGX")

        # === Footer note ===
        y -= 40
        p.setFont("Helvetica-Oblique", 9)
        p.drawString(50, y, "Note: Goods once sold are not returnable.")
        p.drawString(50, y - 15, "For inquiries or complaints, contact us at +256 700 000000 or info@mwf.com")

        # === Save PDF ===
        p.showPage()
        p.save()
        return response
