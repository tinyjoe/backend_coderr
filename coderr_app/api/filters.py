from django.db.models import Min

class OfferQueryHelper:
    """
    Helper class for constructing complex queries on the Offer model.
    """
    @staticmethod
    def add_annotations(queryset):
        """Adds calculated fields (e.g. min_price, min_delivery_time)."""
        return queryset.annotate(
            min_price_val=Min('details__price'),
            min_delivery_time_val=Min('details__delivery_time_in_days'),
        )

    @staticmethod
    def apply_filters(queryset, params):
        """Applies custom filter parameters."""
        creator_id = params.get('creator_id')
        min_price = params.get('min_price')
        max_delivery_time = params.get('max_delivery_time')
        if creator_id:
            queryset = queryset.filter(user_id=creator_id)
        if min_price:
            queryset = queryset.filter(min_price_val__gte=min_price)
        if max_delivery_time:
            queryset = queryset.filter(min_delivery_time_val__lte=max_delivery_time)
        return queryset