from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from .models import User, PendingActivation, PasswordReset


def send_activation_email(user: User):
    """
    Generate an activation token for the given user and send an email to the user with the activation link.

    @param user: The user to send the activation email to
    @return: None
    """
    if user.is_active or not settings.CONFIRMATION_EMAIL_ENABLED:
        return
    activation = PendingActivation.objects.create(user=user)
    token = activation.token
    path = reverse("activate", kwargs={"token": token})
    url = f"{settings.BASE_URL}{path}"

    # send email to the user
    subject = "Activate your account on Gaia"
    html_message = render_to_string("activate_email.html", {"user": user, "url": url})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def use_activation_token(token: str) -> bool:
    """
    Verify the given token and if valid, activate the account of the corresponding user.

    @param token: The token to verify
    @return: True if the token is valid and the user is activated, False otherwise
    """
    try:
        activation = PendingActivation.objects.get(token=token)
        if activation.is_expired():
            return False
        user = activation.user
        user.is_active = True
        user.is_verified = True
        user.save()
        activation.delete()
        return True
    except PendingActivation.DoesNotExist:
        return False


def send_password_reset_email(user: User):
    """
    Generate a password reset token for the given user and send an email to the user with the password reset link.

    @param user: The user to send the password reset email to
    @return: None
    """
    user.set_unusable_password()  # invalidate the current password
    reset = PasswordReset.objects.create(user=user)
    token = reset.token
    url = f"{settings.BASE_URL}/password-reset/{token}"

    # send email to the user
    subject = "Reset your password on Gaia"
    html_message = render_to_string("password_reset_email.html", {"user": user, "url": url})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def use_password_reset_token(token: str, new_password: str) -> bool:
    """
    Verify the given token and if valid, activate the account of the corresponding user.

    @param token: The token to verify
    @throw: ValueError if the password used is invalid
    @return: True if the token is valid and the user is activated, False otherwise
    """
    from .serializers import UserSerializer

    try:
        reset = PasswordReset.objects.get(token=token)
        if reset.is_expired():
            return False
        user = reset.user

        serializer = UserSerializer(instance=user, data={"password": new_password}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        reset.delete()
        return True
    except PasswordReset.DoesNotExist:
        return False
