from rest_framework.relations import StringRelatedField
from six import text_type

from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User
from core.models import Plan


class CustomTokenObtainSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        return super(CustomTokenObtainSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        return super(CustomTokenObtainSerializer, self).create(validated_data)

    email_or_username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super(CustomTokenObtainSerializer, self).__init__(*args, **kwargs)

        self.fields[self.email_or_username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        self.user = None
        attempting_user = User.objects.filter(
            Q(email=attrs[self.email_or_username_field])).first()
        if attempting_user and attempting_user.check_password(attrs['password']):
            self.user = attempting_user
        if attempting_user and not attempting_user.check_password(attrs['password']):
            raise AuthenticationFailed()
        if not attempting_user:
            raise AuthenticationFailed(detail='User does not exist!')
        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplemented('Must implement `get_token` method for `TokenObtainSerializer` subclasses')


class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    """
    Serializer used to return a token when user is successfully authenticated.
    """

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)
        data['token'] = {'refresh': text_type(refresh), 'access': text_type(refresh.access_token)}
        return data


class PlanReadSerializer(ModelSerializer):
    workout = StringRelatedField(read_only=True)
    user = StringRelatedField(read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'name', 'workout', 'user']
        extra_kwargs = {'id': {'read_only': True}}


class PlanWriteSerializer(ModelSerializer):
    workout_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Plan
        fields = ['id', 'name', 'workout_id', 'user_id']
        extra_kwargs = {'id': {'read_only': True}}
