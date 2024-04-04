from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from airport_service import settings

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("__debug__/", include("debug_toolbar.urls")),
                  path(
                      "api/v1/airport_app/",
                      include("airport_app.urls", namespace="airport_app")
                  ),
                  path("chaining/", include('smart_selects.urls')),
                  path("api/v1/user/", include("user.urls", namespace="user")),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
