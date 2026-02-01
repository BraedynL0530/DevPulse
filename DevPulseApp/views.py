from django.contrib.sites import requests
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from rest_framework_api_key.models import APIKey
import json
from models import ProjectMetrics,OrganizationAPIKey, Organization
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import os

@ensure_csrf_cookie
def get_csrf_token(request):
    # This view will ensure the 'csrftoken' cookie is set in the response
    return JsonResponse({"message": "CSRF cookie set"})
def getApiKey(request):
    return render(request, "GetApiKey.html")

@csrf_exempt
def generate(request): #proxy :3
    res = requests.post(
        os.getenv("API_KEY"), #generate api key
    )
    return JsonResponse(res.json())

def generateApiKey(request):
    api_key, key = OrganizationAPIKey.objects.create_key(
        name="default",
        organization=org,#later
    )
    return JsonResponse({"key": key})

#TODO: ratelimiting
def addHistory(request):
    if not request.api_key.organization.active:
        return HttpResponseForbidden("You are not authorized to view this page. Try checking your API key.")
    if request.method == "POST":
        data = json.loads(request.body)
        ProjectMetrics.objects.create(
            project=...,  # need to link to project
            errors=data["errors"],
            successes=data["success"],
            total_requests=data["total"],
            avg_latency=data["avg_latency_ms"],
            p95_latency=data["p95_latency_ms"],
            bucket_size_seconds=data["interval"] # Add in go too
        )


def fetchHistory(request):
    if not request.api_key.organization.active:
        return HttpResponseForbidden("You are not authorized to view this page. Try checking your API key.")
    model_data = ProjectMetrics.objects.all()

    data = []
    for m in model_data:
        data.append({
            "project_name": m.project.name,
            "project_id": m.project_id,
            "avg_latency_ms": m.avg_latency,
            "p95_latency_ms": m.p95_latency,
            "success": m.successes,
            "errors": m.errors,
            "total": m.total_requests,
        })

    return JsonResponse(data, safe=False)

def dashboard(request):
    if not request.api_key.organization.active:
        return HttpResponseForbidden("You are not authorized to view this page. Try checking your API key.")

