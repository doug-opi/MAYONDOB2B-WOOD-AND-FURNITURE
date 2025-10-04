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


















































































#def add_item(request, pk):
 #   sale = get_object_or_404(Sale, pk=pk)
  #  if request.method == "POST":
   #     form = SaleItemForm(request.POST)
    #    if form.is_valid():
     #       item = form.save(commit=False)
      #      item.sale = sale
       #     item.save()
        #    return redirect("sales:sale_detail", pk=sale.pk)
   # else:
    #    form = SaleItemForm()
    #return render(request, "sales/saleitem_form.html", {"form": form})
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