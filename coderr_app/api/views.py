from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from coderr_app.models import Offer
from .serializers import OfferCreateSerializer, SingleOfferDetailSerializer
from .permissions import IsBusinessUser

class OfferCreateView(generics.CreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferCreateSerializer
    permission_classes = [IsBusinessUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
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