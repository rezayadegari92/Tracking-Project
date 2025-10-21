from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from cities_light.models import Country, City
from shipments.models import Shipment, ShipmentImage
from shipments.utils.pdf_generator import (
    generate_shipment_confirmation_pdf,
    generate_shipment_detailed_pdf,
    generate_shipment_label_pdf
)
from .serializers import (
    CountrySerializer, CitySerializer, ShipmentCreateSerializer,
    ShipmentDetailSerializer, ShipmentListSerializer, ShipmentTrackingSerializer
)
from .permissions import IsStaffOrReadOnly, IsOwnerOrAdmin, IsPublicTracking


class CountryListView(generics.ListAPIView):
    """
    List all countries.
    """
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code2', 'code3']
    
    @swagger_auto_schema(
        operation_description="Get list of all countries",
        responses={
            200: openapi.Response('List of countries', CountrySerializer(many=True))
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CityListView(generics.ListAPIView):
    """
    List cities, optionally filtered by country.
    """
    queryset = City.objects.all().order_by('name')
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country']
    search_fields = ['name']
    
    @swagger_auto_schema(
        operation_description="Get list of cities, optionally filtered by country",
        manual_parameters=[
            openapi.Parameter(
                'country',
                openapi.IN_QUERY,
                description="Filter cities by country ID",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response('List of cities', CitySerializer(many=True))
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ShipmentCreateView(generics.CreateAPIView):
    """
    Create a new shipment.
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentCreateSerializer
    permission_classes = [AllowAny]  # Allow public shipment creation
    
    @swagger_auto_schema(
        operation_description="Create a new shipment",
        request_body=ShipmentCreateSerializer,
        responses={
            201: openapi.Response('Shipment created successfully', ShipmentDetailSerializer),
            400: 'Bad request - validation errors'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ShipmentListView(generics.ListAPIView):
    """
    List user's shipments (authenticated users only).
    """
    serializer_class = ShipmentListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product_type', 'service', 'payment_status']
    search_fields = ['awb_number', 'reference_number', 'receiver_name']
    ordering_fields = ['created_at', 'awb_number']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        return Shipment.objects.filter(created_by=user)
    
    @swagger_auto_schema(
        operation_description="Get list of user's shipments",
        responses={
            200: openapi.Response('List of shipments', ShipmentListSerializer(many=True)),
            401: 'Authentication required'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ShipmentDetailView(generics.RetrieveAPIView):
    """
    Retrieve detailed shipment information.
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'id'
    
    @swagger_auto_schema(
        operation_description="Get detailed shipment information",
        responses={
            200: openapi.Response('Shipment details', ShipmentDetailSerializer),
            401: 'Authentication required',
            404: 'Shipment not found'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([IsPublicTracking])
@swagger_auto_schema(
    operation_description="Track shipment by AWB or REF number",
    manual_parameters=[
        openapi.Parameter(
            'tracking_number',
            openapi.IN_QUERY,
            description="AWB or REF tracking number",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response('Shipment tracking information', ShipmentTrackingSerializer),
        400: 'Invalid tracking number format',
        404: 'Shipment not found'
    }
)
def track_shipment(request):
    """
    Track shipment by AWB or REF number (public access).
    """
    tracking_number = request.GET.get('tracking_number')
    
    if not tracking_number:
        return Response(
            {'error': 'Tracking number is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        if tracking_number.startswith('AWB-'):
            shipment = Shipment.objects.get(awb_number=tracking_number)
        elif tracking_number.startswith('REF-'):
            shipment = Shipment.objects.get(reference_number=tracking_number)
        else:
            return Response(
                {'error': 'Invalid tracking number format. Use AWB- or REF- prefix.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ShipmentTrackingSerializer(shipment)
        return Response(serializer.data)
        
    except Shipment.DoesNotExist:
        return Response(
            {'error': 'Shipment not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


class ShipmentConfirmationPDFView(generics.GenericAPIView):
    """
    Generate shipment confirmation PDF (client version).
    """
    permission_classes = [AllowAny]  # Allow public access for paid shipments
    
    @swagger_auto_schema(
        operation_description="Generate shipment confirmation PDF",
        responses={
            200: openapi.Response('PDF file', content_type='application/pdf'),
            404: 'Shipment not found'
        }
    )
    def get(self, request, id):
        shipment = get_object_or_404(Shipment, id=id)
        return generate_shipment_confirmation_pdf(shipment)


class ShipmentDetailedPDFView(generics.GenericAPIView):
    """
    Generate detailed shipment PDF (admin version).
    """
    permission_classes = [IsAdminUser]
    
    @swagger_auto_schema(
        operation_description="Generate detailed shipment PDF (admin only)",
        responses={
            200: openapi.Response('PDF file', content_type='application/pdf'),
            403: 'Admin access required',
            404: 'Shipment not found'
        }
    )
    def get(self, request, id):
        shipment = get_object_or_404(Shipment, id=id)
        return generate_shipment_detailed_pdf(shipment)


class ShipmentLabelPDFView(generics.GenericAPIView):
    """
    Generate shipment label PDF (admin version).
    """
    permission_classes = [IsAdminUser]
    
    @swagger_auto_schema(
        operation_description="Generate shipment label PDF (admin only)",
        responses={
            200: openapi.Response('PDF file', content_type='application/pdf'),
            403: 'Admin access required',
            404: 'Shipment not found'
        }
    )
    def get(self, request, id):
        shipment = get_object_or_404(Shipment, id=id)
        return generate_shipment_label_pdf(shipment)
