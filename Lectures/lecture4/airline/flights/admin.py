from django.contrib import admin
from .models import Flight, Airport, Passenger # import models into admin site

# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin) # update config for display
admin.site.register(Passenger, PassengerAdmin)