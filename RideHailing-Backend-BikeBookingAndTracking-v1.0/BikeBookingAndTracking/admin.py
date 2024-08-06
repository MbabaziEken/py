from django.contrib import admin

from .models import User, Driver, Vehicle, Ride, Location, Payment, FareEstimation

admin.site.register(User)
admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(Ride)
admin.site.register(Location)
admin.site.register(Payment)
admin.site.register(FareEstimation)
# Register your models here.
