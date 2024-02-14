# Generate tests for login and registration
from datetime import timedelta

from django.core import mail
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from .models import User, PendingActivation, PasswordReset

DEFAULT_CREDENTIALS = {"email": "test@email.com", "password": "testpassword"}
override_settings(CONFIRMATION_EMAIL_ENABLED=True)


class AuthAPITestCase(APITestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.credentials = DEFAULT_CREDENTIALS

    def login(self):
        self.client.login(**self.credentials)

    def is_logged(self):
        response = self.client.get(reverse("me"))
        return response.status_code == status.HTTP_200_OK


class MeTests(AuthAPITestCase):
    def setUp(self):
        User.objects.create_user(**self.credentials)

    def test_me(self):
        self.login()
        url = reverse("me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.credentials["email"])

    def test_me_unauthorized(self):
        url = reverse("me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LoginTests(AuthAPITestCase):
    def setUp(self):
        User.objects.create_user(**self.credentials)

    def test_login(self):
        url = reverse("login")
        response = self.client.post(url, self.credentials, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.credentials["email"])
        self.assertTrue(self.is_logged())

    def test_login_invalid(self):
        url = reverse("login")
        response = self.client.post(url, {"email": "invalid", "password": "invalid"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["non_field_errors"][0], "Invalid credentials")
        self.assertFalse(self.is_logged())

    def test_logout(self):
        self.client.login(**self.credentials)
        self.assertTrue(self.is_logged())

        url = reverse("logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Logged out successfully")
        self.assertFalse(self.is_logged())


class RegisterTests(AuthAPITestCase):
    def setUp(self):
        self.url = reverse("register")

    @override_settings(CONFIRMATION_EMAIL_ENABLED=False)
    def test_register_success(self):
        response = self.client.post(self.url, self.credentials, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], self.credentials["email"])
        self.assertFalse(self.is_logged())

        self.login()

        self.assertTrue(self.is_logged())
        self.assertEqual(User.objects.count(), 1)

    @override_settings(CONFIRMATION_EMAIL_ENABLED=False)
    def test_register_invalid_email(self):
        response = self.client.post(self.url, {"email": "invalid", "password": "testpassword"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["email"][0], "Enter a valid email address.")
        self.login()
        self.assertFalse(self.is_logged())
        self.assertEqual(User.objects.count(), 0)

    @override_settings(CONFIRMATION_EMAIL_ENABLED=False)
    def test_register_password_empty(self):
        response = self.client.post(self.url, {"email": "test@email.com", "password": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["password"][0], "This field may not be blank.")
        self.login()
        self.assertFalse(self.is_logged())
        self.assertEqual(User.objects.count(), 0)

    @override_settings(CONFIRMATION_EMAIL_ENABLED=False)
    def test_register_password_too_short(self):
        response = self.client.post(self.url, {"email": "test@email.com", "password": "short"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["password"][0], "This password is too short. It must contain at least 8 characters."
        )

    @override_settings(CONFIRMATION_EMAIL_ENABLED=True)
    def test_register_confirmation_email_enabled(self):
        response = self.client.post(self.url, self.credentials, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], self.credentials["email"])
        self.assertFalse(self.is_logged())
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertFalse(user.is_active)
        self.login()
        self.assertFalse(self.is_logged())


@override_settings(CONFIRMATION_EMAIL_ENABLED=True)
class ActivationTests(AuthAPITestCase):
    def create_user(self):
        url = reverse("register")
        self.client.post(url, self.credentials, format="json")

    def test_email_sent(self):
        self.create_user()
        self.assertEqual(len(mail.outbox), 1)
        self.assertFalse(self.is_logged())
        user = User.objects.first()
        self.assertFalse(user.is_active)
        activation = PendingActivation.objects.filter(user=user).first()
        self.assertIsNotNone(activation)

    def test_email_confirmation(self):
        self.create_user()
        self.assertFalse(self.is_logged())  # should not be able to login without activation

        user = User.objects.first()
        activation = PendingActivation.objects.filter(user=user).first()
        url = reverse("activate", kwargs={"token": activation.token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.login()
        self.assertTrue(self.is_logged())

        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertIsNone(PendingActivation.objects.filter(user=user).first())


class PasswordResetTests(AuthAPITestCase):
    def setUp(self):
        self.user = User.objects.create_user(**self.credentials)
        self.old_password = self.credentials["password"]
        self.new_password = "superhardpassword420"

    def test_ask_password_reset_success(self):
        url = reverse("password-reset-ask")
        response = self.client.post(url, {"email": self.credentials["email"]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

    def test_ask_password_reset_invalid_email(self):
        url = reverse("password-reset-ask")
        response = self.client.post(url, {"email": "invalid"}, format="json")

        # The request is still successful to avoid email enumeration, but no email is actually sent
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_success(self):
        url = reverse("password-reset-ask")
        response = self.client.post(url, {"email": self.credentials["email"]}, format="json")
        self.assertEqual(len(mail.outbox), 1)

        user = User.objects.first()
        reset = PasswordReset.objects.filter(user=user).first()
        self.assertIsNotNone(reset)

        url = reverse("password-reset", kwargs={"token": reset.token})
        response = self.client.post(url, {"password": self.new_password}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertFalse(user.check_password(self.old_password))
        self.assertTrue(user.check_password(self.new_password))
        self.assertIsNone(PasswordReset.objects.filter(user=user).first())


@override_settings(BASE_URL="http://testserver")
class ActivationEmailServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@email.com", password="testpassword", is_active=False)

    def test_send_activation_email(self):
        from GaiaAuth.service import send_activation_email

        send_activation_email(self.user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Activate your account on Gaia")
        self.assertIn("http://testserver/auth/activate/", mail.outbox[0].body)
        activation = PendingActivation.objects.filter(user=self.user).first()
        self.assertIsNotNone(activation)
        self.assertIn(activation.token, mail.outbox[0].body)

    def test_send_activation_email_disabled(self):
        from GaiaAuth.service import send_activation_email

        with override_settings(CONFIRMATION_EMAIL_ENABLED=False):
            send_activation_email(self.user)
            self.assertEqual(len(mail.outbox), 0)
            self.assertIsNone(PendingActivation.objects.filter(user=self.user).first())

    def test_send_activation_email_active_user(self):
        from GaiaAuth.service import send_activation_email

        active_user = User.objects.create_user(email="other@email.com", password="testpassword", is_active=True)
        send_activation_email(active_user)
        self.assertEqual(len(mail.outbox), 0)

    def test_use_activation_token(self):
        from GaiaAuth.service import use_activation_token

        activation = PendingActivation.objects.create(user=self.user)
        token = activation.token
        self.assertTrue(use_activation_token(token))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertIsNone(PendingActivation.objects.filter(user=self.user).first())

    @override_settings(CONFIRMATION_EMAIL_EXPIRY_DAYS=1)
    def test_use_activation_token_expired(self):
        from GaiaAuth.service import use_activation_token

        activation = PendingActivation.objects.create(user=self.user)
        activation.created_at = activation.created_at - timedelta(days=2)
        activation.save()
        self.assertTrue(activation.is_expired())
        token = activation.token
        self.assertFalse(use_activation_token(token))
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertIsNotNone(PendingActivation.objects.filter(user=self.user).first())

    def test_use_activation_token_invalid(self):
        from GaiaAuth.service import use_activation_token

        self.assertFalse(use_activation_token("invalidtoken"))


@override_settings(BASE_URL="http://testserver")
class PasswordResetServiceTests(TestCase):
    def setUp(self):
        self.old_password = "testpassword"
        self.new_password = "validpass420"
        self.user = User.objects.create_user(email="test@email.com", password=self.old_password, is_active=False)

    def test_send_password_reset_email(self):
        from GaiaAuth.service import send_password_reset_email

        send_password_reset_email(self.user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("http://testserver/password-reset/", mail.outbox[0].body)
        self.assertFalse(self.user.check_password(self.old_password))
        reset = PasswordReset.objects.filter(user=self.user).first()
        self.assertIsNotNone(reset)
        self.assertIn(reset.token, mail.outbox[0].body)

    def test_use_password_reset_token(self):
        from GaiaAuth.service import use_password_reset_token

        reset = PasswordReset.objects.create(user=self.user)
        token = reset.token
        self.assertTrue(use_password_reset_token(token, self.new_password))
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(self.old_password))
        self.assertTrue(self.user.check_password(self.new_password))
        self.assertIsNone(PasswordReset.objects.filter(user=self.user).first())

    @override_settings(PASSWORD_RESET_EXPIRY_DAYS=1)
    def test_use_password_reset_token_expired(self):
        from GaiaAuth.service import use_password_reset_token

        reset = PasswordReset.objects.create(user=self.user)
        reset.created_at = reset.created_at - timedelta(days=2)
        reset.save()
        self.assertTrue(reset.is_expired())
        token = reset.token
        self.assertFalse(use_password_reset_token(token, self.new_password))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.old_password))
        self.assertFalse(self.user.check_password(self.new_password))
        self.assertIsNotNone(PasswordReset.objects.filter(user=self.user).first())

    def test_use_password_reset_token_invalid(self):
        from GaiaAuth.service import use_password_reset_token

        self.assertFalse(use_password_reset_token("invalidtoken", self.new_password))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.old_password))
        self.assertFalse(self.user.check_password(self.new_password))
        self.assertIsNone(PasswordReset.objects.filter(user=self.user).first())

    def test_use_password_reset_token_invalid_password(self):
        from GaiaAuth.service import use_password_reset_token

        reset = PasswordReset.objects.create(user=self.user)
        token = reset.token
        self.assertRaises(ValidationError, use_password_reset_token, token, "")
