from drf_yasg import openapi


AddressSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'address_uuid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid'),
        'address': openapi.Schema(type=openapi.TYPE_STRING),
        'country': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'code2': openapi.Schema(type=openapi.TYPE_STRING),
                'code3': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        'city': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'country': openapi.Schema(type=openapi.TYPE_OBJECT),
            },
        ),
        'zip_code': openapi.Schema(type=openapi.TYPE_STRING),
        'location': openapi.Schema(type=openapi.TYPE_STRING),
        'contact_number': openapi.Schema(type=openapi.TYPE_STRING),
        'mobile_number': openapi.Schema(type=openapi.TYPE_STRING),
        'identity_image': openapi.Schema(type=openapi.TYPE_STRING, format='binary'),
        'default_address': openapi.Schema(type=openapi.TYPE_BOOLEAN),
    },
)


AddressCreateUpdateSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['address', 'country_id', 'city_id'],
    properties={
        'address': openapi.Schema(type=openapi.TYPE_STRING),
        'country_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'city_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'zip_code': openapi.Schema(type=openapi.TYPE_STRING),
        'location': openapi.Schema(type=openapi.TYPE_STRING),
        'contact_number': openapi.Schema(type=openapi.TYPE_STRING),
        'mobile_number': openapi.Schema(type=openapi.TYPE_STRING),
        'identity_image': openapi.Schema(type=openapi.TYPE_STRING, format='binary'),
        'set_default': openapi.Schema(type=openapi.TYPE_BOOLEAN),
    },
)


