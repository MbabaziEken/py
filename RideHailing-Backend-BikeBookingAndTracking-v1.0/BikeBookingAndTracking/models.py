from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models  # Combine both models imports into one
from django.utils import timezone
import datetime

class User(AbstractUser):
    #User models extrending the default Django user models.
    is_driver = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    groups = models.ManyToManyField(
        Group,
        related_name='bike_booking_users',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=('groups'),
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='bike_booking_user_permissions',
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

    class Meta:
        indexes = [
            models.Index(fields=['phone_number']),
        ]



class Driver(models.Model):
    #Driver model extending the usermodels for driver-specific information.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    #is_available = models.BooleanField(default=True) #for further discussion.

class Vehicle(models.Model):
    #Vehicle models to store info about drive's vehicle
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=20, db_index=True)
    is_electric = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['license_plate']),
        ]

class Ride(models.Model):
    #Ride model to represent a booking.
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, related_name='rides')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    pickup_time = models.DateTimeField(default=timezone.now)
    dropoff_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[

    ('requested', 'Requested'),
    ('accepted', 'Accepted'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled')
    ], default='requested')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rider_rating = models.FloatField(default=1.0)
    rider_feedback = models.TextField(null=True, blank=True)
    estimated_fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   
    class Meta:
        indexes = [
            models.Index(fields=['pickup_location']),
            models.Index(fields=['dropoff_location']),
        ]
    def estimate_fare(self):
         base_fare = 10.0
         distance = 5.0
         time = 15

         now = timezone.now()
         active_surge =  SurgePricing.objects.filter(
              location=self.pickup_location,
              start_time__lte=now,
              end_time__gte=now
         ).first()

         surge_multiplier = active_surge.surge_multiplier if active_surge else 1.0
         estimated_fare = base_fare + (distance*2) + (time* 0.5)
         estimated_fare *= surge_multiplier

         self.estimate_fare = estimated_fare
         self.save()

    def __str__(self):
         return f"Ride from {self.pick_location} to {self.dropoff_location}"
    #def estimate_fare(self):
    #    traffic_level = 0.5 #eg value
     #   time_of_day = self.pickup_time.time()
    #    weather_conditions = "sunny" #eg value
    #    day_of_week = self.pickup_time.strftime('%A')
     #   distance = self.calculate_distance() #note to self, a method to calculate the distance between the pickup and drop off locations. 


     #   fare_estimation = FareEstimation(
     #   traffic_level = traffic_level,
     #   time_of_day = time_of_day,
     #  weather_conditions = weather_conditions,
     #    day_of_week =day_of_week,
     #   distance=distance
    
      #  self.estimate_fare = fare_estimation.estimate_fare()

   # def calculate_distance(self): #trying to implement the distance calculation logic, possibly using a third_party API or services. Matrix API for Google, unknown for MApbox.
       # return 10.0 # eg of distance
            
   # def __str__(self):
      #  return f"Ried from {self.pickup_location} to {self.dropoff_location}"


class  Location(models.Model):
    #Location model to track the location update for a ride
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='location')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    coordinates = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
        ]

#add the payment determining model.
class Payment(models.Model):
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('mobile_money','Mobile Money'),
        ('cash','Cash')
    ])
    payment_status = models.CharField(max_length=50, choices=[
        ('pending','Pending'),
        ('succeded','Succeded'),
        ('failed','Failed')
    ], default='pending')
    timestamp = models.DateField(auto_now_add=True)

class FareEstimation(models.Model):
    traffic_level = models.FloatField() #value between 0.0 (no traffic) and 1.0 (heavy traffic)
    time_of_day = models.TimeField(auto_now=True)
    weather_condition = models.CharField(max_length=50) #eg sunny, rainy, etc
    day_of_week = models.CharField(max_length=20)
    distance = models.FloatField() #distance to be travelled in kilometers.
    
    def estimate_fare(self):
        base_fare = 5.00 # I am using currency points, subject to editing.
        per_km_rate = 2.00 #rate per kilometer moved
        pass

        #factors to influence the fare estimation
        traffic_multiplier = 1 + self.traffic_level
        time_of_day_multiplier = 1.2 if (self.time_of_day >= datetime.time(17,0) and self.time_of_day <= datetime.time(23,0)) else 1
        weather_multiplier = 1.5 if self.weather_condition in ['rainy'] else 1
        day_of_week_multiplier = 1.2 if self.day_of_week in ['Monday','Tuesday','Friday'] else 1

        #fare calculator
        fare = base_fare + (self.distance * per_km_rate * traffic_multiplier * time_of_day_multiplier * weather_multiplier * day_of_week_multiplier)
        return round(fare, 2)
    
    def __str__(self):
        return f"Fare estimation for {self.distance} km at {self.time_of_day}"
    

class RideRequest(models.Model):
        user = models.ForeignKey('User', on_delete=models.CASCADE)
        pickup_location = models.FloatField()
        dropoff_location = models.FloatField()
        timestamp = models.DateTimeField(default=timezone.now)

        def __str__(self):
            return f"RideRequest by {self.user} at {self.timestamp}"
        
class DriverAvailability(models.Model):
        driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
        location = models.FloatField()
        available = models.BooleanField(default=True)
        timestamp = models.DateTimeField(default=timezone.now)
    

        def __str__(self):
            return f"DriverAvailability for {self.driver} at {self.timestamp}"
        
class SurgePricing(models.Model):
        location = models.FloatField()
        surge_multiplier = models.DecimalField(max_digits=3, decimal_places=2)
        start_time = models.DateTimeField()
        end_time = models.DateTimeField

        def is_active(self):
            return f'SurgePricing at {self.location} from {self.start_time} to {self.end_time} with multiplier {self.surge_multiplier}'