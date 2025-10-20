from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer, 
    PasswordChangeSerializer
)
from .permissions import IsOwnerOrAdmin

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Register a new user account.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Register a new user account",
        responses={
            201: openapi.Response('User created successfully', UserSerializer),
            400: 'Bad request - validation errors'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    """
    Login and obtain JWT tokens.
    """
    serializer_class = UserLoginSerializer
    
    @swagger_auto_schema(
        operation_description="Login and obtain JWT access and refresh tokens",
        responses={
            200: openapi.Response('Login successful', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='User information')
                }
            )),
            401: 'Invalid credentials'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })


class LogoutView(generics.GenericAPIView):
    """
    Logout and blacklist refresh token.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Logout and blacklist refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token to blacklist')
            },
            required=['refresh']
        ),
        responses={
            200: 'Logout successful',
            400: 'Bad request - invalid refresh token'
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update user profile.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get_object(self):
        return self.request.user
    
    @swagger_auto_schema(
        operation_description="Get current user profile",
        responses={
            200: openapi.Response('User profile', UserSerializer),
            401: 'Authentication required'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Update current user profile",
        responses={
            200: openapi.Response('Profile updated', UserSerializer),
            400: 'Bad request - validation errors',
            401: 'Authentication required'
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class PasswordChangeView(generics.GenericAPIView):
    """
    Change user password.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Change user password",
        request_body=PasswordChangeSerializer,
        responses={
            200: 'Password changed successfully',
            400: 'Bad request - validation errors',
            401: 'Authentication required'
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


# Token refresh endpoint
class TokenRefreshView(TokenRefreshView):
    """
    Refresh JWT access token.
    """
    
    @swagger_auto_schema(
        operation_description="Refresh JWT access token using refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
            },
            required=['refresh']
        ),
        responses={
            200: openapi.Response('Token refreshed', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='New access token')
                }
            )),
            401: 'Invalid refresh token'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
