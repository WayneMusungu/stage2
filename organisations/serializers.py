from rest_framework import serializers
from organisations.models import Organisation, UserOrganisation

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('orgId', 'name', 'description')
        
        
class OrganisationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('orgId', 'name', 'description')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'status': 'success',
            'message': 'Organisation retrieved successfully',
            'data': data
        }
        
        
class OrganisationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('orgId', 'name', 'description')
        extra_kwargs = {
            'orgId': {'read_only': True},  # orgId will be generated automatically
            'name': {'required': True},
        }

    def create(self, validated_data):
        return Organisation.objects.create(**validated_data)