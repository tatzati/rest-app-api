from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.urls import reverse, resolve
from faker import Faker
from rest_framework.test import APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import User

faker = Faker()

# The client user credentials used for testing only
TEST_USER_USERNAME = 'test_user'
TEST_USER_EMAIL = 'admin@admin.com'
TEST_USER_PASSWORD = '12345678'


def load_predefined_component_permission_groups(group_name, reversed_url, user=None, permission_actions=None, university=None, faculty=None, department=None):
    # permission_actions must be in ['view', 'add', 'change', 'delete']
    generate_user_groups()
    group = Group.objects.get(name=group_name)
    if not user:
        generate_random_client_with_token()
    view = resolve(reversed_url)[0].cls
    model = view.queryset.model if view.queryset.model else None
    # if model:
    #     content_type = ContentType.objects.get_for_model(model)
    internal_name = view.internal_name if view.internal_name else None
    component_permission = create_component_permission(name=internal_name, view_only=False if model else True)
    u, f, g = generate_user_relations(user, group, university=university, faculty=faculty, department=department)
    create_guardian_object_permission_for_component(component_permission_object=component_permission, group=group, permission_actions=permission_actions)
    print('Generated')


def generate_user(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    return user


def generate_student(user):
    return mommy.make('Student', user=user)


def generate_user_with_token(username, email, password, user=None):
    client = APIClient()
    user = user if user else generate_user(username, email, password)
    token = TokenObtainPairSerializer.get_token(user)
    client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token.access_token))
    return client


def generate_random_client_with_token():
    client = APIClient()
    try:
        user = User.objects.create_user(username=TEST_USER_USERNAME, email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD)
    except IntegrityError:
        user = User.objects.get(username=TEST_USER_USERNAME, email=TEST_USER_EMAIL)
    token = TokenObtainPairSerializer.get_token(user)
    client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token.access_token))
    return client


def generate_user_type_with_token(user_type):
    client = APIClient()
    user = user_type.user
    token = TokenObtainPairSerializer.get_token(user)
    client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token.access_token))
    return client


def generate_user_relations(user, group, university=None, faculty=None, department=None):
    data = [None, None, None]
    if university:
        ug = UniversityGroup.objects.create(group=group, university=university)
        ug.users.add(user)
        university_groups = UniversityGroup.objects.filter(id=ug.id)
        data[0] = university_groups
    if faculty:
        fg = FacultyGroup.objects.create(group=group, faculty=faculty)
        fg.users.add(user)
        faculty_groups = FacultyGroup.objects.filter(id=fg.id)
        data[1] = faculty_groups
    if department:
        dg = DepartmentGroup.objects.create(group=group, department=department)
        dg.users.add(user)
        department_groups = DepartmentGroup.objects.filter(id=dg.id)
        data[2] = department_groups

    return tuple(data)


def generate_student_with_token(username, email, password):
    user = generate_user(username, email, password)
    student = generate_student(user)
    client = generate_user_type_with_token(student)
    return client


def create_component_permission(name, view_only=False):
    return ComponentPermission.objects.create(name=name, view_only=view_only)


def create_guardian_object_permission_for_component(component_permission_object, group, permission_actions):
    # ToDo - implement
    content_type_id = ContentType.objects.get_for_model(ComponentPermission).id
    for permission_action in permission_actions:
        permission = Permission.objects.filter(content_type_id=content_type_id, codename='{}_componentpermission'.format(permission_action)).first()
        GroupObjectPermission.objects.create(object_pk=component_permission_object.id, content_type_id=content_type_id, permission_id=permission.id, group=group)
