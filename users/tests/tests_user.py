from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from organisations.models import Organisation

class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register_user')

    def test_register_user_success(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert response content
        self.assertIn('accessToken', response.data['data']) 
        self.assertIn('user', response.data['data'])
        self.assertEqual(response.data['data']['user']['firstName'], data['firstName'])
        self.assertEqual(response.data['data']['user']['lastName'], data['lastName'])
        self.assertEqual(response.data['data']['user']['phone'], data['phone'])

        # Check if user is created in the database
        user = User.objects.get(email=data['email'])
        self.assertEqual(user.firstName, data['firstName'])
        self.assertEqual(user.lastName, data['lastName'])
        self.assertEqual(user.phone, data['phone'])

    def test_register_user_missing_fields_first_name(self):
        data = {
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        self.assertIn('errors', response.data)
        self.assertEqual(len(response.data['errors']), 1)
        self.assertEqual(response.data['errors'][0]['field'], 'firstName')
        self.assertEqual(response.data['errors'][0]['message'], 'This field is required.')

    def test_register_user_missing_fields_last_name(self):
        data = {
            'firstName': 'John',
            'email': 'john.doe@example.com',
            'password': 'securepassword',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        self.assertIn('errors', response.data)
        self.assertEqual(len(response.data['errors']), 1)
        self.assertEqual(response.data['errors'][0]['field'], 'lastName')
        self.assertEqual(response.data['errors'][0]['message'], 'This field is required.')

    def test_register_user_missing_fields_email(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'password': 'securepassword',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        self.assertIn('errors', response.data)
        self.assertEqual(len(response.data['errors']), 1)
        self.assertEqual(response.data['errors'][0]['field'], 'email')
        self.assertEqual(response.data['errors'][0]['message'], 'This field is required.')

    def test_register_user_missing_fields_password(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        self.assertIn('errors', response.data)
        self.assertEqual(len(response.data['errors']), 1)
        self.assertEqual(response.data['errors'][0]['field'], 'password')
        self.assertEqual(response.data['errors'][0]['message'], 'This field is required.')

    def test_register_user_duplicate_email(self):
        initial_data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword',
            'phone': '1234567890'
        }
        
        # Register the initial user
        response = self.client.post(self.register_url, initial_data, format='json')
        
        # Assert the initial registration is successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        duplicate_data = {
            'firstName': 'Jane',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',  # Same email as initial user
            'password': 'anotherpassword',
            'phone': '9876543210'
        }
        
        # Try to register with duplicate email
        response_duplicate = self.client.post(self.register_url, duplicate_data, format='json')        
        self.assertEqual(response_duplicate.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        # Assert the response contains 'errors' key
        self.assertIn('errors', response_duplicate.data)
        
        # Assert specific error message for duplicate email
        self.assertEqual(len(response_duplicate.data['errors']), 1)
        self.assertEqual(response_duplicate.data['errors'][0]['field'], 'email')
        self.assertEqual(response_duplicate.data['errors'][0]['message'], 'user with this email already exists.')

    def test_register_user_default_organisation_name(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(email=data['email'])
        organisation = user.organisations.first()
        self.assertEqual(organisation.name, f"{data['firstName']}'s Organisation")

    def tearDown(self):
        User.objects.all().delete()
        Organisation.objects.all().delete()
        
        
class UserLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register_user')
        self.login_url = reverse('login_user')

        # Create a user for testing
        self.user_data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword',
            'phone': '1234567890'
        }
        self.client.post(self.register_url, self.user_data, format='json')

    def test_login_success(self):
        # Provide valid credentials
        login_data = {
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')

        # Assert the login is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])
        self.assertIn('user', response.data['data'])
        self.assertEqual(response.data['data']['user']['firstName'], self.user_data['firstName'])
        self.assertEqual(response.data['data']['user']['lastName'], self.user_data['lastName'])
        self.assertEqual(response.data['data']['user']['phone'], self.user_data['phone'])

    def test_login_invalid_credentials(self):
        # Provide invalid credentials
        invalid_login_data = {
            'email': 'john.doe@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, invalid_login_data, format='json')

        # Assert the login fails with 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def tearDown(self):
        User.objects.all().delete()
        
        
class UserDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            firstName='John',
            lastName='Doe',
            email='john.doe@example.com',
            password='securepassword',
            phone='1234567890'
        )
        self.user2 = User.objects.create_user(
            firstName='Jane',
            lastName='Doe',
            email='jane.doe@example.com',
            password='anotherpassword',
            phone='9876543210'
        )
        self.detail_url = reverse('user_detail', args=[self.user.userId])

    def test_view_own_details(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_other_user_details(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        User.objects.all().delete()
        

class OrganisationListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            firstName='John',
            lastName='Doe',
            email='john.doe@example.com',
            password='securepassword',
            phone='1234567890'
        )
        self.org1 = Organisation.objects.create(name="Org 1")
        self.org2 = Organisation.objects.create(name="Org 2")
        self.org1.users.add(self.user)
        self.list_url = reverse('organisation_list')

    def test_list_organisations(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['organisations']), 1)  

    def tearDown(self):
        User.objects.all().delete()
        Organisation.objects.all().delete()


class OrganisationDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            firstName='John',
            lastName='Doe',
            email='john.doe@example.com',
            password='securepassword',
            phone='1234567890'
        )
        self.user2 = User.objects.create_user(
            firstName='Jane',
            lastName='Doe',
            email='jane.doe@example.com',
            password='anotherpassword',
            phone='9876543210'
        )
        self.org = Organisation.objects.create(name="Org 1")
        self.org.users.add(self.user)
        self.detail_url = reverse('organisation_detail', args=[self.org.orgId])

    def test_view_own_organisation_details(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_other_organisation_details(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        User.objects.all().delete()
        Organisation.objects.all().delete()