from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status

from common.constants import JSON_FORMAT, DATA
from common.test_features.user_data_generator import generate_random_client_with_token
from university.models import Department
from university.serializers.department_serializers import DepartmentProgrammeSerializer, DepartmentReadSerializer
from university.urls import DEPARTMENTS


class GetAllDepartmentsTest(TestCase):
    """ Test module for GET all Departments API """

    def setUp(self):
        self.departments = mommy.make('Department')
        self.url = reverse(DEPARTMENTS)
        self.client = generate_random_client_with_token()

    def test_get_departments(self):
        response = self.client.get(self.url, format=JSON_FORMAT)
        departments = Department.objects.all()
        serializer = DepartmentReadSerializer(departments, many=True)
        self.assertEqual(response.data[DATA], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_faculties(self):
        name = Department.objects.first().name
        querystring = '?filter={"name": "%s"}' % name
        response = self.client.get('{}{}'.format(self.url, querystring), format=JSON_FORMAT)
        filtered_faculties = Department.objects.filter(name__icontains=name)
        serializer = DepartmentReadSerializer(filtered_faculties, many=True)
        self.assertEqual(response.data[DATA], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RetrieveDepartmentTest(TestCase):
    """ Test module retrieve Department API """

    def setUp(self):
        self.department = mommy.make('Department')
        self.url = reverse(DEPARTMENTS, kwargs={'pk': self.department.pk})
        self.client = generate_random_client_with_token()

    def test_retrieve_department(self):
        response = self.client.get(self.url, format=JSON_FORMAT)
        department = Department.objects.get(pk=self.department.pk)
        serializer = DepartmentProgrammeSerializer(department)
        self.assertEqual(response.data[DATA], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_invalid_department(self):
        response = self.client.get(self.url, format=JSON_FORMAT)
        department = Department.objects.get(pk=self.department.pk)
        serializer = DepartmentProgrammeSerializer(department)
        self.assertEqual(response.data[DATA], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewDepartmentTest(TestCase):
    """ Test module for inserting a new Department """

    def setUp(self):
        self.faculty = mommy.make('Faculty')
        self.faker = Faker()
        self.code = self.faker.pystr(max_chars=20)
        self.name = self.faker.name()
        self.valid_data = {'code': self.code, 'name': self.name, 'faculty_id': self.faculty.id}
        self.invalid_data = {'code': '', 'name': self.name, 'faculty_id': self.faculty.id}
        self.url = reverse(DEPARTMENTS)
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


class UpdateDepartmentTest(TestCase):
    """ Test module for updating an existing Department record """

    def setUp(self):
        self.faker = Faker()
        self.department = mommy.make('Department')
        self.department2 = mommy.make('Department')
        self.valid_data = {'code': self.faker.pystr(max_chars=20), 'name': self.faker.name(), 'faculty_id': self.department.faculty_id}
        self.invalid_data = {'code': '', 'name': self.faker.name(), 'faculty_id': self.department.faculty_id}
        self.existing_data = {'code': self.department2.code, 'name': self.department2.name, 'faculty_id': self.department.faculty_id}
        self.url = reverse(DEPARTMENTS, kwargs={'pk': self.department.pk})
        self.client = generate_random_client_with_token()

    def test_update_valid_department(self):
        response = self.client.put(self.url, self.valid_data, format=JSON_FORMAT)
        self.assertLessEqual(self.valid_data.items(), response.data[DATA].items())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_department(self):
        response = self.client.put(self.url, self.invalid_data, format=JSON_FORMAT)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_department_unique(self):
        response = self.client.put(self.url, self.existing_data, format=JSON_FORMAT)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteDepartmentTest(TestCase):
    """ Test module for deleting an existing Department record """

    def setUp(self):
        self.department = mommy.make('Department')
        self.url = reverse(DEPARTMENTS, kwargs={'pk': self.department.pk})
        self.invalid_url = reverse(DEPARTMENTS, kwargs={'pk': 0})
        self.client = generate_random_client_with_token()

    def test_valid_delete_department(self):
        response = self.client.delete(self.url, format=JSON_FORMAT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
