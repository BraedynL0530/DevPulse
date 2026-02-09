from django.urls import path, include
from DevPulseApp import views
import os
from dotenv import load_dotenv
urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('devpulse/get-apikeys', views.getApiKey),
    path("api.devpulse/proxy-path", views.generate),
    path(os.getenv("API_KEY"), views.generateApiKey), # put endpoint inside env and modified the link
    path('api.devpulse/add-history', views.addHistory), #log
    path('devpulse/dashboard/', views.dashboard, name='dashboard'),
    path('api.devpulse/create-project', views.createProject),
    path('api.devpulse/delete-project', views.deleteProject),
    path('api.devpulse/get-history',views.fetchHistory),
    path('devpulse/login', views.login_page, name='login'),
    path('api.devpulse/signup-login', views.signupLogin),
]
