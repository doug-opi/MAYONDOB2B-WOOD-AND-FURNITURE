# sales/signals.py
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import SaleItem
from inventory.models import Stock

# -------------------------------
# 1️⃣ Track old quantity (before update)
# -------------------------------
@receiver(pre_save, sender=SaleItem)
def track_old_quantity(sender, instance, **kwargs):
    """
    Before saving a SaleItem, store the old quantity
    so we can calculate the difference during an update.
    """
    if instance.pk:
        try:
            old_item = SaleItem.objects.get(pk=instance.pk)
            instance._old_quantity = old_item.quantity
        except SaleItem.DoesNotExist:
            instance._old_quantity = 0
    else:
        instance._old_quantity = 0


# -------------------------------
# 2️⃣ Update stock when SaleItem is created or updated
# -------------------------------
@receiver(post_save, sender=SaleItem)
def update_stock_on_save(sender, instance, created, **kwargs):
    """
    Adjust stock when a SaleItem is created or updated.
    """
    stock = Stock.objects.filter(product=instance.product).first()
    if not stock:
        print(f"⚠️ No stock record found for product {instance.product}")
        return

    if created:
        if stock.quantity < instance.quantity:
            raise ValidationError(f"Insufficient stock for {instance.product.name}")
        stock.quantity -= instance.quantity
    else:
        # Adjust by difference
        difference = instance.quantity - instance._old_quantity
        if difference > 0 and stock.quantity < difference:
            raise ValidationError(f"Insufficient stock for {instance.product.name}")
        stock.quantity -= difference

    stock.save()

    # Optional: alert if stock is low
    if hasattr(stock, "is_low_stock") and callable(stock.is_low_stock):
        if stock.is_low_stock():
            print(f"⚠️ Low stock alert: {stock.product.name} only has {stock.quantity} left!")


# -------------------------------
# 3️⃣ Restore stock when SaleItem is deleted
# -------------------------------
@receiver(post_delete, sender=SaleItem)
def update_stock_on_delete(sender, instance, **kwargs):
    """
    When a SaleItem is deleted, restore its quantity back to stock.
    """
    if not instance.product or not instance.quantity:
        return

    stock = Stock.objects.filter(product=instance.product).first()
    if stock:
        stock.quantity += instance.quantity
        stock.save()

        if hasattr(stock, "is_low_stock") and callable(stock.is_low_stock):
            if stock.is_low_stock():
                print(f"⚠️ Low stock alert: {stock.product.name} only has {stock.quantity} left!")
    else:
        # Log or print a warning instead of crashing
        print(f"⚠️ No stock record found when deleting SaleItem for {instance.product}")

















# sales/signals.py
#from django.db.models.signals import post_save, post_delete, pre_save
#from django.dispatch import receiver
#from .models import SaleItem
#from inventory.models import Stock
#from django.core.exceptions import ValidationError
#from django.contrib import messages
# Keep track of old quantities when updating
#@receiver(pre_save, sender=SaleItem)
#def track_old_quantity(sender, instance, **kwargs):
#    if instance.pk:  # means it's an update, not a new record
#        old_item = SaleItem.objects.get(pk=instance.pk)
#        instance._old_quantity = old_item.quantity
#    else:
#        instance._old_quantity = 0


# When a SaleItem is created or updated
#@receiver(post_save, sender=SaleItem)
#def update_stock_on_save(sender, instance, created, **kwargs):
#    stock = Stock.objects.filter(product=instance.product).first()
#    if not stock:
#        return  # safety check: product must exist in inventory

#    if created:
#        if stock.quantity < instance.quantity:
#            raise ValidationError(f"Insufficient stock for {instance.product.name}")
        # New sale item → reduce stock
#        stock.quantity -= instance.quantity
#    else:
        # Updating existing sale item → adjust by difference
#        difference = instance.quantity - instance._old_quantity
#        if stock.quantity < difference:
#            raise ValidationError(f"Insufficient stock for {instance.product.name}")
#        stock.quantity -= difference

#    stock.save()


# When a SaleItem is deleted
#@receiver(post_delete, sender=SaleItem)
#def update_stock_on_delete(sender, instance, **kwargs):
#    if instance.product and instance.quantity:
#       stock = Stock.objects.filter(product=instance.product).first()
#       if stock:
        # Restore stock since sale item is gone
#           stock.quantity += instance.quantity
#           stock.save()

# 🔔 Alert if stock is low
#    if stock.is_low_stock():
#        print(f"⚠️ Low stock alert: {stock.product.name} only has {stock.quantity} left!")  
        # Later: send email/notification