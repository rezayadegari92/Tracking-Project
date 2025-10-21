from rest_framework import serializers
from profiles.models import Address
from cities_light.models import Country, City


class CountryLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name", "code2", "code3")


class CityLiteSerializer(serializers.ModelSerializer):
    country = CountryLiteSerializer(read_only=True)

    class Meta:
        model = City
        fields = ("id", "name", "country")


class AddressSerializer(serializers.ModelSerializer):
    country = CountryLiteSerializer(read_only=True)
    city = CityLiteSerializer(read_only=True)

    class Meta:
        model = Address
        fields = (
            "address_uuid", "address", "country", "city", "zip_code", "location",
            "contact_number", "mobile_number", "identity_image", "default_address",
        )
        read_only_fields = ("address_uuid", "default_address")


class AddressCreateUpdateSerializer(serializers.ModelSerializer):
    country_id = serializers.IntegerField(write_only=True)
    city_id = serializers.IntegerField(write_only=True)
    set_default = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = Address
        fields = (
            "address", "country_id", "city_id", "zip_code", "location",
            "contact_number", "mobile_number", "identity_image", "set_default",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        set_default = validated_data.pop("set_default", False)
        country_id = validated_data.pop("country_id")
        city_id = validated_data.pop("city_id")
        instance = Address.objects.create(
            user=user,
            country_id=country_id,
            city_id=city_id,
            default_address=set_default,
            **validated_data,
        )
        return instance

    def update(self, instance, validated_data):
        set_default = validated_data.pop("set_default", False)
        country_id = validated_data.pop("country_id", None)
        city_id = validated_data.pop("city_id", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if country_id is not None:
            instance.country_id = country_id
        if city_id is not None:
            instance.city_id = city_id
        if set_default:
            instance.default_address = True
        instance.save()
        return instance


