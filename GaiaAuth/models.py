import secrets

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# create a user model without username field, using email as the unique identifier
class User(AbstractBaseUser):
    first_name = models.CharField("First name", max_length=30, blank=True)
    last_name = models.CharField("Last name", max_length=30, blank=True)
    email = models.EmailField("Email address", max_length=255, unique=True)
    is_staff = models.BooleanField(
        "Staff status", default=False, help_text="Designates whether the user can log into this admin site."
    )
    is_active = models.BooleanField(
        "Active",
        default=True,
        help_text="Designates whether this user should be treated as "
        "active.  Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField("Date joined", default=timezone.now)

    is_verified = models.BooleanField(
        "Verified",
        default=False,
        help_text="Designates whether this user has completed the email verification process to allow login.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


class PendingActivation(models.Model):
    def generate_token(*args):
        return secrets.token_urlsafe(32)

    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255, unique=True, default=generate_token)

    def __str__(self):
        return f"{self.user.email} - {self.token}"

    def is_expired(self):
        return (timezone.now() - self.created_at).days > settings.CONFIRMATION_EMAIL_EXPIRY_DAYS


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255, unique=True, default=PendingActivation.generate_token)

    def __str__(self):
        return f"{self.user.email} - {self.token}"

    def is_expired(self):
        return (timezone.now() - self.created_at).days > settings.PASSWORD_RESET_EXPIRY_DAYS
