from django.shortcuts import render, redirect
from .models import Vehicle
from django.http import HttpResponse
from .forms import VehicleForm
from .forms import LicensePlateLogForm, VehicleForm
from .models import LicensePlateLog, Vehicle, Junction

def register_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("register_vehicle")  # Redirect to the same page after successful registration
    else:
        form = VehicleForm()

    return render(request, "registration/register_vehicle.html", {"form": form})

def log_plate(request):
    junctions = Junction.objects.all() 
    if request.method == "POST":
        number_plate = request.POST.get("number_plate")
        junction_id = request.POST.get("junction_id")  

        try:
            vehicle = Vehicle.objects.get(number_plate=number_plate)
            junction = Junction.objects.get(id=junction_id)


            LicensePlateLog.objects.create(vehicle=vehicle, junction=junction)
            return HttpResponse("Plate Logged Successfully")

        except Vehicle.DoesNotExist:
            return HttpResponse("❌ Vehicle not registered")
        except Junction.DoesNotExist:
            return HttpResponse("❌ Invalid junction selected")

    return render(request, "registration/log_plate.html", {"junctions": junctions})


def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, "registration/vehicle_list.html", {"vehicles": vehicles})

def dashboard(request):
    return render(request, "registration/dashboard.html")

def license_plate_logs(request):
    logs = LicensePlateLog.objects.all().order_by("-timestamp")  
    return render(request, "registration/license_plate_logs.html", {"logs": logs})

def vehicle_list(request):
    query = request.GET.get("search")
    if query:
        vehicles = Vehicle.objects.filter(number_plate__icontains=query)
    else:
        vehicles = Vehicle.objects.all()
    return render(request, "registration/vehicle_list.html", {"vehicles": vehicles, "query": query})


def setup_initial_data():
    from registration.models import City, Junction

    # Ensure there is at least one city
    city, created = City.objects.get_or_create(name="Default City")  # ✅ Assign default city

    # Ensure junctions exist and are linked to a city
    junction_names = [
        "Downtown", "Highway Exit", "Airport Access", "City Center",
        "Train Station", "Shopping District", "University Road", "Industrial Zone"
    ]
    
    for name in junction_names:
        if not Junction.objects.filter(name=name).exists():
            Junction.objects.create(name=name, location="General Area", city=city)  # ✅ Assign city

setup_initial_data()

  # Runs when the server starts


