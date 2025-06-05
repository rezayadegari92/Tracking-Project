import os
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
from django.http import HttpResponse

def generate_barcode(tracking_number):
    """Generate a barcode image for the given tracking number."""
    buffer = BytesIO()
    Code128(tracking_number, writer=ImageWriter()).write(buffer)
    return buffer.getvalue()

def generate_shipment_confirmation_pdf(shipment):
    """Generate a confirmation PDF for the given shipment."""
    # Generate barcode
    barcode_data = generate_barcode(shipment.awb_number)
    
    # Render HTML template
    html_string = render_to_string('shipments/pdf/shipment_pdf.html', {
        'shipment': shipment,
        'barcode_data': barcode_data,
    })
    
    # Generate PDF
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="shipment_{shipment.awb_number}.pdf"'
    return response

def generate_shipment_detailed_pdf(shipment):
    """Generate a detailed PDF for the given shipment."""
    # Generate barcode
    barcode_data = generate_barcode(shipment.awb_number)
    
    # Render HTML template
    html_string = render_to_string('shipments/pdf/shipment_pdf.html', {
        'shipment': shipment,
        'barcode_data': barcode_data,
    })
    
    # Generate PDF
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="shipment_detailed_{shipment.awb_number}.pdf"'
    return response

def generate_shipment_label_pdf(shipment):
    """Generate a shipping label PDF for the given shipment."""
    # Generate barcode
    barcode_data = generate_barcode(shipment.awb_number)
    
    # Render HTML template
    html_string = render_to_string('shipments/pdf/shipment_label.html', {
        'shipment': shipment,
        'barcode_data': barcode_data,
    })
    
    # Generate PDF
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="label_{shipment.awb_number}.pdf"'
    return response 