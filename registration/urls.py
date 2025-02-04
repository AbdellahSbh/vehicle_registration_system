from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register_vehicle/", views.register_vehicle, name="register_vehicle"),
    path("log_plate/", views.log_plate, name="log_plate"),
    path("vehicles/", views.vehicle_list, name="vehicle_list"),
    path("logs/", views.license_plate_logs, name="license_plate_logs"), 
]



