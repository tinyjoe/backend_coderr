from django.contrib import admin
from django.urls import path

from .views import OfferCreateView, SingleOfferDetailView

urlpatterns = [
    path('offers/', OfferCreateView.as_view(), name='offer-create'),
    path('offers/<int:pk>/', SingleOfferDetailView.as_view(), name='offer-detail'),
]