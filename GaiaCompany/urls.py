from django.urls import path

from .views import CompanyViewSet, SwitchCompanyView

urlpatterns = [
    path("", CompanyViewSet.as_view({"get": "list", "post": "create"}), name="company-list"),
    path("<int:id>/", CompanyViewSet.as_view({"get": "retrieve"}), name="company-detail"),
    path("switch/", SwitchCompanyView.as_view(), name="switch-company"),
]
