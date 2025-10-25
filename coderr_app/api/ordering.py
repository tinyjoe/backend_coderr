class OfferOrderingHelper:
    """
    Encapsulates custom sorting logic for Offers.
    """
    ORDERING_MAP = {
        'min_price': 'min_price_val',
        '-min_price': '-min_price_val',
        'updated_at': 'updated_at',
        '-updated_at': '-updated_at',
    }

    @classmethod
    def apply_ordering(cls, queryset, ordering_param):
        """Applies sorting based on a query parameter."""
        if not ordering_param:
            return queryset.order_by('-updated_at')
        ordering_field = cls.ORDERING_MAP.get(ordering_param)
        if ordering_field:
            return queryset.order_by(ordering_field)
        return queryset.order_by('-updated_at')