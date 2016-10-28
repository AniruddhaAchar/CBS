from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Station(models.Model):
		station_name = models.CharField(max_length=100)
		station_address = models.CharField(max_length = 300)
		class Meta:
		    verbose_name = "Station"
		    verbose_name_plural = "Stations"
		def __str__(self):
		    return self.station_name


class Bike(models.Model):
   bike_name = models.CharField(max_length=100)
   station_name = models.ForeignKey(Station, on_delete = models.CASCADE)
   in_use = models.BooleanField(default=False)
   class Meta:
       verbose_name = "Bike"
       verbose_name_plural = "Bikes"
   def __str__(self):
       return self.bike_name
      

class Booking(models.Model):
		booking_user = models.ForeignKey(User)
		booking_time = models.DateTimeField(default = timezone.now)
		booking_station = models.ForeignKey(Station)
		booking_bike = models.ForeignKey(Bike, null=True)
		booking_end_time = models.DateTimeField(null = True)
		class Meta:
		    verbose_name = "Booking"
		    verbose_name_plural = "Bookings"
		def __str__(self):
		    return str(self.id)

    
