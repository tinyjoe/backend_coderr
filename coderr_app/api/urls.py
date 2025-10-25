from django.contrib import admin
from django.urls import path

from .views import OfferListCreateView, SingleOfferDetailView, OfferDetailView

urlpatterns = [
    path('offers/', OfferListCreateView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', SingleOfferDetailView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offerdetail-detail'),
]