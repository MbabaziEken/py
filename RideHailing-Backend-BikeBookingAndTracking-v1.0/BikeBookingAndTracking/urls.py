from BikeBookingAndTracking import views

from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import UserViewSet, status, DriverViewSet, VehicleViewSet, RideViewSet, LocationViewSet, PaymentViewSet, FareEstimationViewSet, SurgePricingViewSet

router = DefaultRouter()

router.register(r'users',UserViewSet)
router.register(r'drivers',DriverViewSet)
router.register(r'vehicles',VehicleViewSet)
router.register(r'rides',RideViewSet)
router.register(r'locations',LocationViewSet)
router.register(r'payments',PaymentViewSet)
router.register(r'fare_estimations',FareEstimationViewSet)
router.register(r'surge-pricing', SurgePricingViewSet)


#urlpatterns =[
#    path('', include(router.urls)),
#]
urlpatterns = [
    path('', include(router.urls)),
    path('status/', status),
    path('create-ride-request/', views.create_ride_request, name='create_ride_request'),
    path('view-ride-requests/', views.view_ride_requests, name='view_ride_requests'),
    path('cancel-ride-request/<int:ride_request_id>/', views.cancel_ride_request, name='cancel_ride_request'),
    ]
#create a url for is_available call to the frontend. pkay i did