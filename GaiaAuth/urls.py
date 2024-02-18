from django.urls import path
from .views import RegisterView, LoginView, LogoutView, MeView, ActivateView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("activate/<str:token>/", ActivateView.as_view(), name="activate"),
]
