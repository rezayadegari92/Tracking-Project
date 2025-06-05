from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from shipments.models import Shipment, Shipper, Country, City, Service

class ShipmentValidationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass123', email='test@example.com')
        self.client.login(username='testuser', password='testpass123')
        self.country = Country.objects.create(name='Test Country')
        self.city = City.objects.create(name='Test City', country=self.country)
        self.shipper = Shipper.objects.create(
            shipper_name='Test Shipper',
            address='Test Address',
            contact_person='Test Contact',
            contact_number='1234567890',
            shipper_country=self.country,
            shipper_city=self.city
        )
        self.service = Service.objects.create(name='Test Service')

    def test_required_fields_validation(self):
        response = self.client.post(reverse('shipment_create'), {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'receiver_name', 'This field is required.')
        self.assertFormError(response, 'form', 'receiver_address', 'This field is required.')
        self.assertFormError(response, 'form', 'receiver_contact_person', 'This field is required.')
        self.assertFormError(response, 'form', 'receiver_contact_number', 'This field is required.')
        self.assertFormError(response, 'form', 'product_type', 'This field is required.')
        self.assertFormError(response, 'form', 'service', 'This field is required.')
        self.assertFormError(response, 'form', 'quantity', 'This field is required.')
        self.assertFormError(response, 'form', 'grossweight', 'This field is required.')
        self.assertFormError(response, 'form', 'length', 'This field is required.')
        self.assertFormError(response, 'form', 'width', 'This field is required.')
        self.assertFormError(response, 'form', 'height', 'This field is required.')
        self.assertFormError(response, 'form', 'item_description', 'This field is required.')
        self.assertFormError(response, 'form', 'identity_image', 'This field is required.')

    def test_optional_fields_validation(self):
        data = {
            'receiver_name': 'Test Receiver',
            'receiver_address': 'Test Address',
            'receiver_contact_person': 'Test Contact',
            'receiver_contact_number': '1234567890',
            'product_type': 'doc',
            'service': self.service.id,
            'quantity': 1,
            'grossweight': 1.0,
            'length': 1.0,
            'width': 1.0,
            'height': 1.0,
            'item_description': 'Test Description',
            'identity_image': 'test_image.jpg',
            'price_of_shipment': 100.00
        }
        response = self.client.post(reverse('shipment_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Shipment.objects.filter(receiver_name='Test Receiver').exists()) 