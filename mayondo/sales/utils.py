from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Sale

def generate_invoice_pdf(sale_id):
    # Fetch the sale
    sale = Sale.objects.get(id=sale_id)
    
    # Create HTTP response with PDF headers
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{sale.id}.pdf"'

    # Create PDF object
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "XYZ WOOD & FURNITURE LTD")

    # Invoice header
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"Invoice #: {sale.id}")
    p.drawString(50, height - 120, f"Customer: {sale.customer_name}")
    p.drawString(50, height - 140, f"Payment Type: {sale.payment_type}")
    p.drawString(50, height - 160, f"Date: {sale.created_at.strftime('%d-%m-%Y')}")

    # Table headers
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 200, "Product")
    p.drawString(250, height - 200, "Quantity")
    p.drawString(350, height - 200, "Unit Price (UGX)")
    p.drawString(500, height - 200, "Total (UGX)")

    y = height - 220
    grand_total = 0

    # Sale items
    for item in sale.items.all():
        unit_price = (
            item.unit_price() if callable(item.unit_price) else item.unit_price
        )
        total_price = (
            item.total_price() if callable(item.total_price) else item.total_price
        )

        p.setFont("Helvetica", 11)
        p.drawString(50, y, item.product.name)
        p.drawString(250, y, str(item.quantity))
        p.drawString(350, y, f"{unit_price:,.0f}")
        p.drawString(500, y, f"{total_price:,.0f}")
        grand_total += total_price
        y -= 20

    # Total
    p.setFont("Helvetica-Bold", 12)
    p.drawString(400, y - 20, "Grand Total:")
    p.drawString(500, y - 20, f"{grand_total:,.0f} UGX")

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 50, "Thank you for shopping with XYZ Wood & Furniture.")

    p.showPage()
    p.save()
    return response
