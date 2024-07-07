from rest_framework import serializers
from organisations.models import Organisation

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('orgId', 'name', 'description')
        
        
class OrganisationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('orgId', 'name', 'description')
        
        
class OrganisationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('orgId', 'name', 'description')
        extra_kwargs = {
            'orgId': {'read_only': True},
            'name': {'required': True},
            'description': {'required': False, 'allow_blank': True},  # Allow description to be blank
        }

    def create(self, validated_data):
        return Organisation.objects.create(**validated_data)