from rest_framework import routers
from airport_app.views import (
    CountryViewSet,
    CityViewSet,
    AirportViewSet,
    RouteViewSet,
)

app_name = "airport_app"

router = routers.DefaultRouter()

router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)

urlpatterns = router.urls
