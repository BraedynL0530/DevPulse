from django.http import JsonResponse
from django.shortcuts import render
from rest_framework_api_key.models import APIKey
import json
from models import ProjectMetrics
def getApiKey(request):
    return render(request, "GetApiKey.html")

def generateApiKey(request):
    api_key, key = APIKey.objects.create_key(name="api_keys")
    return JsonResponse({"key": key})
def addHistory(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ProjectMetrics.errors = data["errors"]
        ProjectMetrics.successes = data["successes"]
        ProjectMetrics.total_requests = data["total"]
        ProjectMetrics.avg_latency = data["avg_latency_ms"]
        ProjectMetrics.p95_latency = data["p95_latency_ms"]


def fetchHistory(request):
    modelData = ProjectMetrics.objects.all()

    data = []
    for m in modelData:
        data.append({
            "project_name": m.project_name,
            "project_id": m.project_id,
            "avg_latency_ms": m.avg_latency_ms,
            "p95_latency_ms": m.p95_latency_ms,
            "effective_rps": m.effective_rps,
            "success": m.success,
            "errors": m.errors,
            "total": m.total,
        })

    return JsonResponse(data, safe=False)

