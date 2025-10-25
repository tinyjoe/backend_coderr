from rest_framework.pagination import PageNumberPagination

class OfferPagination(PageNumberPagination):
    page_size = 10  # Standardwert
    page_size_query_param = "page_size"  # erlaubt ?page_size=20
    max_page_size = 100