from rest_framework import routers
from airport_app.views import (
    CountryViewSet,
    CityViewSet,
    AirportViewSet,
)

app_name = "airport_app"

router = routers.DefaultRouter()

router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)
router.register("airports", AirportViewSet)

urlpatterns = router.urls
