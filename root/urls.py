from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("change-me/", admin.site.urls),
]
