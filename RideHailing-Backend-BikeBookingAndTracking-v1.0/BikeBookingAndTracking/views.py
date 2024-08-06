from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import RideRequest, User, Driver, SurgePricing, Vehicle, Ride, Location, Payment, FareEstimation
from rest_framework import viewsets
from .serializers import UserSerializer, SurgePricingSerializer, Driverserializer, vehicleSerializer, RideSerializer, LocationSerializer, PaymentSerializer, FareEstimationSerializer
from django.contrib.auth.decorators import login_required
from .forms import RideRequestForm
from django.urls import reverse






class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
@permission_classes([])
def status(request):
    return Response({"status":"OK"})

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = Driverserializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = vehicleSerializer

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    def perform_create(self, serializer):
        ride = serializer.save()
        ride.estimate_fare()
        ride.save()

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serialilzer_class = LocationSerializer
    def get_serializer_class(self):
        return LocationSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class FareEstimationViewSet(viewsets.ModelViewSet):
    queryset = FareEstimation.objects.all()
    serializer_class = FareEstimationSerializer

class SurgePricingViewSet(viewsets.ModelViewSet):
    queryset = SurgePricing.objects.all()
    serializer_class = SurgePricingSerializer



# Create your views here. okay i did



@login_required
def create_ride_request(request):
    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            ride_request = form.save(commit=False)
            ride_request.User = request.User
            ride_request.save()
            return redirect('view_ride_requests')
    else:
        form = RideRequestForm()
    return render(request, 'ride_request_form.html', {'form': form})

@login_required
def create_ride_request(request):
    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            ride_request = form.save(commit=False)
            ride_request.User = request.User
            ride_request.save()
            return redirect('view_ride_requests')
    else:
        form = RideRequestForm()
    return render(request, 'ride_request_form.html', {'form': form})


    



@login_required
def view_ride_requests(request):
    ride_requests = RideRequest.objects.filter(user=request.user)
    return render(request, 'ride_requests.html', {'ride_requests': ride_requests})

@login_required
def cancel_ride_request(request, ride_request_id):
    ride_request = RideRequest.objects.get(id=ride_request_id)
    if ride_request.user == request.user:
        ride_request.delete()
    return redirect('view_ride_requests')



