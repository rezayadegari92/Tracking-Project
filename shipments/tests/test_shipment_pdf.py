from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from ..models import Shipment, Shipper
from cities_light.models import Country, City
import os
from django.conf import settings

class ShipmentPDFTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create test country and city
        self.country = Country.objects.create(name='Test Country')
        self.city = City.objects.create(
            name='Test City',
            country=self.country
        )
        
        # Create test shipper
        self.shipper = Shipper.objects.create(
            shipper_name='Test Shipper',
            address='123 Test St',
            city=self.city,
            country=self.country,
            contact_person='Test Contact',
            contact_number='1234567890'
        )
        
        # Create test shipment
        self.shipment = Shipment.objects.create(
            shipper=self.shipper,
            receiver_name='Test Receiver',
            receiver_address='456 Test Ave',
            receiver_country=self.country,
            receiver_city=self.city,
            receiver_contact_person='Test Receiver Contact',
            receiver_contact_number='0987654321',
            product_type='document',
            service='express',
            quantity=1,
            grossweight=1.0,
            width=10,
            length=10,
            height=10,
            item_description='Test Item',
            payment_status='paid'
        )
        
        self.client = Client()
        
    def test_shipment_confirmation_pdf(self):
        """Test shipment confirmation PDF generation"""
        # Login the user
        self.client.login(username='testuser', password='testpass123')
        
        # Get the PDF
        response = self.client.get(
            reverse('shipment_confirmation_pdf', args=[self.shipment.id])
        )
        
        # Check if response is successful
        self.assertEqual(response.status_code, 200)
        
        # Check if content type is PDF
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Check if filename is correct
        self.assertIn(
            f'attachment; filename="shipment_{self.shipment.awb_number}.pdf"',
            response['Content-Disposition']
        )
        
    def test_shipment_detailed_pdf(self):
        """Test detailed shipment PDF generation"""
        # Login the user
        self.client.login(username='testuser', password='testpass123')
        
        # Get the PDF
        response = self.client.get(
            reverse('shipment_detailed_pdf', args=[self.shipment.id])
        )
        
        # Check if response is successful
        self.assertEqual(response.status_code, 200)
        
        # Check if content type is PDF
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Check if filename is correct
        self.assertIn(
            f'attachment; filename="shipment_detailed_{self.shipment.awb_number}.pdf"',
            response['Content-Disposition']
        )
        
    def test_shipment_label_pdf(self):
        """Test shipping label PDF generation"""
        # Login the user
        self.client.login(username='testuser', password='testpass123')
        
        # Get the PDF
        response = self.client.get(
            reverse('shipment_label_pdf', args=[self.shipment.id])
        )
        
        # Check if response is successful
        self.assertEqual(response.status_code, 200)
        
        # Check if content type is PDF
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Check if filename is correct
        self.assertIn(
            f'attachment; filename="label_{self.shipment.awb_number}.pdf"',
            response['Content-Disposition']
        )
        
    def test_shipment_pdf_by_tracking(self):
        """Test PDF generation by tracking number"""
        # Login the user
        self.client.login(username='testuser', password='testpass123')
        
        # Get the PDF using AWB number
        response = self.client.get(
            reverse('shipment_pdf', args=[self.shipment.awb_number])
        )
        
        # Check if response is successful
        self.assertEqual(response.status_code, 200)
        
        # Check if content type is PDF
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Check if filename is correct
        self.assertIn(
            f'attachment; filename="shipment_{self.shipment.awb_number}.pdf"',
            response['Content-Disposition']
        )
        
    def test_invalid_shipment_pdf(self):
        """Test PDF generation for invalid shipment"""
        # Login the user
        self.client.login(username='testuser', password='testpass123')
        
        # Try to get PDF for non-existent shipment
        response = self.client.get(
            reverse('shipment_confirmation_pdf', args=[99999])
        )
        
        # Check if response is 404
        self.assertEqual(response.status_code, 404)
        
    def test_unauthorized_pdf_access(self):
        """Test PDF access without authentication"""
        # Try to get PDF without logging in
        response = self.client.get(
            reverse('shipment_confirmation_pdf', args=[self.shipment.id])
        )
        
        # Check if redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url) 