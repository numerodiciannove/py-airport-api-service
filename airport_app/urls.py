from rest_framework import routers
from django.urls import path, include
from airport_app.views import (
    CountryViewSet,
    CityViewSet,
    AirportViewSet,
    RouteViewSet,
    AirplaneViewSet,
    AirplaneTypeViewSet,
    CrewViewSet,
)

app_name = "airport_app"

router = routers.DefaultRouter()

router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("crew", CrewViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
