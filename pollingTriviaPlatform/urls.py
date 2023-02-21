"""pollingTriviaPlatform URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from api.views import QuestionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),

]

