from django.urls import path
from . import views

urlpatterns = [
    path('create-shipment/', views.create_shipment, name='create-shipment'),
    # Add other URLs as needed
]