from typing import KeysView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import BadHeaderError, send_mail
from django.http import Http404
from django.urls import conf
from django.core.mail import send_mail
from .models import *
from .forms import *
import sys
from django.db.models import Count, Q, F

@login_required(login_url='didi:login')
def userHomePage(request):
    user = request.user
    name = user.get_full_name()
    try:
        vehicle = Vehicle.objects.get(user=user)
        features = SpecialInfo.objects.filter(vehicle=vehicle)
    except (KeyError, Vehicle.DoesNotExist):
        vehicle = None
        features = None
    try:
        my_rides = Ride.objects.filter(ride_owner=user).exclude(status=Ride.CP)
        shared_rides = Ride.objects.filter(sharer_rid__user_sharer=user).exclude(status=Ride.CP)
        # drive_rides = Ride.objects.filter(driver_rid__user_driver=vehicle).exclude(status=Ride.CP)
    except (KeyError, Ride.DoesNotExist):
        my_rides = None
        shared_rides = None
        # drive_rides = None
    try:
        my_sharer_rides = shared_rides
        my_confirmed_rides_vehicle = []
        my_confirmed_owner_rides = my_rides.filter(status=Ride.CF) ## as ride owner
        my_confirmed_sharer_rides = shared_rides.filter(status=Ride.CF) ## as ride sharer
        my_confirmed_rides = my_confirmed_owner_rides | my_confirmed_sharer_rides
        for r in my_confirmed_rides:
            my_confirmed_rides_vehicle.append(Vehicle.objects.get(driver_vehicle__ride=r))
        test = zip(my_confirmed_rides, my_confirmed_rides_vehicle)
    except (KeyError, Ride.DoesNotExist, Vehicle.DoesNotExist):
        my_sharer_rides = None    
        my_confirmed_rides_vehicle = None
        my_confirmed_rides = None

    try:
        confirmed_rides = Ride.objects.filter(driver_rid__user_driver=vehicle).filter(status=Ride.CF) ## as driver
    except (KeyError, Ride.DoesNotExist):
        confirmed_rides = None
    context = {
        'confirmed_drive_rides':confirmed_rides,
        'my_confirmed_rides_vehicle':my_confirmed_rides_vehicle,
        'my_confirmed_rides':test,
        'my_sharer_rides': shared_rides,
        'user':user, 
        'name':name, 
        'vehicle':vehicle, 
        'features':features, 
        'my_rides':my_rides, 
        # 'drive_rides':drive_rides, 
        # 'open_rides_result' : []
    }
    return render(request, 'didi/home.html', context)

def userRegister(request):
    if request.user.is_authenticated:
        return redirect('didi:home')

    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User ' + form.cleaned_data.get('username') + ' created!')
            return redirect('didi:login')

    context = {'form':form}
    return render(request, 'didi/register.html', context)

@login_required(login_url='didi:login')
def userEdit(request):
    form = UserEditForm(instance=request.user)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User ' + request.user.username + "'s profile updated!")
            # return render(request, 'didi/edit_personal.html', context)

    context = {'form':form}
    return render(request, 'didi/edit_personal.html', context)

