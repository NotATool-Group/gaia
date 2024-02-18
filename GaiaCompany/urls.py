from django.urls import path

from .views import CompanyViewSet, SwitchCompanyView

urlpatterns = [
    path("switch/", SwitchCompanyView.as_view(), name="switch-company"),
    path("active/", CompanyViewSet.as_view({"get": "active"}), name="active-company"),
    path("", CompanyViewSet.as_view({"get": "list", "post": "create"}), name="company-list"),
    path("<int:id>/", CompanyViewSet.as_view({"get": "retrieve"}), name="company-detail"),
]
