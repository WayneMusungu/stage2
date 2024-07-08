from django.urls import path
from .views import (
    OrganisationView,
    OrganisationDetailView,
    OrganisationUserAddView,
    UserRegistrationView,
    UserLoginView,
    UserDetailView,
)

urlpatterns = [
    path('auth/register', UserRegistrationView.as_view(), name='register_user'),
    path('auth/login', UserLoginView.as_view(), name='login_user'),
    path('api/users/<uuid:id>', UserDetailView.as_view(), name='user_detail'),
    path('api/organisations', OrganisationView.as_view(), name='organisation_list_create'),
    path('api/organisations/<uuid:id>', OrganisationDetailView.as_view(), name='organisation_detail'),
    path('api/organisations/<uuid:id>/users', OrganisationUserAddView.as_view(), name='add_user_to_organisation'),
]
