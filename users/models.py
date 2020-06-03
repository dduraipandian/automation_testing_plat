from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


# Create your models here.

class UserProfileManager(BaseUserManager):
    """
    Custom manager for custom user profile
    """

    def create_user(self, email, name, password=None):
        """
        Creates new user profile for platform
        """

        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save()

        return user

    def create_staffuser(self, email, name, password=None):
        """
        Creates new user profile for platform
        """

        user = self.model(email=email, name=name)
        user.set_password(password)
        user.is_staff = True
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates new user profile for platform
        """

        user = self.model(email=email, name=name)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Represents the user profile for platform extending default Auth
    """

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('', '')
    )

    email = models.EmailField(unique=True, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserProfileManager()

    def get_name(self):
        """
        returns name of the user
        """

        return self.name

    def get_user_display_name(self):
        return self.get_name()

    def __str__(self):
        """
        string conversion for the object
        """

        return self.get_user_display_name()
