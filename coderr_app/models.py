from django.db import models


OFFER_TYPE_CHOICES = [
    ('basic', 'Basic'),
    ('standard', 'Standard'),
    ('premium', 'Premium'),
]


ORDER_STATUS_CHOICES = [
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

class Offer(models.Model): 
    user = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.IntegerField(blank=True, null=True)
    min_delivery_time = models.IntegerField(blank=True, null=True)


class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default='basic')
  


class Order(models.Model): 
    customer_user = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='customer_orders')
    business_user = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='business_orders')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE_CHOICES)
    status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model): 
    business_user = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='business_reviews')
    reviewer = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    