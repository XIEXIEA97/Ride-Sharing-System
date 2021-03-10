from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Vehicle)
admin.site.register(Ride)
admin.site.register(SpecialInfo)
admin.site.register(UserDriveRide)
admin.site.register(UserShareRide)