# users/serializers.py

from rest_framework import serializers

from organisations.models import UserOrganisation
from organisations.serializers import OrganisationSerializer
from .models import User
from django.contrib.auth.hashers import make_password



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userId', 'firstName', 'lastName','phone')
        
class RegistrationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20, allow_blank=False)  # Require phone number

    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'email', 'password', 'phone')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_phone(self, value):
        if not value.strip():  # Ensure phone number is not blank or just whitespace
            raise serializers.ValidationError("Phone number cannot be blank")
        return value
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))  # Ensure password is hashed
        return super().create(validated_data)
    
    
class UserOrganisationSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer()

    class Meta:
        model = UserOrganisation
        fields = ('organisation',)

    def to_representation(self, instance):
        return OrganisationSerializer(instance.organisation).data