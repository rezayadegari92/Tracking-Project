from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from profiles.models import Address
from .serializers import AddressSerializer, AddressCreateUpdateSerializer


class AddressListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).order_by('-default_address', 'id')

    @swagger_auto_schema(
        request_body=AddressCreateUpdateSerializer,
        responses={201: AddressSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = AddressCreateUpdateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(AddressSerializer(instance).data, status=status.HTTP_201_CREATED)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    lookup_field = 'address_uuid'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    @swagger_auto_schema(request_body=AddressCreateUpdateSerializer, responses={200: AddressSerializer})
    def patch(self, request, *args, **kwargs):
        address = self.get_object()
        serializer = AddressCreateUpdateSerializer(address, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(AddressSerializer(instance).data)


class AddressSetDefaultView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'address_uuid'

    @swagger_auto_schema(responses={200: 'Default address set'})
    def post(self, request, address_uuid):
        address = get_object_or_404(Address, user=request.user, address_uuid=address_uuid)
        address.default_address = True
        address.save()
        return Response({'detail': 'Default address set'}, status=status.HTTP_200_OK)


