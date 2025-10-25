from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min

from coderr_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, SingleOfferDetailSerializer, OfferDetailSerializer
from .permissions import IsBusinessUser
from .pagination import OfferPagination
from .filters import OfferQueryHelper
from .ordering import OfferOrderingHelper


class OfferListCreateView(generics.ListCreateAPIView):
    """
    GET: View for receiving a list of filtered Offers.
    POST: Creates new instances of the Offer model with permission restrictions for business users.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = OfferPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user']  
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'details__price']
    ordering = ['-updated_at']

    def get_queryset(self):
        queryset = Offer.objects.all().prefetch_related('details', 'user')
        queryset = OfferQueryHelper.add_annotations(queryset)
        queryset = OfferQueryHelper.apply_filters(queryset, self.request.query_params)
        ordering_param = self.request.query_params.get('ordering')
        queryset = OfferOrderingHelper.apply_ordering(queryset, ordering_param)
        return queryset
    
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