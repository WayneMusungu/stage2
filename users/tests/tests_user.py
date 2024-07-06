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
        
        # Assert the status code is 422 UNPROCESSABLE ENTITY
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