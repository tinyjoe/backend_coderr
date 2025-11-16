from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min, Max, Avg, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotAuthenticated, NotFound, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from auth_app.models import CustomUser
from coderr_app.models import Offer, OfferDetail, Order, Review
from .serializers import OfferListSerializer, SingleOfferSerializer, OfferDetailSerializer, OfferCreateUpdateSerializer, OrderListCreateSerializer, OrderDetailSerializer, InProgressOrderCountSerializer, CompletedOrderCountSerializer, ReviewSerializer, ReviewDetailSerializer, BaseInfoSerializer
from .permissions import IsBusinessUser, IsAllowedToCreateOrUpdateOrDelete, IsReviewAuthor, IsAuthenticatedOrCreatorOfOffer
from .pagination import OfferPagination
from .filters import OfferFilter
from .handlers import handle_permission_denied_review


class OfferListCreateView(generics.ListCreateAPIView):
    """
    GET: View for receiving a list of filtered Offers.
    POST: Creates new instances of the Offer model with permission restrictions for business users.
    """
    queryset = Offer.objects.annotate(
        min_price_agg=Min("details__price"),
        min_delivery_agg=Min("details__delivery_time_in_days"),
    ).distinct()
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter 
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price', 'max_delivery_time']
    ordering = ['-updated_at']

    def get_serializer_class(self):
        """
        Uses different serializers for GET and POST requests.
        """
        if self.request.method == 'POST':
            return OfferCreateUpdateSerializer
        return OfferListSerializer
    
    def get_permissions(self):
        """
        For GET: No permissions required.
        For POST: Business-User.
        """
        if self.request.method == 'POST':
            return [IsBusinessUser()]
        return [AllowAny()]
    
    def create(self, request, *args, **kwargs):
        """
        POST handler for creating a new Offer.
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        offer = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)   


class SingleOfferView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving a single Offer with its details.
    """
    queryset = Offer.objects.all()
    serializer_class = SingleOfferSerializer
    permission_classes = [IsAuthenticatedOrCreatorOfOffer]

    def get_serializer_class(self):
        """
        Uses different serializers for PATCH and GET requests.
        """
        if self.request.method == 'PATCH':
            return OfferCreateUpdateSerializer
        return SingleOfferSerializer


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
    permission_classes = [IsAllowedToCreateOrUpdateOrDelete]

    def get_queryset(self):
        user = self.request.user.customuser
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )

    def post(self, request, *args, **kwargs):
        """POST handler for creating a new order."""
        user = request.user
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single Order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAllowedToCreateOrUpdateOrDelete]


class InProgressOrderCountView(generics.ListAPIView):
    """
    View for counting Orders with status 'in_progress'.
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    def get(self, request, *args, **kwargs):
        """Retrieves the count of in-progress orders."""
        user_id = self.kwargs.get('pk')
        business_user = get_object_or_404(CustomUser, id=user_id, type='business')
        count = Order.objects.filter(status='in_progress', offer_detail__offer__user__id=user_id).count()
        serializer = InProgressOrderCountSerializer({'order_count': count})
        return Response(serializer.data)


class CompletedOrderCountView(generics.ListAPIView):
    """
    View for counting Orders with status 'completed'.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        """Retrieves the count of completed orders."""
        user_id = self.kwargs.get('pk')
        business_user = get_object_or_404(CustomUser, id=user_id, type='business')
        count = Order.objects.filter(status='completed',  offer_detail__offer__user__id=user_id).count()
        serializer = CompletedOrderCountSerializer({'completed_order_count': count})
        return Response(serializer.data)


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating Reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAllowedToCreateOrUpdateOrDelete]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']

    def post(self, request, *args, **kwargs):
        """POST handler for creating a new review."""
        user = request.user
        if hasattr(user, 'customuser') and user.customuser.type == 'business':
            return handle_permission_denied_review(self)
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single Review.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsReviewAuthor]

    def patch(self, request, *args, **kwargs):
        """PATCH handler for updating a review."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        """DELETE handler for deleting a review."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class BaseInfoView(APIView):
    """
    View for retrieving BaseInfo statistics.
    """
    serializer = BaseInfoSerializer
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        """GET handler for retrieving base information statistics."""
        data = {
            "review_count": Review.objects.count(),
            "average_rating": Review.objects.aggregate(Avg('rating'))['rating__avg'],
            "business_profile_count": CustomUser.objects.filter(type='business').count(),
            "offer_count": Offer.objects.count(),
        }
        return Response(data)
