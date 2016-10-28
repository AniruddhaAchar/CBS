from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'home/$', views.home, name = "home"),
url(r'book/$', views.booking, name = 'booking'),
url(r'^accounts/register/$', views.register, name='register'),
url(r'^login/$', views.login, name='login'),
url(r'^logout/$', views.log_out, name='logout'),
url(r'^ride/',views.ride, name="ride"),
url(r'^endRide/',views.end_ride, name="end_ride"),
url(r'^allBooking/',views.allRides,name = "all_rides"),
url(r'^sensor/',views.sensor,name = "sensor"),
]