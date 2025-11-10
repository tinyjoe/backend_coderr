from django.db import models
from auth_app.models import CustomUser


"""
Predefined choices for offer types.
"""
OFFER_TYPE_CHOICES = [
    ('basic', 'Basic'),
    ('standard', 'Standard'),
    ('premium', 'Premium'),
]


"""
Predefined choices for order states.
"""
ORDER_STATUS_CHOICES = [
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class Offer(models.Model): 
    """
    Model representing an offer created by a business user.
    """
    user = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.IntegerField(blank=True, null=True)
    min_delivery_time = models.IntegerField(blank=True, null=True)


class OfferDetail(models.Model):
    """
    Model representing detailed information about an offer.
    """
    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default='basic')
  

class Order(models.Model): 
    """
    Model representing an order placed by a customer for an offer.
    """
    customer_user = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='customer_orders')
    business_user = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='business_orders', null=True)
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name='orders', null=True)
    status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model): 
    """
    Model representing a review given by a customer to a business user.
    """
    business_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='business_reviews')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['business_user', 'reviewer'], name='unique_review_per_business_user')
        ]

    