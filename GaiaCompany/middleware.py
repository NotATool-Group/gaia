from GaiaCompany.models import Company


class ActiveCompanyMiddleware:
    """
    Middleware to set the active company for the request.

    This middleware sets the active company for the request based on the company_id stored in the session.
    If the company_id is not found in the session, the first company is set as the active company.

    This way, the user can switch between companies during the session and the choice will be remembered as long
    as the session is active.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        company_id = request.session.get("active_company", None)
        if company_id:
            try:
                company = Company.objects.get(id=company_id)
                request.active_company = company
            except Company.DoesNotExist:
                request.active_company = None
        else:
            request.active_company = Company.objects.first()

        return self.get_response(request)
