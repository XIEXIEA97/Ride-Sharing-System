from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SpecialInfo(models.Model):
    information = models.CharField(max_length=100)

    def __str__(self):
        return self.information

class Vehicle(models.Model):
    CAR = 'CR'
    VAN = 'VN'
    BUS = 'BS'
    TRUCK = 'TK'
    VEHICLE_TYPES = [
        (CAR, 'Car'),
        (VAN, 'Van'),
        (BUS, 'Bus'),
        (TRUCK, 'Truck'),
    ]
    DEFAULT_CAPACITY = {
        CAR: 10,
        VAN: 20,
        TRUCK: 10,
        BUS: 100,
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    vehicle_type = models.CharField(choices=VEHICLE_TYPES, blank=True, max_length=2)
    plate_number = models.CharField(max_length=20, blank=True, unique=True)
    license_number = models.CharField(max_length=20, blank=True, unique=True)
    vehicle_capacity = models.PositiveSmallIntegerField(default=0, blank=True)
    feature = models.ManyToManyField(SpecialInfo)

    def __str__(self):
        return self.user.get_full_name() + "'s vehicle with plate number: " + self.plate_number

class Ride(models.Model):
    OP = 'OPEN'
    SD = 'SHARED'
    CF = 'CONFIRMED'
    CP = 'COMPLETE'
    Status = [
        (OP, 'Open'),
        (SD, 'Shared'),
        (CF, 'Confirmed'),
        (CP, 'Complete'),
    ]
    ride_owner = models.ForeignKey(User, related_name='ride_owner_uid', on_delete=models.CASCADE)
    start_point = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    #start_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    request_time = models.DateTimeField(auto_now_add=True)
    # number of total passengers from the owner’s party
    owner_psger_num = models.PositiveSmallIntegerField(default=1)
    # only one vehicle type can be chosen
    vehicle_type = models.CharField(choices=Vehicle.VEHICLE_TYPES, max_length=2)
    sharable = models.BooleanField(default=False)
    status = models.CharField(choices=Status, default=OP, max_length=9)
    request = models.ManyToManyField(SpecialInfo)

    def __str__(self):
        return "From " + self.start_point + " to " + self.destination + " arrived at " + timezone.localtime(self.arrival_time).strftime("%Y-%m-%d %H:%M:%S")

class UserDriveRide(models.Model):
    user_driver = models.ForeignKey(Vehicle, related_name='driver_vehicle', on_delete=models.CASCADE)
    ride = models.OneToOneField(Ride, related_name='driver_rid', on_delete=models.CASCADE)
    claim_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_driver.user.get_full_name() + " drives ride No. " + str(self.ride.id)

class UserShareRide(models.Model):
    user_sharer = models.ForeignKey(User, related_name='sharer_uid', on_delete=models.CASCADE)
    ride = models.ForeignKey(Ride, related_name='sharer_rid', on_delete=models.CASCADE)
    join_time = models.DateTimeField(auto_now_add=True)
    psger_num = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('user_sharer', 'ride')

    def __str__(self):
        return self.user_sharer.get_full_name() + " joins ride No. " + str(self.ride.id)
