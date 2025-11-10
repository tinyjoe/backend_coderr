from rest_framework import serializers

def validate_details(self, value):
        """
        Validates that the details field is a list containing exactly 3 OfferDetail objects.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError('Details need to be a list of OfferDetail objects.')
        if len(value) != 3:
            raise serializers.ValidationError('An offer must contain exactly 3 details.')
        return value

def update_offer_detail(self, details_data, existing_details, serializer):
        """
        Updates existing OfferDetail instances based on the provided offer type and detail data.
        """
        for detail_data in details_data:
            offer_type = detail_data.get('offer_type', None)
            if not offer_type:
                 raise serializers.ValidationError('Um das Angebotsdetail zu aktualisieren, ist der Angebotstyp erforderlich.')
            if offer_type and offer_type in existing_details:
                detail_instance = existing_details.pop(offer_type)
                serializer.update(detail_instance, detail_data)