from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin2/", admin.site.urls),
]


