# users/views.py
from django.contrib.auth import authenticate

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, RegistrationSerializer
from organisations.models import Organisation, UserOrganisation
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
            organisation.save()

            # Link user to organisation
            UserOrganisation.objects.create(user=user, organisation=organisation)

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
        return Response({
            'status': 'Bad request',
            'message': 'Registration unsuccessful',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Debug prints to check input data
        print(f"Email: {email}")
        print(f"Password: {password}")

        user = authenticate(request, email=email, password=password)
        print(user)  # Debug print statement

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

            # Check if the requesting user is either the user themselves or belongs to the same organization
            if user == request.user or UserOrganisation.objects.filter(user=request.user, organisation__in=user.userorganisation_set.values_list('organisation', flat=True)).exists():
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
            
            

class OrganisationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_organisations = UserOrganisation.objects.filter(user=request.user)
            organisations = Organisation.objects.filter(orgId__in=user_organisations.values_list('organisation_id', flat=True))
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
                

class OrganisationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            organisation = Organisation.objects.get(orgId=id)
            user_org = UserOrganisation.objects.filter(user=request.user, organisation=organisation).first()
            if user_org:
                serializer = OrganisationDetailSerializer(organisation)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Organisation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)     
        
        
class OrganisationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrganisationCreateSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
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
        
        
class OrganisationAddUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        data = request.data
        userId = data.get('userId', None)
        
        if not userId:
            return Response({
                'status': 'Bad Request',
                'message': 'userId field is required in the request body',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        organisation = get_object_or_404(Organisation, orgId=id)
        user = get_object_or_404(User, userId=userId)
        
        # Check if the requesting user has permission to add users to this organisation
        # if not request.user.userorganisation_set.filter(organisation=organisation).exists():
        #     return Response({
        #         'status': 'Unauthorized',
        #         'message': 'You do not have permission to add users to this organisation',
        #     }, status=status.HTTP_403_FORBIDDEN)
        
        # Check if the user is already added to the organisation
        if organisation.userorganisation_set.filter(user=user).exists():
            return Response({
                'status': 'Bad Request',
                'message': 'User is already added to this organisation',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Add user to organisation
        UserOrganisation.objects.create(user=user, organisation=organisation)
        
        return Response({
            'status': 'success',
            'message': 'User added to organisation successfully',
        }, status=status.HTTP_200_OK)
                
# class UserDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, id):
#         try:
#             user = User.objects.get(userId=id)
            
#             # Check if the requesting user is authorized to view the user's details
#             if user == request.user or UserOrganisation.objects.filter(user=request.user, organisation__in=user.userorganisation_set.values_list('organisation', flat=True)).exists():
#                 serializer = UserSerializer(user)
                
#                 # Get organizations associated with the user
#                 user_organisations = UserOrganisation.objects.filter(user=user)
#                 org_serializer = UserOrganisationSerializer(user_organisations, many=True)
                
#                 return Response({
#                     'status': 'success',
#                     'message': 'User retrieved successfully',
#                     'data': {
#                         'user': serializer.data,
#                         'organisations': org_serializer.data
#                     }
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({
#                     'status': 'Unauthorized',
#                     'message': 'You do not have permission to access this user\'s data'
#                 }, status=status.HTTP_403_FORBIDDEN)
#         except User.DoesNotExist:
#             return Response({
#                 'status': 'Not found',
#                 'message': 'User not found'
#             }, status=status.HTTP_404_NOT_FOUND)


# class UserDetailsView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user

# class OrganisationListView(generics.ListCreateAPIView):
#     queryset = Organisation.objects.all()
#     serializer_class = OrganisationSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         # Automatically link creator to organisation
#         user = self.request.user
#         organisation = serializer.save()
#         UserOrganisation.objects.create(user=user, organisation=organisation)

# class OrganisationDetailView(generics.RetrieveAPIView):
#     queryset = Organisation.objects.all()
#     serializer_class = OrganisationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return user.organisation_set.all()
