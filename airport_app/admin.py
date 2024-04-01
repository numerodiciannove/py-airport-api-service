from django.contrib import admin

from airport_app.models import (
    Country,
    City,
    Airport,
    Airplane,
    Route,
    Flight,
    Order,
    Ticket,
)

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Airplane)
admin.site.register(Flight)
admin.site.register(Order)
admin.site.register(Ticket)
