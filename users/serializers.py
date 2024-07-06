# users/serializers.py

from rest_framework import serializers

# from organisations.models import UserOrganisation
from organisations.serializers import OrganisationSerializer
from .models import User
from django.contrib.auth.hashers import make_password



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userId', 'firstName', 'lastName','phone')
        
class RegistrationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20, allow_blank=False)  # Require phone number
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'email', 'password', 'phone')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        return user
    
    
# class UserOrganisationSerializer(serializers.ModelSerializer):
#     organisation = OrganisationSerializer()

#     class Meta:
#         model = UserOrganisation
#         fields = ('organisation',)

#     def to_representation(self, instance):
#         return OrganisationSerializer(instance.organisation).data