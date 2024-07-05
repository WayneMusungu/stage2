# urls.py

from django.urls import path
from .views import (
    OrganisationAddUserView,
    OrganisationCreateView,
    OrganisationDetailView,
    OrganisationListView,
    UserRegistrationView,
    UserLoginView,
    UserDetailView,
    # OrganisationListView,
    # OrganisationDetailView,
)

urlpatterns = [
    path('auth/register', UserRegistrationView.as_view()),
    path('auth/login', UserLoginView.as_view()),
    path('api/users/<int:id>', UserDetailView.as_view()),
    path('api/organisations', OrganisationListView.as_view()),
    path('api/organisations/<int:id>', OrganisationDetailView.as_view()),
    path('api/organisation', OrganisationCreateView.as_view(), name='create_organisation'),
    path('organisations/<int:id>/users/', OrganisationAddUserView.as_view(), name='add_user_to_organisation'),

    # Add other endpoints here
]
