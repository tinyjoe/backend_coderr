from urllib import request
from django.db import models
from rest_framework import serializers

from auth_app.models import CustomUser
from coderr_app.models import Offer, OfferDetail, Order, Review
from .services import update_offer_detail, validate_details


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class NestedOfferDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        
    def get_url(self, obj):
        return f"/offerdetails/{obj.pk}/"


class UserShortInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username"]


class OfferListSerializer(serializers.ModelSerializer):
    details = NestedOfferDetailSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserShortInfoSerializer(source="user", read_only=True)
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

    def get_min_price(self, obj):
        return obj.details.aggregate(models.Min('price'))['price__min']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min']
    

class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, required=False)
    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        extra_kwargs = {'offer_type': {'required': True}}

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        validate_details(self, details_data)
        user = self.context['request'].user
        custom_user = user.customuser
        offer = Offer.objects.create(user=custom_user, **validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if details_data is not None:
            existing_details = {detail.offer_type: detail for detail in instance.details.all()}
            update_offer_detail(self, details_data, existing_details, OfferDetailSerializer())
        return instance



class SingleOfferSerializer(serializers.ModelSerializer):
    details = NestedOfferDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Offer 
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', ]


class OrderListCreateSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)
    customer_user = serializers.IntegerField(source='customer_user.id', read_only=True)
    business_user = serializers.IntegerField(source='offer_detail.offer.user.id', read_only=True)
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time_in_days', read_only=True)
    price = serializers.IntegerField(source='offer_detail.price', read_only=True)
    features = serializers.ListField(source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'offer_detail_id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        customer_user = request.user.customuser
        offer_detail_id = validated_data.pop('offer_detail_id')
        try:
            offer_detail = OfferDetail.objects.get(pk=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError({'offer_detail_id': 'OfferDetail not found.'})
        order = Order.objects.create(offer_detail=offer_detail, customer_user=customer_user, status='in_progress')
        return order
    

class OrderDetailSerializer(serializers.ModelSerializer):
    customer_user = serializers.IntegerField(source='customer_user.id', read_only=True)
    business_user = serializers.IntegerField(source='offer_detail.offer.user.id', read_only=True)
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time_in_days', read_only=True)
    price = serializers.IntegerField(source='offer_detail.price', read_only=True)
    features = serializers.ListField(source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']


class InProgressOrderCountSerializer(serializers.Serializer):
    order_count = serializers.IntegerField()
    
    
class CompletedOrderCountSerializer(serializers.Serializer):
    completed_order_count = serializers.IntegerField()
    

class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=True)
    reviewer = serializers.IntegerField(source='reviewer.id', read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        reviewer = request.user.customuser
        business_user = validated_data['business_user']
        if business_user.type != 'business':
            raise serializers.ValidationError('Dieser User ist kein Business User.')
        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError('Sie haben diesen Business User bereits bewertet.')
        review = Review.objects.create(business_user=business_user, reviewer=reviewer, rating=validated_data['rating'], description=validated_data['description'])
        return review
    

class ReviewDetailSerializer(serializers.ModelSerializer):
    business_user = serializers.IntegerField(source='business_user.id', read_only=True)
    reviewer = serializers.IntegerField(source='reviewer.id', read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']


class BaseInfoSerializer(serializers.Serializer):
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()