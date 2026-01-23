from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

class Organization(models.Model):
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

class OrganizationAPIKey(AbstractAPIKey):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

class Project(models.Model):
    name = models.CharField(max_length=128)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

class ProjectAPIKey(AbstractAPIKey):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="api_keys")
    last_used_ip = models.GenericIPAddressField(null=True, blank=True)
    last_used = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)

class ProjectMetrics(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="metrics")
    errors = models.IntegerField(default=0)
    successes = models.IntegerField(default=0)
    total_requests = models.IntegerField(default=0)
    effective_Rps = models.FloatField(null=True, blank=True)
    avg_latency = models.FloatField(null=True, blank=True)
    p95_latency = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    bucket_size_seconds = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["project", "timestamp"]),
        ]