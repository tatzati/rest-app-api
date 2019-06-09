from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""
        email = 'test@mail.com'
        password = 'test2019'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized."""
        email = 'test@MAIL.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='test123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_with_invalid_email(self):
        """Test creating user with no email address raises Error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')

    def test_new_superuser(self):
        """Test creating new superuser"""
        superuser = get_user_model().objects.create_superuser(
            'mail@mail.com',
            'test2019'
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
