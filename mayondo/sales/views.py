from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django.db import transaction
from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemForm, SaleItemFormSet

class SaleListView(ListView):
    model = Sale
    template_name = "sale_list.html"
    context_object_name = "sales"


class SaleDetailView(DetailView):
    model = Sale
    template_name = "sale_detail.html"
    context_object_name = "sale"


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "sale_form.html"
    success_url = reverse_lazy("sales:sale_list")

    #def form_valid(self, form):
     #   form.instance.sales_agent = self.request.user
      #  response = super().form_valid(form)
       # return redirect("sales:add_item", pk=self.object.pk)
    def form_valid(self, form):
        
        if self.request.user.is_authenticated:
            form.instance.sales_agent = self.request.user
        else:
            # Assign a default user (e.g., the first one in the database)
            form.instance.sales_agent = User.objects.first()
        return super().form_valid(form)


class SaleItemCreateView(CreateView):
    model = SaleItem
    form_class = SaleItemForm
    template_name = "saleitem_form.html"

    def form_valid(self, form):
        sale_id = self.kwargs['pk']
        form.instance.sale_id = sale_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("sales:sale_detail", kwargs={"pk": self.kwargs['pk']})
    
class SaleUpdateView(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = "sale_form.html"

    def get_success_url(self):
        return reverse("sales:sale_detail", kwargs={"pk": self.object.pk})


class SaleDeleteView(DeleteView):
    model = Sale
    template_name = "sale_confirm_delete.html"
    success_url = reverse_lazy("sales:sale_list")



from .utils import generate_invoice_pdf

class SaleInvoicePDFView(View):
    def get(self, request, pk):
        sale = get_object_or_404(Sale, pk=pk)
        return generate_invoice_pdf(sale.id)

from django.views.generic import ListView
from django.db.models import Sum, Count
from django.utils import timezone
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from .models import Sale, SaleItem
from datetime import timedelta

from django.db.models import (
    Sum, F, DecimalField, ExpressionWrapper, OuterRef, Subquery
)

#class SalesReportView(ListView):
#    model = Sale
#    template_name = 'sales_report.html'
#    context_object_name = 'sales'

#    def get_queryset(self):
#        # Default: last 30 days
#        start_date = self.request.GET.get('start_date')
#        end_date = self.request.GET.get('end_date')

#        if start_date and end_date:
#            queryset = Sale.objects.filter(created_at__range=[start_date, end_date])
#        else:
#            today = timezone.now().date()
#            queryset = Sale.objects.filter(created_at__gte=today - timedelta(days=30))

#        return queryset.order_by('-created_at')

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        sales = context['sales']

        # Aggregations
#        context['total_sales'] = sales.aggregate(total=Sum('total_amount'))['total'] or 0
#        context['sale_count'] = sales.count()
#        context['sales_by_payment'] = (
#            sales.values('payment_type')
#            .annotate(total=Sum('total_amount'))
#            .order_by('-total')
#        )
#        return context

class SalesReportView(ListView):
    model = Sale
    template_name = 'sales_report.html'
    context_object_name = 'sales'

    def get_queryset(self):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        queryset = Sale.objects.all()
        if start_date and end_date:
            queryset = queryset.filter(created_at__range=[start_date, end_date])
        else:
            from django.utils import timezone
            from datetime import timedelta
            today = timezone.now().date()
            queryset = queryset.filter(created_at__gte=today - timedelta(days=30))

        # Annotate total per sale
        total_subquery = (
            SaleItem.objects.filter(sale=OuterRef('pk'))
            .values('sale')
            .annotate(total=Sum(ExpressionWrapper(F('quantity') * F('unit_price'), output_field=DecimalField())))
            .values('total')[:1]
        )

        queryset = queryset.annotate(total_amount=Subquery(total_subquery))
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales = context['sales']

        context['total_sales'] = sum(s.total_amount or 0 for s in sales)
        context['sale_count'] = sales.count()
        context['sales_by_payment'] = (
            sales.values('payment_type')
            .annotate(total=Sum('total_amount'))
            .order_by('-total')
        )
        return context



class DownloadSalesReportPDFView(View):
    def get(self, request, *args, **kwargs):
        # Create HTTP response with PDF headers
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="sales_report.pdf"'

        # Initialize PDF
        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        # Header
        p.setFont("Helvetica-Bold", 16)
        p.drawString(180, height - 50, "XYZ WOOD & FURNITURE LTD")
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 80, "Sales Report")

        # Data
        sales = Sale.objects.all().order_by('-created_at')
        total_sales = sales.aggregate(total=Sum('total_amount'))['total'] or 0

        # Table headers
        y = height - 120
        p.setFont("Helvetica-Bold", 11)
        p.drawString(50, y, "Date")
        p.drawString(150, y, "Customer")
        p.drawString(350, y, "Payment Type")
        p.drawString(480, y, "Total (UGX)")
        y -= 20
        p.line(50, y, 550, y)
        y -= 15
        p.setFont("Helvetica", 10)

        # Table rows
        for sale in sales:
            if y < 80:
                p.showPage()
                y = height - 80
                p.setFont("Helvetica-Bold", 11)
                p.drawString(50, y, "Date")
                p.drawString(150, y, "Customer")
                p.drawString(350, y, "Payment Type")
                p.drawString(480, y, "Total (UGX)")
                y -= 20
                p.line(50, y, 550, y)
                y -= 15
                p.setFont("Helvetica", 10)

            # Draw sale row
            p.drawString(50, y, sale.created_at.strftime('%d-%m-%Y'))
            p.drawString(150, y, sale.customer_name[:18])
            p.drawString(350, y, sale.payment_type)
            p.drawRightString(550, y, f"{sale.total_amount:,.0f}")
            y -= 18

        # Footer summary
        y -= 15
        p.line(50, y, 550, y)
        p.setFont("Helvetica-Bold", 11)
        y -= 20
        p.drawString(400, y, "Total Sales:")
        p.drawRightString(550, y, f"{total_sales:,.0f} UGX")

        # Footer note
        y -= 40
        p.setFont("Helvetica-Oblique", 9)
        p.drawString(50, y, "Goods once sold are not returnable.")
        p.drawString(50, y - 15, "For inquiries or complaints, contact +256 700 000000 or info@xyzfurniture.com")

        # Finalize
        p.showPage()
        p.save()

        return response



 #<!-- <a href="{% url 'download_sales_report_pdf' %}" class="btn btn-danger">
 #     <i class="bi bi-file-earmark-pdf"></i> Download PDF
 #   </a>-->



