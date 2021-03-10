from django.urls import path

from . import views

app_name = 'didi'
urlpatterns = [
    path('', views.userHomePage, name='default'),
    path('register/', views.userRegister, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('home/', views.userHomePage, name='home'),
    path('edit_personal/', views.userEdit, name='edit_personal'),
    path('reset_password/', views.resetPassword, name='reset_password'),
    path('driver_register/', views.driverRegister, name='driver_register'),
    path('driver_unregister/', views.driverUnregister, name='driver_unregister'),
    path('driver_update/', views.driverUpdate, name='driver_update'),
    path('si_create/', views.createSpecialInfo, name='si_create'),
    path('si_modify/', views.modifySpecialInfo, name='si_modify'),
    path('ride_request/', views.requestRide, name='ride_request'),
    path('ride_edit/<str:pk>/', views.editRide, name='ride_edit'),
    path('ride_cancel/<str:pk>/', views.cancelRide, name='ride_cancel'),
    path('share_edit/<str:pk>/', views.editShare, name='share_edit'),
    path('share_cancel/<str:pk>/', views.cancelShare, name='share_cancel'),
    path('ride_detail/<str:pk>/', views.ride, name='ride'),
    path('search_openride_sharer/', views.search_openride_for_sharer, name='search_openride_sharer'),
    path('search_openride_driver/', views.search_openride_for_driver, name='search_openride_driver'),
    path('join_ride_sharer/<str:pk>/<int:psger_num>', views.join_ride_sharer, name='join_ride_sharer'),
    path('confirm_ride_driver/<str:pk>/', views.confirm_ride_driver, name= 'confirm_ride_driver'),
    path('vehicle_detail/<str:pk>/', views.get_vehicle, name='vehicle_detail'),
    path('mark_complete/<str:pk>', views.mark_complete, name='mark_complete'),
]