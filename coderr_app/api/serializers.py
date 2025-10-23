from rest_framework import serializers
from coderr_app.models import Offer, OfferDetail

class OfferDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailCreateSerializer(many=True)
    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

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
    

class NestedOfferDetailSerializer(serializers.HyperlinkedRelatedField):
    url = serializers.HyperlinkedIdentityField(view_name='offerdetail-detail', lookup_field='pk')
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class SingleOfferDetailSerializer(serializers.ModelSerializer):
    details = NestedOfferDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Offer 
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', ]