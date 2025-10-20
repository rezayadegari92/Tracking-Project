import os
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import logging

logger = logging.getLogger(__name__)

def generate_barcode(awb_number):
    """Generate a Code128 barcode for the AWB number."""
    # Create a BytesIO object to store the barcode image
    buffer = BytesIO()
    
    # Generate the barcode
    code128 = Code128(awb_number, writer=ImageWriter())
    code128.write(buffer)
    
    # Get the image data and encode it to base64
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

def generate_shipment_confirmation_pdf(shipment):
    """Generate a confirmation PDF for the given shipment."""
    try:
        if not shipment:
            raise Http404("Shipment not found")
        
        # Generate barcode
        barcode_data = generate_barcode(shipment.awb_number)
        
        # Render HTML template
        html_string = render_to_string('shipments/pdf/shipment_pdf.html', {
            'shipment': shipment,
            'barcode_data': barcode_data,
            'company_name': 'Your Company Name',
            'company_address': 'Your Company Address',
            'company_phone': 'Your Company Phone',
            'company_email': 'Your Company Email',
            'generated_date': shipment.created_at,
        })
        
        # Configure fonts
        font_config = FontConfiguration()
        
        # Generate PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf(font_config=font_config)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="shipment_{shipment.awb_number}.pdf"'
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
        
    except Exception as e:
        logger.error(f"Error generating confirmation PDF for shipment {shipment.id}: {str(e)}")
        return HttpResponse(
            f"Error generating PDF: {str(e)}", 
            status=500, 
            content_type='text/plain'
        )

def generate_shipment_detailed_pdf(shipment):
    """Generate a detailed PDF for the given shipment."""
    try:
        if not shipment:
            raise Http404("Shipment not found")
        
        # Generate barcode
        barcode_data = generate_barcode(shipment.awb_number)
        
        # Render HTML template
        html_string = render_to_string('shipments/pdf/shipment_detailed.html', {
            'shipment': shipment,
            'barcode_data': barcode_data,
            'company_name': 'Your Company Name',
            'company_address': 'Your Company Address',
            'company_phone': 'Your Company Phone',
            'company_email': 'Your Company Email',
            'generated_date': shipment.created_at,
        })
        
        # Configure fonts
        font_config = FontConfiguration()
        
        # Generate PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf(font_config=font_config)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="shipment_detailed_{shipment.awb_number}.pdf"'
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
        
    except Exception as e:
        logger.error(f"Error generating detailed PDF for shipment {shipment.id}: {str(e)}")
        return HttpResponse(
            f"Error generating PDF: {str(e)}", 
            status=500, 
            content_type='text/plain'
        )

def generate_shipment_label_pdf(shipment):
    """Generate a shipping label PDF for the given shipment."""
    try:
        if not shipment:
            raise Http404("Shipment not found")
        
        # Generate barcode
        barcode_data = generate_barcode(shipment.awb_number)
        
        # Render HTML template
        html_string = render_to_string('shipments/pdf/shipment_label.html', {
            'shipment': shipment,
            'barcode_data': barcode_data,
            'company_name': 'Your Company Name',
            'company_address': 'Your Company Address',
            'company_phone': 'Your Company Phone',
            'company_email': 'Your Company Email',
            'generated_date': shipment.created_at,
        })
        
        # Configure fonts
        font_config = FontConfiguration()
        
        # Generate PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf(font_config=font_config)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="label_{shipment.awb_number}.pdf"'
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
        
    except Exception as e:
        logger.error(f"Error generating label PDF for shipment {shipment.id}: {str(e)}")
        return HttpResponse(
            f"Error generating PDF: {str(e)}", 
            status=500, 
            content_type='text/plain'
        ) 