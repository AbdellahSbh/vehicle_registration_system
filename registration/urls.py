from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register_vehicle/", views.register_vehicle, name="register_vehicle"),
    path("log_plate/", views.log_plate, name="log_plate"),
    path("vehicles/", views.vehicle_list, name="vehicle_list"),
    path("logs/", views.license_plate_logs, name="license_plate_logs"), 
    path("simulation/" , views.simulation_view, name="simulation_view"),
    path('violations/', views.violation_list, name='violation_list'),
    path("simulation/", views.simulation_view, name="simulation"),
    path("log_vehicle/", views.log_vehicle_violation, name="log_vehicle_violation"),
    path("log_violation/", views.log_violation, name="log_violation"),
    path("get_registered_vehicles/", views.get_registered_vehicles, name="get_registered_vehicles"),
    path("junction_count/", views.junction_count, name="junction_count"),



]



