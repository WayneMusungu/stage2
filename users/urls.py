# urls.py

from django.urls import path
from .views import (
    OrganisationCreateView,
    OrganisationDetailView,
    OrganisationListView,
    OrganisationUserAddView,
    UserRegistrationView,
    UserLoginView,
    UserDetailView,
)

urlpatterns = [
    path('auth/register', UserRegistrationView.as_view(),name='register_user'),
    path('auth/login', UserLoginView.as_view(),name='login_user'),
    path('api/users/<int:id>', UserDetailView.as_view(), name='user_detail'),
    path('api/organisations', OrganisationListView.as_view(), name='organisation_list'),
    path('api/organisations/<int:id>', OrganisationDetailView.as_view(), name='organisation_detail'),
    path('api/organisation', OrganisationCreateView.as_view(), name='create_organisation'),
    path('organisations/<int:id>/users/', OrganisationUserAddView.as_view(), name='add_user_to_organisation'),

]
