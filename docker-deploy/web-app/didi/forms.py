from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class DriverRegisterForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'plate_number', 'license_number', 'vehicle_capacity']

class SpecialInfoForm(ModelForm):
    class Meta:
        model = SpecialInfo
        fields = '__all__'

class ModifyFeatureForm(ModelForm):
    feature = forms.ModelMultipleChoiceField(
        queryset = SpecialInfo.objects.all(),
        widget  = forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Vehicle
        fields = ['feature']

class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)

class RequestRideForm(ModelForm):

    request = forms.ModelMultipleChoiceField(
        queryset = SpecialInfo.objects.all(),
        widget  = forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Ride
        fields = ['start_point', 'destination', 'arrival_time', 'owner_psger_num', 'vehicle_type', 'sharable', 'request']
        # 'start_time', 
        labels = {
            'owner_psger_num': 'number of passengers from my party',
        }
        widgets = {
            'arrival_time': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            # 'start_time': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["arrival_time"].widget = DateTimeInput()
        # self.fields["start_time"].widget = DateTimeInput()

class searchOpenRideFormSharer(ModelForm):
    earliest_arrival_time=forms.CharField(widget=DateTimeInput())
    latest_arrival_time=forms.CharField(widget=DateTimeInput())
    class Meta:
        model = Ride
        fields = ['destination', 'owner_psger_num']
        labels = {
            'owner_psger_num': 'number of passengers from my party',
        }
        widgets = {
            'arrival_time': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class searchOpenRideFormDriver(ModelForm):
    feature = forms.ModelMultipleChoiceField(
        queryset = SpecialInfo.objects.all(),
        widget  = forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Vehicle
        fields = ['vehicle_capacity','vehicle_type']
        
class RideSpecialRequestForm(forms.Form):
    ride_special_request = forms.ModelMultipleChoiceField(
        queryset = SpecialInfo.objects.all(),
        widget  = forms.CheckboxSelectMultiple,
        required=False,
    )

class ShareEditForm(ModelForm):
    class Meta:
        model = UserShareRide
        fields = ['psger_num']