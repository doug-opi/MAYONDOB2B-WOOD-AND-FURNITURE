from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Sale
import os
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.conf import settings


def generate_invoice_pdf(sale_id):
    # Fetch the sale
    sale = Sale.objects.get(id=sale_id)
    
    # Create HTTP response with PDF headers
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="invoice_{sale.id}.pdf"'  # inline = print, not download

    # Create PDF canvas
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # === Add watermark logo ===
    logo_path = os.path.join(settings.BASE_DIR, "static/images/Flux_Dev_Create_a_professional_and_elegant_logo_for_MAYONDO_Wo_1.jpg")
    if os.path.exists(logo_path):
        p.saveState()
        p.translate(width / 2, height / 2)
        p.rotate(45)
        try:
            p.setFillAlpha(0.1)  # transparency for watermark
        except AttributeError:
            pass  # older reportlab versions may not support this
        p.drawImage(
            logo_path,
            -200, -200,
            width=400, height=400,
            preserveAspectRatio=True,
            mask="auto"
        )
        p.restoreState()

    # === Header ===
    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, height - 50, "MAYONDO WOOD & FURNITURE LTD")

    p.setFont("Helvetica", 11)
    p.drawString(50, height - 70, "Dealers in quality wooden furniture & timber products")
    p.drawString(50, height - 85, "Plot 12, Industrial Area, Kampala - Uganda")
    p.drawString(50, height - 100, "Tel: +256 700 123 456 | Email: info@mayondowf.com")

    # === Invoice Info ===
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 130, "INVOICE")
    p.setFont("Helvetica", 11)
    p.drawString(50, height - 150, f"Invoice No: {sale.id}")
    p.drawString(50, height - 165, f"Customer: {sale.customer_name}")
    p.drawString(50, height - 180, f"Payment Type: {sale.payment_type}")
    p.drawString(50, height - 195, f"Date: {sale.created_at.strftime('%d-%m-%Y')}")

    # === Table Data ===
    data = [["Product", "Quantity", "Unit Price (UGX)", "Total (UGX)"]]
    grand_total = 0

    for item in sale.items.all():
        unit_price = item.unit_price() if callable(item.unit_price) else item.unit_price
        total_price = item.total_price() if callable(item.total_price) else item.total_price
        data.append([
            item.product.name,
            str(item.quantity),
            f"{unit_price:,.0f}",
            f"{total_price:,.0f}"
        ])
        grand_total += total_price

    # Add total row
    data.append(["", "", "Grand Total:", f"{grand_total:,.0f} UGX"])

    # === Build Table ===
    table = Table(data, colWidths=[200, 80, 120, 120])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
        ("FONTNAME", (2, -1), (-1, -1), "Helvetica-Bold"),
    ]))

    # Place table
    table.wrapOn(p, width, height)
    table_height = len(data) * 20
    table.drawOn(p, 50, height - 250 - table_height)

    # === Footer Section ===
    footer_y = 80
    p.setFont("Helvetica", 10)
    p.drawString(50, footer_y, "Goods once sold are not returnable.")
    p.drawString(50, footer_y - 15, "For inquiries or complaints, contact: +256 700 123 456 | support@mayondowf.com")
    p.drawString(50, footer_y - 30, "Thank you for shopping with Mayondo Wood & Furniture Ltd.")

    # === Signature Line ===
    p.line(400, footer_y + 10, 550, footer_y + 10)
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(420, footer_y - 5, "Authorized Signature")

    # Finalize PDF
    p.showPage()
    p.save()
    return response
