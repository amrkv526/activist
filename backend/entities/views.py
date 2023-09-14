import json
from uuid import UUID

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request

from .models import Organization
from .serializers import OrganizationSerializer


@method_decorator(csrf_exempt, name="dispatch")
class OrganizationView(View):
    def post(self, request: Request) ->  JsonResponse:
        data = json.loads(request.body.decode("utf-8"))
        name = data.get("name")
        tagline = data.get("tagline")

        organization_data = {"name": name, "tagline": tagline}

        organization = Organization.objects.create(**organization_data)

        data = {"message": f"New Organization created with id: {organization.id}"}
        return JsonResponse(data, status=201)

    def get(self, request: Request) -> JsonResponse:
        organizations = Organization.objects.all()
        data = OrganizationSerializer(organizations, many=True)

        return JsonResponse(data.data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class OrganizationUpdate(View):
    def patch(self, request: Request, organization_id: UUID) -> JsonResponse:
        data = json.loads(request.body.decode("utf-8"))
        org = Organization.objects.get(id=organization_id)
        org.name = data["name"]
        org.tagline = data["tagline"]
        org.save()

        data = {"message": f"Organization {organization_id} has been updated"}
        return JsonResponse(data)

    def delete(self, request: Request, organization_id: UUID) ->JsonResponse:
        data = json.loads(request.body.decode("utf-8"))
        org = Organization.objects.get(id=organization_id)
        org.delete()

        data = {
            "message": f"Organization {organization_id} has been deleted successfully"
        }
        return JsonResponse(data)
