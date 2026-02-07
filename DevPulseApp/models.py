from django.db import models
from rest_framework_api_key.models import AbstractAPIKey
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    email = models.EmailField(unique=True)
    organization = models.ForeignKey('Organization', null=True, on_delete=models.SET_NULL)

class Organization(models.Model):
    name = models.CharField(max_length=128)
    invite_code = models.CharField(max_length=32, unique=True)
    active = models.BooleanField(default=True)

class OrganizationAPIKey(AbstractAPIKey):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, default="Unnamed Key")  # "Production CLI", "Dev Environment"
    last_used = models.DateTimeField(null=True, blank=True)

class OrganizationMember(models.Model):
    ROLES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)

class Project(models.Model):
    name = models.CharField(max_length=128)
    project_id = models.CharField(max_length=128, default=None)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class ProjectMetrics(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="metrics")
    errors = models.IntegerField(default=0)
    successes = models.IntegerField(default=0)
    total_requests = models.IntegerField(default=0)
    avg_latency = models.FloatField(null=True, blank=True)
    p95_latency = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields=["project", "timestamp"]),
        ]