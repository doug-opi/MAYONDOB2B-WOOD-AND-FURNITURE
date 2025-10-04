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
    path("item/<int:pk>/delete/", views.SaleItemDeleteView.as_view(), name="item_delete"),
]
