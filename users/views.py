from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer, RegistrationSerializer
from organisations.models import Organisation
from rest_framework_simplejwt.tokens import RefreshToken
from organisations.serializers import OrganisationCreateSerializer, OrganisationDetailSerializer, OrganisationSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Create default organisation
            org_name = f"{user.firstName}'s Organisation"
            organisation = Organisation.objects.create(name=org_name)
            organisation.users.add(user)
            organisation.save()

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Registration successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
            }, status=status.HTTP_201_CREATED)
        
        # Handle validation errors (422 status code)
        if serializer.errors:
            errors = []
            for field, messages in serializer.errors.items():
                for message in messages:
                    errors.append({
                        'field': field,
                        'message': message
                    })
            return Response({
                'errors': errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        # If serializer is not valid and no specific error is caught, return 400 Bad Request
        return Response({
            'status': 'Bad request',
            'message': 'Registration unsuccessful',
        }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # try:
        #     user = User.objects.get(email=email)
        # except User.DoesNotExist:
        #     return Response({
        #         'status': 'Bad request',
        #         'message': 'User is not registered'
        #     }, status=status.HTTP_401_UNAUTHORIZED)


        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'Bad request',
            'message': 'Authentication failed',
        }, status=status.HTTP_401_UNAUTHORIZED)
    
        
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            user = User.objects.get(userId=id)

            if user == request.user:
                serializer = UserSerializer(user)
                return Response({
                    'status': 'success',
                    'message': 'User retrieved successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'You are not authorized to view this user\'s data'
                }, status=status.HTTP_403_FORBIDDEN)

        except User.DoesNotExist:
            return Response({
                'status': 'Not found',
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
            
class OrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch organisations related to the logged-in user
            organisations = request.user.organisations.all()
            serializer = OrganisationSerializer(organisations, many=True)
            return Response({
                'status': 'success',
                'message': 'Organisations retrieved successfully',
                'data': {
                    'organisations': serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Failed to retrieve organisations',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = OrganisationCreateSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()

            # Automatically add the requesting user to the new organisation
            organisation.users.add(request.user)

            return Response({
                'status': 'success',
                'message': 'Organisation created successfully',
                'data': {
                    'orgId': organisation.orgId,
                    'name': organisation.name,
                    'description': organisation.description,
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad Request',
            'message': 'Client error',
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
                

class OrganisationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            organisation = Organisation.objects.get(orgId=id)
            
            # Check if the requesting user belongs to the organisation
            if request.user in organisation.users.all():
                serializer = OrganisationDetailSerializer(organisation)
                return Response({
                    'status': 'success',
                    'message': 'Organisation retrieved successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'Forbidden',
                    'message': 'You do not have permission to view this organisation'
                }, status=status.HTTP_403_FORBIDDEN)
                
        except Organisation.DoesNotExist:
            return Response({
                'status': 'Not Found',
                'message': 'Organisation not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
            
class OrganisationUserAddView(APIView):
    def post(self, request, id):
        try:
            organisation = Organisation.objects.get(orgId=id)

            # Extract userId from request data
            userId = request.data.get('userId')
            
            if not userId:
                return Response({
                    'status': 'Bad Request',
                    'message': 'userId is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check if the userId exists
            user = User.objects.get(userId=userId)

            # Add user to the organisation
            organisation.users.add(user)

            return Response({
                'status': 'success',
                'message': 'User added to organisation successfully',
            }, status=status.HTTP_200_OK)

        except Organisation.DoesNotExist:
            return Response({
                'status': 'Not found',
                'message': 'Organisation not found'
            }, status=status.HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({
                'status': 'Not found',
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Failed to add user to organisation',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)