from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/v1/airport_app/",
         include("airport_app.urls", namespace="airport_app")),
    path("chaining/", include('smart_selects.urls')),
]
