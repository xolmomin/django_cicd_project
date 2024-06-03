from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("botir/", admin.site.urls),
]
