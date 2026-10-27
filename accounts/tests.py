from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from shop.models import Order

class AuthAndProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_profile_created_automatically(self):
        """Test that our signal creates a Profile when a User is created."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.user.username, 'testuser')

    def test_profile_requires_login(self):
        """Test that an anonymous user is redirected from the profile page."""
        response = self.client.get(reverse('profile'))
        # Should redirect to login page with ?next=/accounts/profile/
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_profile_accessible_when_logged_in(self):
        """Test that a logged-in user can access their profile."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_login_flow(self):
        """Test that a user can log in successfully."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        # Django LoginView redirects to LOGIN_REDIRECT_URL ('/') on success
        self.assertRedirects(response, '/')

    def test_registration_form(self):
        """Test that a new user can register."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpassword123!',
            'password2': 'complexpassword123!'
        })
        self.assertEqual(response.status_code, 302) # Redirects to login
        self.assertTrue(User.objects.filter(username='newuser').exists())