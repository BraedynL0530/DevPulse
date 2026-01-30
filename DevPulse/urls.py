from django.urls import path
from DevPulseApp import views

urlpatterns = [
    path('devpulse/get-apikeys', views.getApiKey),
    path("api.devpulse/generate-key", views.generateApiKey),
    path('api.devpulse/add-history', views.addHistory), #log
    path('api.devpulse/get-history',views.fetchHistory)
]