#SALES ANALYTICS
from django.views.generic import TemplateView
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.utils import timezone
from datetime import timedelta
from .models import Sale, SaleItem

class SalesAnalyticsView(TemplateView):
    template_name = "sales_analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # --- Annotate each sale with its total amount ---
        sales = Sale.objects.annotate(
            total_amount=Sum(
                ExpressionWrapper(
                    F("items__quantity") * F("items__unit_price"),
                    output_field=DecimalField()
                )
            )
        )

        # --- Total sales (computed directly from SaleItem, not nested aggregate) ---
        total_sales = (
            SaleItem.objects.aggregate(
                total=Sum(
                    ExpressionWrapper(
                        F("quantity") * F("unit_price"),
                        output_field=DecimalField()
                    )
                )
            )["total"]
            or 0
        )

        sale_count = sales.count()
        average_sale = total_sales / sale_count if sale_count else 0

        # --- Top 5 customers ---
        top_customers = (
            sales.values("customer_name")
            .annotate(total=Sum(
                ExpressionWrapper(
                    F("items__quantity") * F("items__unit_price"),
                    output_field=DecimalField()
                )
            ))
            .order_by("-total")[:5]
        )

        # --- Top 5 products ---
        top_products = (
            SaleItem.objects.values("product__name")
            .annotate(
                total=Sum(
                    ExpressionWrapper(F("quantity") * F("unit_price"), output_field=DecimalField())
                )
            )
            .order_by("-total")[:5]
        )

        # --- Payment breakdown ---
        payment_breakdown = (
            sales.values("payment_type")
            .annotate(
                total=Sum(
                    ExpressionWrapper(
                        F("items__quantity") * F("items__unit_price"),
                        output_field=DecimalField()
                    )
                )
            )
            .order_by("-total")
        )

        # --- Sales trend (last 30 days) ---
        today = timezone.now().date()
        last_30 = today - timedelta(days=30)
        trend_data = (
            SaleItem.objects.filter(sale__created_at__date__gte=last_30)
            .values("sale__created_at__date")
            .annotate(
                total=Sum(
                    ExpressionWrapper(F("quantity") * F("unit_price"), output_field=DecimalField())
                )
            )
            .order_by("sale__created_at__date")
        )

        # --- Add to context ---
        context.update({
            "total_sales": total_sales,
            "sale_count": sale_count,
            "average_sale": average_sale,
            "top_customers": top_customers,
            "top_products": top_products,
            "payment_breakdown": payment_breakdown,
            "trend_data": trend_data,
        })

        return context


