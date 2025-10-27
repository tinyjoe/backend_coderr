from django.urls import path, include
from rest_framework import routers

from .views import OfferListCreateView, SingleOfferDetailView, OfferDetailView, OfferDetailViewSet, OrderView, OrderDetailView, ProgressOrderListView, CompletedOrderListView

router = routers.DefaultRouter()
router.register(r'offerdetails', OfferDetailViewSet, basename='offerdetail')

urlpatterns = [
    path('offers/', OfferListCreateView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', SingleOfferDetailView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offerdetail-detail'),
    path('', include(router.urls)),
    path('orders/', OrderView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:pk>/', ProgressOrderListView.as_view(), name='progress-order-list'),
    path('completed-order-count/<int:pk>/', CompletedOrderListView.as_view(), name='completed-order-list'),
]