@login_required(login_url='didi:login')
def resetPassword(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        return redirect('didi:home')
    context = {'form':form}
    return render(request, 'didi/reset_password.html', {'form': form})

def userLogin(request):
    if request.user.is_authenticated:
        return redirect('didi:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('didi:home')
        else:
            messages.info(request, 'username/password mismatch')
    context = {}
    return render(request, 'didi/login.html', context)

def userLogout(request):
    logout(request)
    return redirect('didi:login')

@login_required(login_url='didi:login')
def driverRegister(request):
    form = DriverRegisterForm()
    if request.method == 'POST':
        form = DriverRegisterForm(request.POST, instance=Vehicle(user=request.user))
        if form.is_valid():
            form.save()
            return redirect('didi:home')
    context = {'form':form, }
    return render(request, 'didi/driver_register.html', context)


@login_required(login_url='didi:login')
def driverUnregister(request):
    vehicle = Vehicle.objects.get(user=request.user)
    context = {'vehicle':vehicle}
    if request.method == 'POST':
        vehicle.delete()
        return redirect('didi:home')
    return render(request, 'didi/driver_unregister.html', context)

@login_required(login_url='didi:login')
def driverUpdate(request):
    vehicle = Vehicle.objects.get(user=request.user)
    form = DriverRegisterForm(instance=vehicle)
    if request.method == 'POST':
        form = DriverRegisterForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('didi:home')
    context = {'form':form, }
    return render(request, 'didi/driver_update.html', context)

@login_required(login_url='didi:login')
def createSpecialInfo(request):
    if request.method == 'POST':
        form = SpecialInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('didi:si_modify')

@login_required(login_url='didi:login')
def modifySpecialInfo(request):
    vehicle = Vehicle.objects.get(user=request.user)
    if request.method == 'POST':
        form = ModifyFeatureForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('didi:home')
    form_mod = ModifyFeatureForm(
        initial={'feature': SpecialInfo.objects.filter(vehicle=vehicle)})
    form_create = SpecialInfoForm()
    context = {'form_mod':form_mod, 'form_create':form_create}
    return render(request, 'didi/special_info.html', context)

@login_required(login_url='didi:login')
def requestRide(request):
    form = RequestRideForm()
    if request.method == 'POST':
        ride = Ride(ride_owner=request.user)
        form = RequestRideForm(request.POST, instance=ride)
        if form.is_valid():
            form.save()
            return redirect('didi:home')
    context = {'form':form, }
    return render(request, 'didi/ride_request.html', context)

@login_required(login_url='didi:login')
def editRide(request, pk):
    ride = Ride.objects.get(id=pk)
    if request.method == 'POST':
        form = RequestRideForm(request.POST, instance=ride)
        if form.is_valid():
            form.save()
            return redirect('didi:home')
    form = RequestRideForm(instance=ride)
    context = {'form':form, }
    return render(request, 'didi/ride_edit.html', context)

@login_required(login_url='didi:login')
def cancelRide(request, pk):
    ride = Ride.objects.get(id=pk)
    context = {'ride':ride}
    if request.method == 'POST':
        ride.delete()
        return redirect('didi:home')
    return render(request, 'didi/ride_cancel.html', context)

@login_required(login_url='didi:login')
def ride(request, pk):
    try:
        ride = Ride.objects.get(id=pk)
        # if not UserShareRide.objects.filter(user_sharer=request.user).filter(ride=ride) and not UserDriveRide.objects.filter(user_driver__user=request.user).filter(ride=ride):
        #     return render(request, 'didi/invalid_access.html')
    except (KeyError, Ride.DoesNotExist):
        return render(request, 'didi/invalid_access.html')
    requests = SpecialInfo.objects.filter(ride=ride)
    sharers = UserShareRide.objects.filter(ride=ride)
    if ride.status == Ride.CF:
        vehicle = Vehicle.objects.get(driver_vehicle__ride=ride)
        driver = vehicle.user
    else:
        vehicle = driver = None
    context = {'ride':ride, 'requests':requests, 'sharers':sharers, 'driver':driver, 'vehicle':vehicle}
    return render(request, 'didi/ride_detail.html', context)

#search open ride
@login_required(login_url='didi:login')
def search_openride_for_sharer(request):
    form = searchOpenRideFormSharer()
    if request.method == 'POST':
        form = searchOpenRideFormSharer(request.POST)
        if form.is_valid():
            dst = form.cleaned_data.get('destination')
            user = request.user
            num = form.cleaned_data.get('owner_psger_num')
            stime = form.cleaned_data.get('earliest_arrival_time')
            etime = form.cleaned_data.get('latest_arrival_time')
            
            open_rides_result=search_ride_sharer(user, dst, num, stime, etime)

            if not open_rides_result:
                context = {'form' : form, 'sharer_open_rides' : None, 'flag' : "test"}
            else:
                context = {'form' : form, 'sharer_open_rides' : open_rides_result, 'flag' : 1}
            return render(request, 'didi/search_openride_sharer.html', context)
    context = {'form':form, }
    return render(request, 'didi/search_openride_sharer.html', context)

@login_required(login_url='didi:login')
def join_ride_sharer(request, pk, psger_num):
    try:
        ride = Ride.objects.get(id=pk)
        ride.status = Ride.SD
        if ride in Ride.objects.filter(sharer_rid__user_sharer=request.user).exclude(status=Ride.CP):
            raise Http404("You are already in this ride")
    except Ride.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
    q = UserShareRide(ride = ride, user_sharer=request.user, psger_num=psger_num)
    q.save()
    ride.save()
    return redirect('didi:home')


@login_required(login_url='didi:login')
def editShare(request, pk):
    # add constrain to limit number
    ride = Ride.objects.get(id=pk)
    share = UserShareRide.objects.filter(user_sharer=request.user).get(ride=ride)
    form = ShareEditForm(instance=share)
    if request.method == 'POST':
        form = ShareEditForm(request.POST, instance=share)
        if form.is_valid():
            cap = Vehicle.DEFAULT_CAPACITY[ride.vehicle_type]
            total_psgr_num = form.cleaned_data.get('psger_num')
            shares = UserShareRide.objects.filter(ride=ride)
            for share in shares:
                total_psgr_num += share.psger_num
            total_psgr_num += ride.owner_psger_num
            if total_psgr_num > cap :
                messages.info(request, 'Total passengers exceeding limit. ')
            else:
                form.save()
                return redirect('didi:home')
    context = {'form':form}
    return render(request, 'didi/share_edit.html', context)

@login_required(login_url='didi:login')
def cancelShare(request, pk):
    ride = Ride.objects.get(id=pk)
    context = {'ride':ride}
    if request.method == 'POST':
        share = UserShareRide.objects.filter(user_sharer=request.user).get(ride=ride)
        share.delete()
        remain = UserShareRide.objects.filter(ride=ride)
        if not remain:
            ride.status = Ride.OP
            ride.save()
        return redirect('didi:home')
    return render(request, 'didi/share_cancel.html', context)

@login_required(login_url='didi:login')
def confirm_ride_driver(request, pk):
    ride = Ride.objects.get(id=pk)
    ride.status = Ride.CF
    ride.save()
    p = UserDriveRide(ride = ride, user_driver=Vehicle.objects.get(user=request.user))
    p.save()
    sendemail(request, ride)
    return redirect('didi:home')

@login_required(login_url='didi:login')
def sendemail(request, ride):
    all_riders_email =[]
    sharer_list = UserShareRide.objects.filter(ride=ride)
    all_riders_email.append(ride.ride_owner.email)
    for person in sharer_list:
        all_riders_email.append(person.user_sharer)
    subject = "Confirmed Ride!"
    message = "Your ride to " + ride.destination + " has been confirmed!"# may need change, now just hardcode it
    from_email = request.POST.get('from_email', '')
    if subject and message:
        try:
            send_mail(subject, message, '', all_riders_email)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('didi:home')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')

@login_required(login_url='didi:login')
def search_openride_for_driver(request):
    user = request.user
    v = Vehicle.objects.get(user=request.user)
    num = v.vehicle_capacity
    feature = v.feature.all()
    open_rides_result=search_ride_driver(user, v.vehicle_capacity, v.vehicle_type, feature)
    if not open_rides_result :
        context = {'driver_open_rides' : None, 'flag' : 0}
    else:
        context = {'driver_open_rides' : open_rides_result, 'flag' : 1}
    return render(request, 'didi/search_openride_driver.html', context)

@login_required(login_url='didi:login')
def mark_complete(request, pk):
    ride = Ride.objects.get(id=pk)
    ride.status=Ride.CP
    ride.save()
    return redirect('didi:home')

@login_required(login_url='didi:login')
def get_vehicle(request, pk):
    vehicle = Vehicle.objects.get(user=User.objects.get(id=pk))
    context = {'vehicle' : vehicle, 'request' : request}
    return render(request, 'didi/vehicle_detail.html', context)

@login_required(login_url='didi:login')
def get_driver(request, pk):
    driver = User.objects.get(id=pk)
    context = {'driver' : driver, 'request' : request}
    return render(request, 'didi/driver_detail.html', context)

### ====== helper function ====== ###

#this func is for search open ride for—— sharer
def search_ride_sharer(user, dst, num, earliest_arrival_time, latest_arrival_time):
    res = []
    if dst and user and num and earliest_arrival_time and latest_arrival_time:
        rides = Ride.objects.exclude(ride_owner=user).exclude(sharer_rid__user_sharer=user).filter(destination__contains=dst).filter(arrival_time__gte=earliest_arrival_time).filter(arrival_time__lte=latest_arrival_time).filter(status__in=[Ride.OP,Ride.SD]).filter(sharable=True)
        for r in rides:
            cap = Vehicle.DEFAULT_CAPACITY[r.vehicle_type]
            total_psgr_num = num
            shares = UserShareRide.objects.filter(ride=r)
            for share in shares:
                total_psgr_num += share.psger_num
            total_psgr_num += r.owner_psger_num
            if total_psgr_num <= cap :
                res.append(r)
    else :
        raise Http404("Please input all information")
    return res

#this func is for search open ride for—— driver
def search_ride_driver(user, cap, v_type, special_req):
    res = []
    if user and cap and v_type:
        ride = Ride.objects.annotate(self_count=Count('request')).annotate(sf_match_count=Count('request', filter=Q(request__in=special_req))).filter(sf_match_count__gte=F('self_count')).exclude(ride_owner=user).filter(vehicle_type=v_type).filter(status__in=[Ride.OP,Ride.SD]) 
        for r in ride:
            total_psgr_num = 0
            shares = UserShareRide.objects.filter(ride=r)
            for share in shares:
                total_psgr_num += share.psger_num
            total_psgr_num += r.owner_psger_num
            if total_psgr_num <= cap :
                res.append(r)
    #querySet are rides
    else :
        raise Http404("Please input all infomation")
    return res