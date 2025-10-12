from django.urls import path
from .views import (
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    StockListView, StockCreateView, StockUpdateView, StockDeleteView,StockLevelReportView,StockReportPDFView

)

urlpatterns = [
    # Product URLs
    path("products/", ProductListView.as_view(), name="product_list"),
    #path('product/<int:pk>/toggle/', ToggleProductStatusView.as_view(), name='toggle_product_status'),
    path("products/add/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path('stock-report/', StockLevelReportView.as_view(), name='stock_level_report'),
   path('download-stock-report/', StockReportPDFView.as_view(), name='download_stock_report'),

    # Stock URLs
    path("stocks/", StockListView.as_view(), name="stock_list"),
    path("stocks/add/", StockCreateView.as_view(), name="stock_create"),
    path("stocks/<int:pk>/edit/", StockUpdateView.as_view(), name="stock_update"),
    path("stocks/<int:pk>/delete/", StockDeleteView.as_view(), name="stock_delete"),
]


#PRODUCT LIST.HTML
#{% extends "base.html" %}
#{% block title %}Products{% endblock %}
#{% block content %}
#<div class="d-flex justify-content-between align-items-center mb-3">
#    <h2>Products</h2>
#    <a href="{% url 'product_create' %}" class="btn btn-primary">+ Add Product</a>
#</div>

#<table class="table table-striped table-bordered">
#    <thead class="table-dark">
#        <tr>
#            <th>Name</th>
#            <th>Type</th>
#            <th>Description</th>
#            <th>Actions</th>
#        </tr>
#    </thead>
#    <tbody>
#        {% for product in products %}
#        <tr>
#            <td>{{ product.name }}</td>
#            <td>{{ product.type }}</td>
#            <td>{{ product.description }}</td>
#            <td>
#             
#            <td>
#              <a href="{% url 'product_update' product.pk %}" class="btn btn-sm btn-warning">Edit</a>  
#              <a href="{% url 'product_delete' product.pk %}" class="btn btn-sm btn-danger">Delete</a> 
#            </td>
#        </tr>
#        {% empty %}
#        <tr><td colspan="4" class="text-center">No products available.</td></tr>
#        {% endfor %}
#    </tbody>
#</table>
#{% endblock %}



#stock_level_report.html

#{% extends "base.html" %}
#{% load static %}
#{% load humanize %}

#{% block content %}
#<div class="container mt-4">
 # <h2 class="mb-3 text-center">📦 Stock Level Report</h2>

 # <div class="row text-center mb-4">
 #   <div class="col-md-3">
 #     <div class="card bg-success text-white shadow">
 #       <div class="card-body">
 #         <h5>Available</h5>
 #         <h3>{{ available_count }}</h3>
 #       </div>
 #     </div>
 #   </div>
 #   <div class="col-md-3">
 #     <div class="card bg-warning text-dark shadow">
 #       <div class="card-body">
 #         <h5>Low Stock (≤5)</h5>
 #         <h3>{{ low_stock_count }}</h3>
 #       </div>
 #     </div>
 #   </div>
 #   <div class="col-md-3">
 #     <div class="card bg-danger text-white shadow">
 #       <div class="card-body">
 #         <h5>Out of Stock</h5>
 #         <h3>{{ out_of_stock_count }}</h3>
 #       </div>
 #     </div>
 #   </div>
 #   <div class="col-md-3">
 #     <div class="card bg-primary text-white shadow">
 #       <div class="card-body">
 #         <h5>Total Stock Value</h5>
 #         <h3>{{ total_stock_value|intcomma }} UGX</h3>
 #       </div>
 #     </div>
 #   </div>
 # </div>

  #<div class="d-flex justify-content-end mb-3">
  #  <a href="{% url 'download_stock_report' %}" class="btn btn-outline-danger">
  #    <i class="bi bi-file-earmark-pdf"></i> Download PDF Report
  #  </a>
  #</div>

#  <table class="table table-hover table-bordered">
#    <thead class="table-dark">
#      <tr>
#        <th>Product</th>
#        <th>Category</th>
#        <th>Quantity</th>
#        <th>Unit Price (UGX)</th>
#        <th>Total Value (UGX)</th>
#      </tr>
#    </thead>
#    <tbody>
#      {% for product in products %}
#      <tr class="
#          {% if product.quantity == 0 %}
#            table-danger
#          {% elif product.quantity <= 5 %}
#            table-warning
#          {% else %}
#            table-success
#          {% endif %}
#        ">
#        <td>{{ product.name }}</td>
#        <td>{{ product.category.name }}</td>
#        <td>{{ product.quantity }}</td>
#        <td>{{ product.unit_price|intcomma }}</td>
#        <td>{{ product.stock_value|intcomma }}</td>
#      </tr>
#      {% empty %}
#      <tr><td colspan="5" class="text-center">No products found.</td></tr>
#      {% endfor %}
#    </tbody>
#  </table>

#  {% if is_paginated %}
#  <div class="pagination justify-content-center">
#    {% if page_obj.has_previous %}
#    <a href="?page={{ page_obj.previous_page_number }}" class="btn btn-outline-secondary btn-sm">Previous</a>
#    {% endif %}
#    <span class="mx-2">Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span>
#    {% if page_obj.has_next %}
#    <a href="?page={{ page_obj.next_page_number }}" class="btn btn-outline-secondary btn-sm">Next</a>
#    {% endif %}
#  </div>
#  {% endif %}
#</div>
#{% endblock %}







#STOCK LIST.HTML
#<!--{% extends "base.html" %}
#{% block title %}Stock{% endblock %}
#{% block content %}
#<div class="d-flex justify-content-between align-items-center mb-3">
#    <h2>Stock</h2>
#    <a href="{% url 'stock_create' %}" class="btn btn-primary">+ Add Stock</a>
#</div>

#<table class="table table-striped table-bordered">
#    <thead class="table-dark">
#        <tr>
#            <th>Product</th>
#            <th>Supplier</th>
#            <th>Quantity</th>
#            <th>Cost Price</th>
#            <th>Selling Price</th>
#            <th>Actions</th>
#        </tr>
#    </thead>
#    <tbody>
#        {% for stock in stocks %}
#        <tr>
#            <td>{{ stock.product.name }}</td>
#            <td>{{ stock.supplier_name }}</td>
#            <td>{{ stock.quantity }}</td>
#            <td>{{ stock.cost_price }}</td>
#            <td>{{ stock.selling_price }}</td>
#            <td>
#                <a href="{% url 'stock_update' stock.pk %}" class="btn btn-sm btn-warning">Edit</a>
#                <a href="{% url 'stock_delete' stock.pk %}" class="btn btn-sm btn-danger">Delete</a>
#            </td>
#        </tr>
#        {% empty %}
#        <tr><td colspan="6" class="text-center">No stock records available.</td></tr>
#        {% endfor %}
#    </tbody>
#</table>
#{% endblock %}

#PRODUCT LIST.HTML
#{% extends "base.html" %}
#{% block title %}Products{% endblock %}
#{% block content %}
#<div class="d-flex justify-content-between align-items-center mb-3">
#    <h2>Products</h2>
#    <a href="{% url 'product_create' %}" class="btn btn-primary">+ Add Product</a>
#</div>

#<table class="table table-striped table-bordered">
#    <thead class="table-dark">
#        <tr>
#            <th>Name</th>
#            <th>Type</th>
#            <th>Description</th>
#            <th>Actions</th>
#        </tr>
#    </thead>
#    <tbody>
#        {% for product in products %}
#        <tr>
#            <td>{{ product.name }}</td>
#            <td>{{ product.type }}</td>
#            <td>{{ product.description }}</td>
#            <td>
#             
#            <td>
#              <a href="{% url 'product_update' product.pk %}" class="btn btn-sm btn-warning">Edit</a>  
#              <a href="{% url 'product_delete' product.pk %}" class="btn btn-sm btn-danger">Delete</a> 
#            </td>
#        </tr>
#        {% empty %}
#        <tr><td colspan="4" class="text-center">No products available.</td></tr>
#        {% endfor %}
#    </tbody>
#</table>
#{% endblock %}

