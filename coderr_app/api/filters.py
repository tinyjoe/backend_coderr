from django_filters import rest_framework as filters
from django.db.models import Min, Max
from coderr_app.models import Offer


class OfferFilter(filters.FilterSet):
    """
    FilterSet for filtering Offer instances based on creator ID, minimum price, and maximum delivery time.
    """
    creator_id = filters.NumberFilter(field_name="user__id", lookup_expr="exact")
    min_price = filters.NumberFilter(method='filter_min_price')
    max_delivery_time = filters.NumberFilter(method='filter_max_delivery_time')

    class Meta:
        model = Offer
        fields = ['creator_id']

    def filter_min_price(self, queryset, name, value):
        """
        Filters offers with a minimum price greater than or equal to value.
        """
        return queryset.annotate(_min_price=Min('details__price')).filter(_min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        """
        Filters offers with a maximum delivery time greater than or equal to value.
        """
        return queryset.annotate(_max_delivery_time=Max('details__delivery_time_in_days')).filter(_max_delivery_time__gte=value)
