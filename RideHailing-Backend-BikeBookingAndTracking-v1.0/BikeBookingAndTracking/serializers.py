from rest_framework import serializers
from .models import User, SurgePricing, Driver, Vehicle, Ride, Location, Payment, FareEstimation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['id', 'username', 'email','is_driver','phone_number','created_at','updated_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

class Driverserializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ['id','user','license_number','rating','created_at','updated_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }
    def create(self, validate_data):
            user_data = validate_data.pop('user')
            user = User.objects.create(**user_data)
            driver = Driver.objects.create(user=user, **validate_data)
            return  driver

class vehicleSerializer(serializers.ModelSerializer):
    driver = Driverserializer()
    
    class Meta:
        model = Vehicle
        fields = ['id', 'driver', 'make', 'model', 'license_plate', 'is_electric','created_at','updated_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

class LocationSerializer(serializers.ModelSerializer):
    rider = UserSerializer()
    driver = Driverserializer()
    vehicle = vehicleSerializer()

    class Meta:
        model = Location
        fields = ['id', 'ride','latitude','logitude','timestamp']
        extra_kwargs = {
            'timestamp': {'read_only': True}
        }

class RideSerializer(serializers.ModelSerializer):
    rider = UserSerializer()
    driver = Driverserializer()
    vehicle = vehicleSerializer()

    class Meta:
        model = Ride
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

class PaymentSerializer(serializers.ModelSerializer):
    ride = RideSerializer()

    class Meta:
        model = Payment
        fields = ['id','ride','amount','payment_method','payment_time']
        extra_kwaargs = {
            'payment_time': {'read_only':True}
        }

class FareEstimationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FareEstimation
        fields = '__all__'


class SurgePricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurgePricing
        fields = ['id','location','surge_multipler','start_time','end_time']


