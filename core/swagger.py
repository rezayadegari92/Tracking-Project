from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Shipment Tracking API",
        default_version='v1',
        description="""
        A comprehensive API for shipment tracking and management system.
        
        ## Features
        - User authentication and registration with JWT tokens
        - Shipment creation and management
        - Public shipment tracking by AWB/REF numbers
        - PDF generation for confirmations, detailed reports, and labels
        - Country and city data for form dropdowns
        
        ## Authentication
        This API uses JWT (JSON Web Token) authentication. To authenticate:
        1. Register a new account or login to get access and refresh tokens
        2. Include the access token in the Authorization header: `Bearer <access_token>`
        3. Use the refresh token to get new access tokens when they expire
        
        ## Public Endpoints
        - Shipment creation (no authentication required)
        - Shipment tracking by AWB/REF number
        - Country and city lists
        - Confirmation PDF generation
        
        ## Authenticated Endpoints
        - User profile management
        - Shipment listing and details
        - Password change
        
        ## Admin Endpoints
        - Detailed PDF generation
        - Label PDF generation
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@shipmenttracking.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
