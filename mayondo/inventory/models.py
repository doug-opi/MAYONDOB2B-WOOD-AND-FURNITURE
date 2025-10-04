from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    """
    Represents a general product type (e.g. Sofa, Timber, Dining Table).
    """
    PRODUCT_TYPES = [
        ('wood', 'Wood'),
        ('furniture', 'Furniture'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=PRODUCT_TYPES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # NEW: soft status
    STATUS_AVAILABLE = 'AVAILABLE'
    STATUS_UNAVAILABLE = 'UNAVAILABLE'
    STATUS_DISCONTINUED = 'DISCONTINUED'
    STATUS_ARCHIVED = 'ARCHIVED'

    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_UNAVAILABLE, 'Unavailable'),
        (STATUS_DISCONTINUED, 'Discontinued'),
        (STATUS_ARCHIVED, 'Archived'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AVAILABLE,
        help_text="Product lifecycle status (soft delete / archival)."
    )

    def is_active(self):
        return self.status == self.STATUS_AVAILABLE

    def __str__(self):
        return self.name

    def __str__(self):
        return f"{self.name} ({self.type})"


class Stock(models.Model):
    """
    Represents stock entries for a product in the warehouse/showroom.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
    supplier_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quality = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    measurements = models.CharField(max_length=100, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # Threshold field for low stock alert
    low_stock_threshold = models.PositiveIntegerField(default=5)

    def is_low_stock(self):
       return self.quantity <= self.low_stock_threshold

    def __str__(self):
        return f"{self.product.name} - {self.quantity} in stock"

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"
