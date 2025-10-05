from django.urls import path
from .views import (
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    StockListView, StockCreateView, StockUpdateView, StockDeleteView,StockLevelReportView
)

urlpatterns = [
    # Product URLs
    path("products/", ProductListView.as_view(), name="product_list"),
    #path('product/<int:pk>/toggle/', ToggleProductStatusView.as_view(), name='toggle_product_status'),
    path("products/add/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path('stock-report/', StockLevelReportView.as_view(), name='stock_level_report'),

    # Stock URLs
    path("stocks/", StockListView.as_view(), name="stock_list"),
    path("stocks/add/", StockCreateView.as_view(), name="stock_create"),
    path("stocks/<int:pk>/edit/", StockUpdateView.as_view(), name="stock_update"),
    path("stocks/<int:pk>/delete/", StockDeleteView.as_view(), name="stock_delete"),
]
