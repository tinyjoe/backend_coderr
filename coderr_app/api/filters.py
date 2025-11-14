from django_filters import rest_framework as filters
from django.db.models import Min, Max
from coderr_app.models import Offer


class OfferFilter(filters.FilterSet):
    """
    FilterSet for filtering Offer instances based on creator ID, minimum price, and maximum delivery time.
    """
    creator_id = filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    max_delivery_time = filters.NumberFilter(field_name='details__delivery_time_in_days', lookup_expr='lte')
    min_price = filters.NumberFilter(field_name='details__price', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['creator_id', 'max_delivery_time', 'min_price']
    
