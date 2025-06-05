from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from ..models import Shipment, Shipper
from cities_light.models import Country, City
from ..forms import ShipmentForm

class ShipmentCreationTest(TestCase):
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
        
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
    def test_create_shipment_page(self):
        """Test accessing the create shipment page"""
        response = self.client.get(reverse('create_shipment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shipments/create_shipment.html')
        
    def test_create_valid_shipment(self):
        """Test creating a valid shipment"""
        shipment_data = {
            'shipper': self.shipper.id,
            'receiver_name': 'Test Receiver',
            'receiver_address': '456 Test Ave',
            'receiver_country': self.country.id,
            'receiver_city': self.city.id,
            'receiver_contact_person': 'Test Receiver Contact',
            'receiver_contact_number': '0987654321',
            'product_type': 'document',
            'service': 'express',
            'quantity': 1,
            'grossweight': 1.0,
            'width': 10,
            'length': 10,
            'height': 10,
            'item_description': 'Test Item',
            'payment_status': 'paid'
        }
        
        response = self.client.post(reverse('create_shipment'), shipment_data)
        
        # Check if shipment was created
        self.assertEqual(Shipment.objects.count(), 1)
        
        # Check if redirected to success page
        self.assertEqual(response.status_code, 302)
        self.assertIn('success', response.url)
        
        # Verify shipment details
        shipment = Shipment.objects.first()
        self.assertEqual(shipment.receiver_name, 'Test Receiver')
        self.assertEqual(shipment.product_type, 'document')
        self.assertEqual(shipment.service, 'express')
        
    def test_create_invalid_shipment(self):
        """Test creating an invalid shipment"""
        # Missing required fields
        shipment_data = {
            'shipper': self.shipper.id,
            'receiver_name': 'Test Receiver',
            # Missing other required fields
        }
        
        response = self.client.post(reverse('create_shipment'), shipment_data)
        
        # Check if shipment was not created
        self.assertEqual(Shipment.objects.count(), 0)
        
        # Check if form errors are displayed
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'receiver_address', 'This field is required.')
        
    def test_shipment_creation_with_payment(self):
        """Test shipment creation with payment status"""
        shipment_data = {
            'shipper': self.shipper.id,
            'receiver_name': 'Test Receiver',
            'receiver_address': '456 Test Ave',
            'receiver_country': self.country.id,
            'receiver_city': self.city.id,
            'receiver_contact_person': 'Test Receiver Contact',
            'receiver_contact_number': '0987654321',
            'product_type': 'document',
            'service': 'express',
            'quantity': 1,
            'grossweight': 1.0,
            'width': 10,
            'length': 10,
            'height': 10,
            'item_description': 'Test Item',
            'payment_status': 'paid',
            'price_of_shipment': 100.00
        }
        
        response = self.client.post(reverse('create_shipment'), shipment_data)
        
        # Check if shipment was created
        self.assertEqual(Shipment.objects.count(), 1)
        
        # Verify AWB number was generated
        shipment = Shipment.objects.first()
        self.assertTrue(shipment.awb_number.startswith('AWB-'))
        
    def test_shipment_creation_without_payment(self):
        """Test shipment creation without payment"""
        shipment_data = {
            'shipper': self.shipper.id,
            'receiver_name': 'Test Receiver',
            'receiver_address': '456 Test Ave',
            'receiver_country': self.country.id,
            'receiver_city': self.city.id,
            'receiver_contact_person': 'Test Receiver Contact',
            'receiver_contact_number': '0987654321',
            'product_type': 'document',
            'service': 'express',
            'quantity': 1,
            'grossweight': 1.0,
            'width': 10,
            'length': 10,
            'height': 10,
            'item_description': 'Test Item',
            'payment_status': 'pending'
        }
        
        response = self.client.post(reverse('create_shipment'), shipment_data)
        
        # Check if shipment was created
        self.assertEqual(Shipment.objects.count(), 1)
        
        # Verify AWB number is not generated
        shipment = Shipment.objects.first()
        self.assertEqual(shipment.awb_number, '0')
        
    def test_unauthorized_shipment_creation(self):
        """Test shipment creation without authentication"""
        # Logout the user
        self.client.logout()
        
        response = self.client.get(reverse('create_shipment'))
        
        # Check if redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url) 