from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Role(models.TextChoices):
    ADMIN = "ADMIN", _("Admin")
    USER = "USER", _("User")


class CustomUser(AbstractBaseUser, BaseUserManager):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    def __str__(self):
        return self.email


class CustomerUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **other_fields):
        if not email:
            raise ValueError("The Email field must be set")

        if not last_name or not first_name:
            raise ValueError("The First Name field must be set")

        email = self.normalize_email(email)
        user = self.model(
            email=email, last_name=last_name, first_name=first_name, **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)


def create_superuser(self, email, first_name, last_name, password=None):
    user = self.create_user(email, first_name, last_name, password)
    user.is_admin = True
    user.save(using=self._db)
    return user


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.name
