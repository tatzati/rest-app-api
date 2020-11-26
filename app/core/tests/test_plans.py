from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from model_bakery import baker

from tests.test_tools import generate_random_client_with_token
from core.models import Plan
from core.serializers import PlanReadSerializer, PlanWriteSerializer
from core.urls import PLANS

JSON_FORMAT = 'json'
DATA = 'data'


class GetAllPlansTest(TestCase):
    """ Test module for GET all Plans API """
    def setUp(self):
        self.plan = baker.make('core.Plan')
        self.url = reverse(PLANS)
        self.client = generate_random_client_with_token()

    def test_get_plans(self):
        response = self.client.get(self.url, format=JSON_FORMAT)
        plan = Plan.objects.filter(deleted=False)
        serializer = PlanReadSerializer(plan, many=True)
        self.assertEqual(response.data[DATA], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewPlanTest(TestCase):
    """ Test module for inserting a new Plan """
    def setUp(self):
        self.faculty = mommy.make('Plan')
        self.faker = Faker()
        self.code = self.faker.pystr(max_chars=20)
        self.name = self.faker.name()
        self.valid_data = {'code': self.code, 'name': self.name, 'faculty_id': self.faculty.id}
        self.invalid_data = {'code': '', 'name': self.name, 'faculty_id': self.faculty.id}
        self.url = reverse(PLANS)
        self.client = generate_random_client_with_token()

    def test_create_department(self):
        response = self.client.post(self.url, self.valid_data, format=JSON_FORMAT)
        self.assertLessEqual(self.valid_data.items(), response.data[DATA].items())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.get(code=self.code).code, self.code)
        self.assertEqual(Department.objects.get(name=self.name).name, self.name)
        self.assertEqual(Department.objects.get(code=self.code).faculty_id, self.faculty.id)

    def test_create_department_unique(self):
        self.test_create_department()
        response = self.client.post(self.url, self.valid_data, format=JSON_FORMAT)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_department(self):
        response = self.client.post(self.url, {}, format=JSON_FORMAT)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
