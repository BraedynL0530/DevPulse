from django.contrib.sites import requests
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from rest_framework_api_key.models import APIKey
import json
from .models import ProjectMetrics, OrganizationAPIKey, Organization, User, OrganizationMember
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import os
from django.contrib.auth import authenticate, login


def getApiKey(request):
    return render(request, "GetApiKey.html")


def generate(request): #proxy :3
    res = requests.post(
        os.getenv("API_KEY"), #generate api key
    )
    return JsonResponse(res.json())

def generateApiKey(request):
    try:
        org= 0#temp
        api_key, key = OrganizationAPIKey.objects.create_key(
            organization=org,#later
        )
        return JsonResponse({"key": key})
    except Exception as e:
        return JsonResponse({"error": str(e)})

#TODO: ratelimiting
@csrf_exempt
def addHistory(request):
    if not request.api_key.organization.active:
        return HttpResponseForbidden("You are not authorized to view this page. Try checking your API key.")
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            ProjectMetrics.objects.create(
                project=...,  # need to link to project
                errors=data["errors"],
                successes=data["success"],
                total_requests=data["total"],
                avg_latency=data["avg_latency_ms"],
                p95_latency=data["p95_latency_ms"],
                bucket_size_seconds=data["interval"] # Add in go too
            )
        except Exception as e:
            return JsonResponse({"error": str(e)})

@csrf_exempt
def fetchHistory(request):
    if not request.api_key.organization.active:
        return HttpResponseForbidden("You are not authorized to view this page. Try checking your API key.")
    model_data = ProjectMetrics.objects.all()
    try:
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
    except Exception as e:
        return JsonResponse({"error": str(e)})

def dashboard(request):
    if not request.api_key.organization.active:
        return HttpResponseForbidden("You are not authorized to view this page. Try checking your API key.")


def login_page(request):
    return render(request, 'login.html')

def signupLogin(request):
    if request.method == "Post":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data["password"]
            api_key = data.get('api_key')
            user = authenticate(request, username=email, password=password)

            # If user exist login
            if user is not None:
                login(request, user)
                return JsonResponse({"success": True})

            if api_key:
                #join org
                try:
                    org_key = OrganizationAPIKey.objects.get(key=api_key)
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                        organization=org_key.organization
                    )
                    OrganizationMember.objects.create(
                        user=user,
                        organization=org_key.organization,
                        role='member'
                    )
                except:
                    return JsonResponse({"error": "Invalid API key"}, status=400)
            else:
                #make org
                try:
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password
                    )
                    org = Organization.objects.create(
                        name=f"{email}'s Organization",
                        owner=user
                    )
                    user.organization = org
                    user.save()

                    OrganizationMember.objects.create(
                        user=user,
                        organization=org,
                        role='owner'
                    )

                    login(request, user)
                    return JsonResponse({"success": True})

                except Exception as e:
                    return JsonResponse({"error": str(e)}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


