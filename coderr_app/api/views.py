from rest_framework import generics, status, filters, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min, Avg

from auth_app.models import CustomUser
from coderr_app.models import Offer, OfferDetail, Order, Review
from .serializers import OfferSerializer, SingleOfferDetailSerializer, OfferDetailSerializer, OfferCreateUpdateSerializer, OrderListCreateSerializer, OrderDetailSerializer, ProgressOrderListSerializer, CompletedOrderListSerializer, ReviewSerializer, ReviewDetailSerializer, BaseInfoSerializer
from .permissions import IsBusinessUser, IsAuthenticatedOrCustomerUser, IsReviewAuthor
from .pagination import OfferPagination


class OfferListCreateView(generics.ListCreateAPIView):
    """
    GET: View for receiving a list of filtered Offers.
    POST: Creates new instances of the Offer model with permission restrictions for business users.
    """
    queryset = Offer.objects.all()
    pagination_class = OfferPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user']  
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'details__price']
    ordering = ['-updated_at']

    def get_serializer_class(self):
        if self.request.method == 'PATCH' or self.request.method == 'POST':
            return OfferCreateUpdateSerializer
        return OfferSerializer
    
    def get_permissions(self):
        """
        For GET: No permissions required.
        For POST: Business-User.
        """
        if self.request.method == 'POST':
            return [IsBusinessUser()]
        return [AllowAny()]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        offer = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)   


class SingleOfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving a single Offer with its details.
    """
    queryset = Offer.objects.all()
    serializer_class = SingleOfferDetailSerializer
    permission_classes = [IsAuthenticated]


class OfferDetailView(generics.RetrieveAPIView):
    """
    View for retrieving a single OfferDetail.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]


class OfferDetailViewSet(viewsets.ModelViewSet):
    """
    ViewSet for OfferDetail model to provide CRUD operations.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class OrderView(generics.ListCreateAPIView):
    """
    View for listing and creating Orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderListCreateSerializer
    permission_classes = [IsAuthenticatedOrCustomerUser]


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single Order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticatedOrCustomerUser]


class ProgressOrderListView(generics.ListAPIView):
    """
    View for listing Orders with status 'in_progress'.
    """
    queryset = Order.objects.filter(status='in_progress')
    serializer_class = ProgressOrderListSerializer
    permission_classes = [IsAuthenticated]


class CompletedOrderListView(generics.ListAPIView):
    """
    View for listing Orders with status 'completed'.
    """
    queryset = Order.objects.filter(status='completed')
    serializer_class = CompletedOrderListSerializer
    permission_classes = [IsAuthenticated]


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating Reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrCustomerUser]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single Review.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsReviewAuthor]


class BaseInfoView(APIView):
    """
    View for retrieving BaseInfo statistics.
    """
    serializer = BaseInfoSerializer
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        data = {
            "review_count": Review.objects.count(),
            "average_rating": Review.objects.aggregate(Avg('rating'))['rating__avg'],
            "business_profile_count": CustomUser.objects.filter(type='business').count(),
            "offer_count": Offer.objects.count(),
        }
        return Response(data)
