from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Company
from .serializers import CompanySerializer


class SwitchCompanyView(APIView):
    def post(self, request):
        company_id = request.data.get("company_id", None)
        if not company_id:
            return Response({"non_field_errors": ["Company ID is required"]}, status=400)

        try:
            company = Company.objects.get(id=company_id)
            request.session["active_company"] = company.id
            return Response(CompanySerializer(company).data)
        except Company.DoesNotExist:
            return Response({"non_field_errors": ["Company not found"]}, status=404)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ["get", "post"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def active(self, request):
        company = request.active_company
        if not company:
            return Response({"non_field_errors": ["No active company"]}, status=404)
        return Response(CompanySerializer(company).data)
