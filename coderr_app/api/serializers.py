from django.db import models
from rest_framework import serializers

from auth_app.models import CustomUser
from coderr_app.models import Offer, OfferDetail



class NestedOfferDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(view_name='offerdetail-detail', lookup_field='pk', read_only=True)
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class UserShortSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username"]


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class OfferSerializer(serializers.ModelSerializer):
    details = NestedOfferDetailSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserShortSerializer(source="user", read_only=True)
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

    def get_min_price(self, obj):
        return obj.details.aggregate(models.Min('price'))['price__min']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min']

    def validate_details(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('Details need to be a list of OfferDetail objects.')
        if len(value) != 3:
            raise serializers.ValidationError('An offer must contain exactly 3 details.')
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user
        custom_user = user.customuser
        offer = Offer.objects.create(user=custom_user, **validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer


class SingleOfferDetailSerializer(serializers.ModelSerializer):
    details = NestedOfferDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Offer 
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', ]


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']