class SaleItemCreateView(CreateView):
    model = SaleItem
    form_class = SaleItemForm
    template_name = "saleitem_form.html"

    def form_valid(self, form):
        sale = get_object_or_404(Sale, pk=self.kwargs["pk"])
        form.instance.sale = sale
        if self.request.user.is_authenticated:
            form.instance.sale.sales_agent = self.request.user
        else:
            form.instance.sale.sales_agent = User.objects.first()
        form.instance.sale.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("sales:sale_detail", kwargs={"pk": self.kwargs["pk"]})



class SaleItemUpdateView(UpdateView):
    model = SaleItem
    form_class = SaleItemForm
    template_name = "saleitem_form.html"
  
    def get_success_url(self):
        return reverse("sales:sale_detail", kwargs={"pk": self.object.sale.pk})


class SaleItemDeleteView(DeleteView):
    model = SaleItem
    template_name = "saleitem_confirm_delete.html"

    def get_success_url(self):
        return reverse("sales:sale_detail", kwargs={"pk": self.object.sale.pk})

class SaleCreateWithItemsView(View):
    def get(self, request):
        form = SaleForm()
        formset = SaleItemFormSet()
        return render(request, "sale_with_items_form.html", {"form": form, "formset": formset})
    def post(self, request):
        form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # 1. Save sale first
                    sale = form.save(commit=False)
                    sale.sales_agent = None   # since no auth
                    sale.save()

                    # 2. Link sale to each item manually
                    items = formset.save(commit=False)
                    for item in items:
                        item.sale = sale
                        item.save()

                    # 3. Delete any marked for deletion
                    for obj in formset.deleted_objects:
                        obj.delete()

                return redirect("sales:sale_detail", pk=sale.pk)

            except Exception as e:
                form.add_error(None, f"Error saving sale: {e}")

        return render(request, "sale_with_items_form.html", {"form": form, "formset": formset})















































































   # def post(self, request):
    #    form = SaleForm(request.POST)
     #   formset = SaleItemFormSet(request.POST)
#
 #       if form.is_valid() and formset.is_valid():
  #          sale = form.save(commit=False)
   #         # temporarily assign dummy sales_agent until accounts app is added
    #        sale.sales_agent_id = 1  # Replace with request.user.id once accounts app is ready
     #       sale.save()
      #      formset.instance = sale
       #     formset.save()
        #    return redirect("sales:sale_detail", pk=sale.pk)
#
 #       return render(request, "sales/sale_with_items_form.html", {"form": form, "formset": formset})