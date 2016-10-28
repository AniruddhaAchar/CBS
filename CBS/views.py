from django.shortcuts import render, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from .forms import SignupForm,BookingForm
from .models import Booking, Bike
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import requires_csrf_token
from django.utils import timezone
from pubnub import Pubnub
import json

@requires_csrf_token
def index(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/home')
	else:
		form = SignupForm()
	token = {}
	token['form'] = form
	return render(request,'CBS/index.html',token)

@login_required(login_url='/')
@requires_csrf_token
def home(request):
	booked_rides = None
	booking_list = None
	recent_booking =None
	bikes = None
	if request.method == 'POST':
		form = BookingForm(request.POST)
		if form.is_valid():
			form.setuser(request.user)
			form.save()
			return HttpResponseRedirect('/home')
	else:
		form = BookingForm()
	try:
		booked_rides = Booking.objects.all().filter(booking_user = request.user,booking_end_time__isnull = True)
		recent_booking = list(booked_rides)[-1]
		station = recent_booking.booking_station
		bikes =  Bike.objects.all().filter(station_name = station)
		station = [b.booking_station for b in booked_rides.all()]
		time = [b.booking_time for b in booked_rides.all()]
		booking_list = zip(time,station)
	except Exception :
		print ("Exception")
	token = {}
	token['form']= form
	if booked_rides:
		token['booking_list'] = booking_list
		token['recent_booking'] = recent_booking
	if bikes:
		token["bikes"] = bikes
	return render(request,'CBS/home.html',token)

@login_required(login_url='/')
@requires_csrf_token
def booking(request):
	try:
		selected_bike = stations.bike_set.get(pk = request.POST['bike'])
		print (selected_bike)
	except:
		print ("error")

def register(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/home')
	else:
		form = SignupForm()
	token = {}
	token['form'] = form
	return render_to_response('registration/signup.html',token)

def loggedin(request):
    return render_to_response('/home.html')

def log_out(request):
	auth.logout(request)
	return render(request,'CBS/logout.html')

@requires_csrf_token
def login(request):
	print ("Enetred login")
	if request.method == "POST":
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		user = auth.authenticate(username = username, password = password)
		if user is not None:
			print ('logged in')
			auth.login(request,user)
			return HttpResponseRedirect('/home')
		else:
			print ("Login error")
			messages.error(request, 'Incorrect username or password')
			return HttpResponseRedirect('/')
	else:
		token = {}
		return render_to_response('CBS/index.html',token)

@login_required(login_url='/')
@requires_csrf_token
def ride(request):
	if request.method == "POST":
		current_ride = None
		bike_no = request.POST.get("bike_no")
		booking_id = request.POST.get("booking_id")
		try:
			bike = Bike.objects.get(bike_name = bike_no)
			current_ride = Booking.objects.get(pk=booking_id)
			current_ride.booking_bike = bike
			bike.in_use = True
			print (bike, current_ride.booking_bike)
			current_ride.save() 
			bike.save()
			sendNotification("Start",bike_no)
			
		except Exception:
			print ("Exception ")
		token = {}
		if current_ride:
			token['current_ride'] = current_ride
		return render(request,"CBS/riding.html",token)
	else:
		return render(request,"CBS/error.html",token)

@login_required(login_url='/')
def end_ride(request):
	print("In end ride")
	if request.method == "POST":
		booking_id = request.POST.get("booking_id")
		booking_bike = request.POST.get("bike_no")
		bike = Bike.objects.get(bike_name=booking_bike)
		bike.in_use = False
		bike.save()
		booking = Booking.objects.get(pk = booking_id)
		booking.booking_end_time = timezone.now()
		booking.save(); 
		sendNotification("End",booking_bike)
		return HttpResponseRedirect('/home')
	else:
		return render(request,"CBS/error.html")

@login_required(login_url='/')
def allRides(request):
	booked_rides = Booking.objects.all().filter(booking_user = request.user)
	print(booked_rides)
	token = {}
	token['booked_rides'] = booked_rides
	return render(request,"CBS/bookedRides.html",token)


def sensor(request):
	return render(request,"CBS/sensor.html")

def sendNotification(notif,bikeNo):
	pubnub = Pubnub(publish_key="pub-c-c8508a4f-2f25-4934-b2d1-02b9872a3c20", subscribe_key="sub-c-425d0caa-1da9-11e6-b700-0619f8945a4f")
	def callback(message):
		print(message)
	message = "{\"Bike\":\""+bikeNo+"\",\"State\":\""+notif+"\"}"
	pubnub.publish('bikes_channel', message, callback=callback, error=callback)
	
