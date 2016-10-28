from django.contrib import admin

from .models import Station, Bike,Booking

admin.site.register(Station)
admin.site.register(Bike)
admin.site.register(Booking)
