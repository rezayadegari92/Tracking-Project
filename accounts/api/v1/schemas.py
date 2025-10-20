"""
Swagger/OpenAPI schemas for Accounts API v1.

This module contains comprehensive OpenAPI schemas for the accounts application,
including user registration, authentication, profile management, and password operations.
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    PasswordChangeSerializer
)


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

# User Registration Schemas
user_registration_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm'],
    properties={
        'username': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Unique username for the user',
            max_length=150,
            example='john_doe'
        ),
        'email': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_EMAIL,
            description='User email address',
            example='john.doe@example.com'
        ),
        'first_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User first name',
            max_length=30,
            example='John'
        ),
        'last_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User last name',
            max_length=150,
            example='Doe'
        ),
        'password': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User password (must meet Django password validation requirements)',
            min_length=8,
            write_only=True,
            example='SecurePass123!'
        ),
        'password_confirm': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Password confirmation (must match password)',
            min_length=8,
            write_only=True,
            example='SecurePass123!'
        )
    }
)

user_registration_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='User ID',
            example=1
        ),
        'username': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Username',
            example='john_doe'
        ),
        'email': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_EMAIL,
            description='Email address',
            example='john.doe@example.com'
        ),
        'first_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='First name',
            example='John'
        ),
        'last_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Last name',
            example='Doe'
        ),
        'user_type': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User type',
            example='customer'
        ),
        'date_joined': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description='Account creation date',
            example='2024-01-15T10:30:00Z'
        ),
        'last_login': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description='Last login date',
            example='2024-01-15T10:30:00Z'
        )
    }
)

# User Login Schemas
user_login_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', 'password'],
    properties={
        'username': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Username or email',
            example='john_doe'
        ),
        'password': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User password',
            example='SecurePass123!'
        )
    }
)

user_login_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'access': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='JWT access token',
            example='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
        ),
        'refresh': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='JWT refresh token',
            example='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
        ),
        'user': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='User information',
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                'username': openapi.Schema(type=openapi.TYPE_STRING, example='john_doe'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, example='john.doe@example.com'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, example='John'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='Doe'),
                'user_type': openapi.Schema(type=openapi.TYPE_STRING, example='customer'),
                'date_joined': openapi.Schema(type=openapi.TYPE_STRING, example='2024-01-15T10:30:00Z'),
                'last_login': openapi.Schema(type=openapi.TYPE_STRING, example='2024-01-15T10:30:00Z')
            }
        )
    }
)

# Password Change Schemas
password_change_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['old_password', 'new_password', 'new_password_confirm'],
    properties={
        'old_password': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Current password',
            example='OldPass123!'
        ),
        'new_password': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='New password (must meet Django password validation requirements)',
            min_length=8,
            example='NewSecurePass123!'
        ),
        'new_password_confirm': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='New password confirmation (must match new password)',
            min_length=8,
            example='NewSecurePass123!'
        )
    }
)

password_change_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Success message',
            example='Password changed successfully'
        )
    }
)

# Token Refresh Schemas
token_refresh_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['refresh'],
    properties={
        'refresh': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='JWT refresh token',
            example='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
        )
    }
)

token_refresh_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'access': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='New JWT access token',
            example='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
        )
    }
)

# Logout Schema
logout_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['refresh'],
    properties={
        'refresh': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='JWT refresh token to blacklist',
            example='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
        )
    }
)

logout_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Success message',
            example='Logout successful'
        )
    }
)

# Error Response Schema
error_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Error message',
            example='Invalid credentials'
        ),
        'detail': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Detailed error message',
            example='Authentication credentials were not provided.'
        ),
        'field_errors': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Field-specific validation errors',
            additional_properties=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING)
            ),
            example={'username': ['This field is required.']}
        )
    }
)


# =============================================================================
# API ENDPOINT SCHEMAS
# =============================================================================

def get_user_registration_schema():
    """Get swagger schema for user registration endpoint."""
    return swagger_auto_schema(
        operation_id='accounts_register_user',
        operation_summary='Register a new user account',
        operation_description="""
        Create a new user account in the system.
        
        **Requirements:**
        - Username must be unique
        - Email must be valid and unique
        - Password must meet Django's password validation requirements
        - Password confirmation must match the password
        - User type is automatically set to 'customer' by default
        
        **Password Requirements:**
        - Minimum 8 characters
        - Cannot be too common
        - Cannot be entirely numeric
        - Cannot be too similar to user information
        """,
        request_body=user_registration_request_schema,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                'User created successfully',
                user_registration_response_schema,
                examples={
                    'application/json': {
                        'id': 1,
                        'username': 'john_doe',
                        'email': 'john.doe@example.com',
                        'first_name': 'John',
                        'last_name': 'Doe',
                        'user_type': 'customer',
                        'date_joined': '2024-01-15T10:30:00Z',
                        'last_login': None
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                'Bad request - validation errors',
                error_response_schema,
                examples={
                    'application/json': {
                        'username': ['A user with that username already exists.'],
                        'password_confirm': ["Passwords don't match."]
                    }
                }
            )
        },
        tags=['Authentication']
    )


def get_user_login_schema():
    """Get swagger schema for user login endpoint."""
    return swagger_auto_schema(
        operation_id='accounts_login_user',
        operation_summary='Login and obtain JWT tokens',
        operation_description="""
        Authenticate user credentials and return JWT access and refresh tokens.
        
        **Authentication Flow:**
        1. Provide username/email and password
        2. System validates credentials
        3. Returns JWT access token (short-lived) and refresh token (long-lived)
        4. Use access token for authenticated requests
        5. Use refresh token to get new access tokens when expired
        
        **Token Usage:**
        - Access token: Include in Authorization header as `Bearer <token>`
        - Refresh token: Use to obtain new access tokens via `/api/v1/auth/token/refresh/`
        """,
        request_body=user_login_request_schema,
        responses={
            status.HTTP_200_OK: openapi.Response(
                'Login successful',
                user_login_response_schema,
                examples={
                    'application/json': {
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                        'user': {
                            'id': 1,
                            'username': 'john_doe',
                            'email': 'john.doe@example.com',
                            'first_name': 'John',
                            'last_name': 'Doe',
                            'user_type': 'customer',
                            'date_joined': '2024-01-15T10:30:00Z',
                            'last_login': '2024-01-15T10:30:00Z'
                        }
                    }
                }
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                'Invalid credentials',
                error_response_schema,
                examples={
                    'application/json': {
                        'error': 'Invalid credentials.'
                    }
                }
            )
        },
        tags=['Authentication']
    )


def get_token_refresh_schema():
    """Get swagger schema for token refresh endpoint."""
    return swagger_auto_schema(
        operation_id='accounts_refresh_token',
        operation_summary='Refresh JWT access token',
        operation_description="""
        Obtain a new JWT access token using a valid refresh token.
        
        **When to use:**
        - Access token has expired
        - Need to continue making authenticated requests
        
        **Token Lifecycle:**
        - Access tokens are short-lived (typically 15-60 minutes)
        - Refresh tokens are long-lived (typically 7-30 days)
        - Use refresh token to get new access tokens without re-authentication
        """,
        request_body=token_refresh_request_schema,
        responses={
            status.HTTP_200_OK: openapi.Response(
                'Token refreshed successfully',
                token_refresh_response_schema,
                examples={
                    'application/json': {
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                    }
                }
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                'Invalid refresh token',
                error_response_schema,
                examples={
                    'application/json': {
                        'detail': 'Token is invalid or expired'
                    }
                }
            )
        },
        tags=['Authentication']
    )


def get_logout_schema():
    """Get swagger schema for logout endpoint."""
    return swagger_auto_schema(
        operation_id='accounts_logout_user',
        operation_summary='Logout and blacklist refresh token',
        operation_description="""
        Logout user and blacklist the refresh token to prevent further use.
        
        **Security:**
        - Blacklists the provided refresh token
        - Prevents unauthorized access even if token is compromised
        - User will need to login again to get new tokens
        
        **Best Practice:**
        - Always logout when user explicitly logs out
        - Implement automatic logout on token expiration
        """,
        request_body=logout_request_schema,
        responses={
            status.HTTP_200_OK: openapi.Response(
                'Logout successful',
                logout_response_schema,
                examples={
                    'application/json': {
                        'message': 'Logout successful'
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                'Bad request - invalid refresh token',
                error_response_schema,
                examples={
                    'application/json': {
                        'error': 'Invalid refresh token'
                    }
                }
            )
        },
        tags=['Authentication']
    )


def get_user_profile_schema():
    """Get swagger schema for user profile endpoints."""
    return {
        'get': swagger_auto_schema(
            operation_id='accounts_get_profile',
            operation_summary='Get current user profile',
            operation_description="""
            Retrieve the current authenticated user's profile information.
            
            **Access:**
            - Requires authentication
            - Returns only the current user's data
            """,
            responses={
                status.HTTP_200_OK: openapi.Response(
                    'User profile',
                    user_registration_response_schema,
                    examples={
                        'application/json': {
                            'id': 1,
                            'username': 'john_doe',
                            'email': 'john.doe@example.com',
                            'first_name': 'John',
                            'last_name': 'Doe',
                            'user_type': 'customer',
                            'date_joined': '2024-01-15T10:30:00Z',
                            'last_login': '2024-01-15T10:30:00Z'
                        }
                    }
                ),
                status.HTTP_401_UNAUTHORIZED: openapi.Response(
                    'Authentication required',
                    error_response_schema
                )
            },
            tags=['User Profile']
        ),
        'patch': swagger_auto_schema(
            operation_id='accounts_update_profile',
            operation_summary='Update current user profile',
            operation_description="""
            Update the current authenticated user's profile information.
            
            **Updateable Fields:**
            - email
            - first_name
            - last_name
            
            **Restrictions:**
            - Cannot change username (immutable)
            - Cannot change password (use password change endpoint)
            - Cannot change ID, date_joined, last_login (system fields)
            """,
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_EMAIL,
                        description='User email address',
                        example='new.email@example.com'
                    ),
                    'first_name': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='User first name',
                        max_length=30,
                        example='John'
                    ),
                    'last_name': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='User last name',
                        max_length=150,
                        example='Doe'
                    )
                }
            ),
            responses={
                status.HTTP_200_OK: openapi.Response(
                    'Profile updated successfully',
                    user_registration_response_schema
                ),
                status.HTTP_400_BAD_REQUEST: openapi.Response(
                    'Bad request - validation errors',
                    error_response_schema
                ),
                status.HTTP_401_UNAUTHORIZED: openapi.Response(
                    'Authentication required',
                    error_response_schema
                )
            },
            tags=['User Profile']
        )
    }


def get_password_change_schema():
    """Get swagger schema for password change endpoint."""
    return swagger_auto_schema(
        operation_id='accounts_change_password',
        operation_summary='Change user password',
        operation_description="""
        Change the current authenticated user's password.
        
        **Security Requirements:**
        - Must provide current password for verification
        - New password must meet Django's password validation requirements
        - New password confirmation must match new password
        
        **Password Requirements:**
        - Minimum 8 characters
        - Cannot be too common
        - Cannot be entirely numeric
        - Cannot be too similar to user information
        """,
        request_body=password_change_request_schema,
        responses={
            status.HTTP_200_OK: openapi.Response(
                'Password changed successfully',
                password_change_response_schema,
                examples={
                    'application/json': {
                        'message': 'Password changed successfully'
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                'Bad request - validation errors',
                error_response_schema,
                examples={
                    'application/json': {
                        'old_password': ['Old password is incorrect.'],
                        'new_password_confirm': ["New passwords don't match."]
                    }
                }
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                'Authentication required',
                error_response_schema
            )
        },
        tags=['User Profile']
    )


# =============================================================================
# SCHEMA REGISTRY
# =============================================================================

# Dictionary mapping endpoint names to their schemas
ACCOUNTS_SCHEMAS = {
    'register': get_user_registration_schema(),
    'login': get_user_login_schema(),
    'token_refresh': get_token_refresh_schema(),
    'logout': get_logout_schema(),
    'profile': get_user_profile_schema(),
    'password_change': get_password_change_schema(),
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_schema_for_endpoint(endpoint_name):
    """
    Get the appropriate schema for a given endpoint.
    
    Args:
        endpoint_name (str): Name of the endpoint
        
    Returns:
        dict or function: The schema for the endpoint
    """
    return ACCOUNTS_SCHEMAS.get(endpoint_name)


def get_all_schemas():
    """
    Get all available schemas.
    
    Returns:
        dict: Dictionary of all schemas
    """
    return ACCOUNTS_SCHEMAS


# =============================================================================
# DYNAMIC SERIALIZER INTEGRATION
# =============================================================================

def create_dynamic_schema_from_serializer(serializer_class, operation_type='request'):
    """
    Create a dynamic OpenAPI schema from a Django REST Framework serializer.
    
    Args:
        serializer_class: The serializer class to convert
        operation_type (str): Type of operation ('request' or 'response')
        
    Returns:
        openapi.Schema: The generated OpenAPI schema
    """
    if not serializer_class:
        return None
    
    # Get serializer fields
    serializer = serializer_class()
    fields = serializer.get_fields()
    
    properties = {}
    required_fields = []
    
    for field_name, field in fields.items():
        # Map DRF field types to OpenAPI types
        if hasattr(field, 'child'):
            # Handle nested serializers
            if hasattr(field.child, 'Meta'):
                properties[field_name] = openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=create_dynamic_schema_from_serializer(field.child.__class__, operation_type)
                )
            else:
                properties[field_name] = openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING)
                )
        elif hasattr(field, 'Meta'):
            # Handle nested serializer
            properties[field_name] = create_dynamic_schema_from_serializer(field.__class__, operation_type)
        else:
            # Handle primitive fields
            field_type = get_openapi_field_type(field)
            field_schema = openapi.Schema(type=field_type)
            
            # Add field-specific properties
            if hasattr(field, 'help_text') and field.help_text:
                field_schema.description = field.help_text
            
            if hasattr(field, 'max_length') and field.max_length:
                field_schema.max_length = field.max_length
            
            if hasattr(field, 'min_length') and field.min_length:
                field_schema.min_length = field.min_length
            
            if hasattr(field, 'choices') and field.choices:
                field_schema.enum = [choice[0] for choice in field.choices]
            
            if field.write_only and operation_type == 'response':
                continue  # Skip write-only fields in response
            
            if field.read_only and operation_type == 'request':
                continue  # Skip read-only fields in request
            
            properties[field_name] = field_schema
            
            # Add to required fields if not optional
            if field.required and not field.read_only:
                required_fields.append(field_name)
    
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=properties,
        required=required_fields if required_fields else None
    )


def get_openapi_field_type(drf_field):
    """Map DRF field types to OpenAPI types."""
    field_type_mapping = {
        'CharField': openapi.TYPE_STRING,
        'EmailField': openapi.TYPE_STRING,
        'IntegerField': openapi.TYPE_INTEGER,
        'FloatField': openapi.TYPE_NUMBER,
        'DecimalField': openapi.TYPE_NUMBER,
        'BooleanField': openapi.TYPE_BOOLEAN,
        'DateTimeField': openapi.TYPE_STRING,
        'DateField': openapi.TYPE_STRING,
        'TimeField': openapi.TYPE_STRING,
        'URLField': openapi.TYPE_STRING,
        'UUIDField': openapi.TYPE_STRING,
        'FileField': openapi.TYPE_STRING,
        'ImageField': openapi.TYPE_STRING,
        'ChoiceField': openapi.TYPE_STRING,
        'MultipleChoiceField': openapi.TYPE_ARRAY,
        'ListField': openapi.TYPE_ARRAY,
        'DictField': openapi.TYPE_OBJECT,
    }
    
    field_class_name = drf_field.__class__.__name__
    return field_type_mapping.get(field_class_name, openapi.TYPE_STRING)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Schema functions
    'get_user_registration_schema',
    'get_user_login_schema',
    'get_token_refresh_schema',
    'get_logout_schema',
    'get_user_profile_schema',
    'get_password_change_schema',
    
    # Schema registry
    'ACCOUNTS_SCHEMAS',
    
    # Utility functions
    'get_schema_for_endpoint',
    'get_all_schemas',
    'create_dynamic_schema_from_serializer',
    'get_openapi_field_type',
    
    # Request/Response schemas
    'user_registration_request_schema',
    'user_registration_response_schema',
    'user_login_request_schema',
    'user_login_response_schema',
    'password_change_request_schema',
    'password_change_response_schema',
    'token_refresh_request_schema',
    'token_refresh_response_schema',
    'logout_request_schema',
    'logout_response_schema',
    'error_response_schema',
]
