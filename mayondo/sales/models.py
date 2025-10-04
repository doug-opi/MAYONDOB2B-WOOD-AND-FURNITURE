from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from inventory.models import Product

class Sale(models.Model):
    PAYMENT_TYPES = [
        ('cash', 'Cash'),
        ('credit', 'Credit'),
        ('mobile', 'Mobile Money'),
    ]

    customer_name = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    transport_required = models.BooleanField(default=False)
    sales_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale #{self.id} - {self.customer_name} ({self.payment_type})"

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def total_price(self):
        return self.quantity * self.unit_price
