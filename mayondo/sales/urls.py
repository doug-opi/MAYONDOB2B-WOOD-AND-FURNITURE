from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path("", views.SaleListView.as_view(), name="sale_list"),
    path("sale/<int:pk>/", views.SaleDetailView.as_view(), name="sale_detail"),
    path("sale/new/", views.SaleCreateWithItemsView.as_view(), name="sale_create"), 
    #path("sale/new/", views.SaleCreateView.as_view(), name="sale_create"),
    path("sale/<int:pk>/edit/", views.SaleUpdateView.as_view(), name="sale_edit"),
    path("sale/<int:pk>/delete/", views.SaleDeleteView.as_view(), name="sale_delete"),

    # Sale Items
    path("sale/<int:pk>/add-item/", views.SaleItemCreateView.as_view(), name="add_item"),
    path("item/<int:pk>/edit/", views.SaleItemUpdateView.as_view(), name="item_edit"),
    path("sale/<int:pk>/invoice/", views.SaleInvoicePDFView.as_view(), name="sale_invoice"),
    path("item/<int:pk>/delete/", views.SaleItemDeleteView.as_view(), name="item_delete"),
    path('sales-report/', views.SalesReportView.as_view(), name='sales_report'),
    path('download-sales-report/', views.DownloadSalesReportPDFView.as_view(), name='download_sales_report_pdf'),
    path("analytics/", views.SalesAnalyticsView.as_view(), name="sales_analytics"),
]
#SALE FORM.HTML
#{% extends "base.html" %}
#{% load crispy_forms_tags %}
#{% block content %}
#<div class="container mt-4">
#    <h2>New Sale</h2>
#    <form method="post" class="card p-4 shadow-sm" novalidate>
#        {% csrf_token %}
#        {{ form.non_field_errors }}
#        <div class="mb-3">
#            {{ form.customer_name.label_tag }}
#            {{ form.customer_name }}
#            {{ form.customer_name.errors }}
#        </div>
#        <div class="mb-3">
#            {{ form.payment_type.label_tag }}
#            {{ form.payment_type }}
#            {{ form.payment_type.errors }}
#        </div>
#        <div class="form-check mb-3">
#            {{ form.transport_required }}
#            {{ form.transport_required.label_tag }}
#            {{ form.transport_required.errors }}
#        </div>
#        <button type="submit" class="btn btn-primary">Save Sale</button>
#    </form>
#</div>
#{% endblock %}
