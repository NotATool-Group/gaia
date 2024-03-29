from django.conf import settings
from django.urls import path

from .views import RegisterView, LoginView, LogoutView, MeView, ActivateView, PasswordResetView, AskPasswordResetView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("password-reset/", AskPasswordResetView.as_view(), name="password-reset-ask"),
    path("password-reset/<str:token>/", PasswordResetView.as_view(), name="password-reset"),
]

if settings.CONFIRMATION_EMAIL_ENABLED:
    urlpatterns.append(path("activate/<str:token>/", ActivateView.as_view(), name="activate"))
