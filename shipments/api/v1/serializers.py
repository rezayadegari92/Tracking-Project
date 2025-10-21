from rest_framework import serializers
from django.shortcuts import get_object_or_404
from cities_light.models import Country, City
from shipments.models import Shipper, Shipment, ShipmentImage
from profiles.models import Address


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for country information."""
    
    class Meta:
        model = Country
        fields = ('id', 'name', 'code2', 'code3')


class CitySerializer(serializers.ModelSerializer):
    """Serializer for city information."""
    country = CountrySerializer(read_only=True)
    
    class Meta:
        model = City
        fields = ('id', 'name', 'country')


class ShipperSerializer(serializers.ModelSerializer):
    """Serializer for shipper information."""
    country = CountrySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    country_id = serializers.IntegerField(write_only=True)
    city_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Shipper
        fields = (
            'id', 'shipper_name', 'address', 'country', 'city', 
            'country_id', 'city_id', 'zip_code', 'location',
            'contact_person', 'contact_number', 'mobile_number', 'identity_image'
        )
        read_only_fields = ('id',)
    
    def validate_country_id(self, value):
        try:
            Country.objects.get(id=value)
        except Country.DoesNotExist:
            raise serializers.ValidationError("Invalid country ID.")
        return value
    
    def validate_city_id(self, value):
        try:
            City.objects.get(id=value)
        except City.DoesNotExist:
            raise serializers.ValidationError("Invalid city ID.")
        return value
    
    def create(self, validated_data):
        country_id = validated_data.pop('country_id')
        city_id = validated_data.pop('city_id')
        
        country = Country.objects.get(id=country_id)
        city = City.objects.get(id=city_id)
        
        shipper = Shipper.objects.create(
            country=country,
            city=city,
            **validated_data
        )
        return shipper


class ShipmentImageSerializer(serializers.ModelSerializer):
    """Serializer for shipment images."""
    
    class Meta:
        model = ShipmentImage
        fields = ('id', 'image', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_at')


class ShipmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating shipments."""
    shipper = ShipperSerializer()
    images = ShipmentImageSerializer(many=True, read_only=True)
    address_uuid = serializers.UUIDField(required=False, write_only=True)
    
    class Meta:
        model = Shipment
        fields = (
            'id', 'shipper', 'receiver_name', 'receiver_address',
            'receiver_country', 'receiver_city', 'receiver_zip_code',
            'receiver_location', 'receiver_contact_person', 'receiver_contact_number',
            'receiver_mobile_number', 'product_type', 'service', 'quantity',
            'grossweight', 'width', 'length', 'height', 'item_description',
            'special_instruction', 'cod_amount', 'base_price', 'additional_charges',
            'images', 'awb_number', 'reference_number', 'payment_status', 'address_uuid',
            'chargeable_weight', 'volumetricks', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'awb_number', 'reference_number', 'payment_status',
            'chargeable_weight', 'volumetricks', 'created_at', 'updated_at'
        )
    
    def create(self, validated_data):
        shipper_data = validated_data.pop('shipper')
        address_uuid = validated_data.pop('address_uuid', None)
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        if address_uuid and user and user.is_authenticated:
            address = get_object_or_404(Address, user=user, address_uuid=address_uuid)
            shipper_data.setdefault('shipper_name', user.get_full_name() or user.username)
            shipper_data.setdefault('address', address.address)
            shipper_data.setdefault('country_id', address.country_id)
            shipper_data.setdefault('city_id', address.city_id)
            shipper_data.setdefault('zip_code', address.zip_code)
            shipper_data.setdefault('location', address.location)
            shipper_data.setdefault('contact_number', address.contact_number)
            shipper_data.setdefault('mobile_number', address.mobile_number)

        shipper_serializer = ShipperSerializer(data=shipper_data)
        shipper_serializer.is_valid(raise_exception=True)
        shipper = shipper_serializer.save()

        create_kwargs = {
            'shipper': shipper,
            'payment_status': 'pending',
            **validated_data,
        }
        if user and user.is_authenticated:
            create_kwargs['created_by'] = user

        shipment = Shipment.objects.create(**create_kwargs)
        return shipment


class ShipmentDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed shipment information."""
    shipper = ShipperSerializer(read_only=True)
    receiver_country = CountrySerializer(read_only=True)
    receiver_city = CitySerializer(read_only=True)
    images = ShipmentImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Shipment
        fields = (
            'id', 'shipper', 'receiver_name', 'receiver_address',
            'receiver_country', 'receiver_city', 'receiver_zip_code',
            'receiver_location', 'receiver_contact_person', 'receiver_contact_number',
            'receiver_mobile_number', 'awb_number', 'reference_number',
            'forwarder', 'product_type', 'service', 'payment_status',
            'quantity', 'grossweight', 'chargeable_weight', 'width', 'length',
            'height', 'volumetricks', 'price_of_shipment', 'item_description',
            'special_instruction', 'cod_amount', 'base_price', 'additional_charges',
            'images', 'created_at', 'updated_at'
        )


class ShipmentListSerializer(serializers.ModelSerializer):
    """Serializer for shipment list view."""
    shipper_name = serializers.CharField(source='shipper.shipper_name', read_only=True)
    receiver_country_name = serializers.CharField(source='receiver_country.name', read_only=True)
    receiver_city_name = serializers.CharField(source='receiver_city.name', read_only=True)
    
    class Meta:
        model = Shipment
        fields = (
            'id', 'awb_number', 'reference_number', 'shipper_name',
            'receiver_name', 'receiver_country_name', 'receiver_city_name',
            'product_type', 'service', 'payment_status', 'created_at'
        )


class ShipmentTrackingSerializer(serializers.ModelSerializer):
    """Serializer for public shipment tracking."""
    shipper_name = serializers.CharField(source='shipper.shipper_name', read_only=True)
    receiver_country_name = serializers.CharField(source='receiver_country.name', read_only=True)
    receiver_city_name = serializers.CharField(source='receiver_city.name', read_only=True)
    
    class Meta:
        model = Shipment
        fields = (
            'awb_number', 'reference_number', 'shipper_name', 'receiver_name',
            'receiver_country_name', 'receiver_city_name', 'product_type',
            'service', 'payment_status', 'created_at'
        )
