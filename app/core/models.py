from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CoreModel(models.Model):
    class Meta:
        app_label = 'core'
        abstract = True

    deleted = models.BooleanField(default=False)


class UserManager(BaseUserManager):
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must provide an email address!')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a super user"""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, CoreModel, PermissionsMixin):
    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    plan = models.ForeignKey('Plan', on_delete=models.CASCADE, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name


class Plan(CoreModel):
    class Meta:
        db_table = 'plan'
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'

    """A Plan has a name and groups several ​Workout​ items."""
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Workout(CoreModel):
    class Meta:
        db_table = 'workout'
        verbose_name = 'Workout'
        verbose_name_plural = 'Workouts'

    """A ​Workout​ can have multiple ​Activity​ items that your a ​User​ will perform that day."""
    name = models.CharField(max_length=255, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Activity(CoreModel):
    class Meta:
        db_table = 'activity'
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    """​Activity​ items that your ​User​ will perform that day."""
    name = models.CharField(max_length=255, blank=True, null=True)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
