from django.urls import path
from .views import AddressListCreateView, AddressDetailView, AddressSetDefaultView


urlpatterns = [
    path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<uuid:address_uuid>/', AddressDetailView.as_view(), name='address-detail'),
    path('addresses/<uuid:address_uuid>/set-default/', AddressSetDefaultView.as_view(), name='address-set-default'),
]


