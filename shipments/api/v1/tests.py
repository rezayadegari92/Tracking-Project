from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from cities_light.models import Country, City
from shipments.models import Shipper, Shipment

User = get_user_model()


class ShipmentAPITestCase(APITestCase):
    """Test shipment API endpoints."""
    
    def setUp(self):
        # Create test data
        self.country = Country.objects.create(name='Test Country', code2='TC', code3='TCO')
        self.city = City.objects.create(name='Test City', country=self.country)
        self.shipper = Shipper.objects.create(
            shipper_name='Test Shipper',
            address='Test Address',
            country=self.country,
            city=self.city,
            contact_person='Test Contact',
            contact_number='1234567890'
        )
        self.shipment = Shipment.objects.create(
            shipper=self.shipper,
            receiver_name='Test Receiver',
            receiver_address='Test Receiver Address',
            receiver_country=self.country,
            receiver_city=self.city,
            receiver_contact_person='Test Receiver Contact',
            receiver_contact_number='0987654321',
            product_type='doc',
            service='outbound',
            quantity=1,
            grossweight=1.0,
            width=10.0,
            length=10.0,
            height=10.0,
            item_description='Test Item'
        )
    
    def test_country_list(self):
        """Test country list endpoint."""
        response = self.client.get(reverse('country-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_city_list(self):
        """Test city list endpoint."""
        response = self.client.get(reverse('city-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_city_list_filtered_by_country(self):
        """Test city list filtered by country."""
        response = self.client.get(f"{reverse('city-list')}?country={self.country.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_shipment_creation(self):
        """Test shipment creation."""
        data = {
            'shipper': {
                'shipper_name': 'New Shipper',
                'address': 'New Address',
                'country_id': self.country.id,
                'city_id': self.city.id,
                'contact_person': 'New Contact',
                'contact_number': '1111111111'
            },
            'receiver_name': 'New Receiver',
            'receiver_address': 'New Receiver Address',
            'receiver_country': self.country.id,
            'receiver_city': self.city.id,
            'receiver_contact_person': 'New Receiver Contact',
            'receiver_contact_number': '2222222222',
            'product_type': 'doc',
            'service': 'outbound',
            'quantity': 1,
            'grossweight': 1.0,
            'width': 10.0,
            'length': 10.0,
            'height': 10.0,
            'item_description': 'New Test Item'
        }
        response = self.client.post(reverse('shipment-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Shipment.objects.filter(receiver_name='New Receiver').exists())
    
    def test_shipment_tracking_by_awb(self):
        """Test shipment tracking by AWB number."""
        response = self.client.get(f"{reverse('shipment-track')}?tracking_number={self.shipment.awb_number}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['awb_number'], self.shipment.awb_number)
    
    def test_shipment_tracking_by_ref(self):
        """Test shipment tracking by REF number."""
        response = self.client.get(f"{reverse('shipment-track')}?tracking_number={self.shipment.reference_number}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reference_number'], self.shipment.reference_number)
    
    def test_shipment_tracking_invalid_number(self):
        """Test shipment tracking with invalid number."""
        response = self.client.get(f"{reverse('shipment-track')}?tracking_number=INVALID")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_shipment_tracking_not_found(self):
        """Test shipment tracking with non-existent number."""
        response = self.client.get(f"{reverse('shipment-track')}?tracking_number=AWB-999999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ShipmentDetailAPITestCase(APITestCase):
    """Test shipment detail API endpoints."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.country = Country.objects.create(name='Test Country', code2='TC', code3='TCO')
        self.city = City.objects.create(name='Test City', country=self.country)
        self.shipper = Shipper.objects.create(
            shipper_name='Test Shipper',
            address='Test Address',
            country=self.country,
            city=self.city,
            contact_person='Test Contact',
            contact_number='1234567890'
        )
        self.shipment = Shipment.objects.create(
            shipper=self.shipper,
            receiver_name='Test Receiver',
            receiver_address='Test Receiver Address',
            receiver_country=self.country,
            receiver_city=self.city,
            receiver_contact_person='Test Receiver Contact',
            receiver_contact_number='0987654321',
            product_type='doc',
            service='outbound',
            quantity=1,
            grossweight=1.0,
            width=10.0,
            length=10.0,
            height=10.0,
            item_description='Test Item'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_shipment_detail_authenticated(self):
        """Test accessing shipment detail with authentication."""
        response = self.client.get(reverse('shipment-detail', kwargs={'id': self.shipment.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.shipment.id)
    
    def test_shipment_detail_unauthenticated(self):
        """Test accessing shipment detail without authentication."""
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('shipment-detail', kwargs={'id': self.shipment.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_shipment_list_authenticated(self):
        """Test accessing shipment list with authentication."""
        response = self.client.get(reverse('shipment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_shipment_list_unauthenticated(self):
        """Test accessing shipment list without authentication."""
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('shipment-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
