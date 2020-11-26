from django.db import IntegrityError
from faker import Faker
from rest_framework.test import APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import User

faker = Faker()

# The client user credentials used for testing only
TEST_USER_EMAIL = 'admin@admin.com'
TEST_USER_PASSWORD = '12345678'


def generate_user(email, password):
    user = User.objects.create_user(email=email, password=password)
    return user


def generate_user_with_token(email, password, user=None):
    client = APIClient()
    user = user if user else generate_user(email, password)
    token = TokenObtainPairSerializer.get_token(user)
    client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token.access_token))
    return client


def generate_random_client_with_token():
    client = APIClient()
    try:
        user = User.objects.create_user(email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD)
    except IntegrityError:
        user = User.objects.get(email=TEST_USER_EMAIL)
    token = TokenObtainPairSerializer.get_token(user)
    client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token.access_token))
    return client
