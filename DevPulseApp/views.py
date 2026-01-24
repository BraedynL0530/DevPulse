from django.shortcuts import render
from rest_framework_api_key.models import APIKey
import json
from models import ProjectMetrics
def getApiKey(request):
    api_key, key = APIKey.objects.create_key(name="api_keys")

def addHistory(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ProjectMetrics.errors = data["errors"]
        ProjectMetrics.successes = data["successes"]
        ProjectMetrics.total_requests = data["total"]
        ProjectMetrics.avg_latency = data["avg_latency_ms"]
        ProjectMetrics.p95_latency = data["p95_latency_ms"]


def fetchHistory(request):
    return None