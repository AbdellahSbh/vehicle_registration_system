from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Vehicle, LicensePlateLog, Junction, City, Violation
from .forms import VehicleForm
from django.contrib import messages
import logging
import random
from django.utils.timezone import now
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse


logger = logging.getLogger(__name__)

def register_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save()

            # Send vehicle data to WebSocket for simulation
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "vehicle_simulation",
                {
                    "type": "new_vehicle",
                    "vehicle_id": vehicle.id,
                    "number_plate": vehicle.number_plate,
                    "vehicle_type": vehicle.vehicle_type,
                    "city": vehicle.city,
                    "lat": random.uniform(51.0, 52.0),  # Random starting latitude
                    "lng": random.uniform(10.0, 11.0)  # Random starting longitude
                }
            )

            messages.success(request, f"✅ Vehicle {vehicle.number_plate} registered successfully and added to the road!")
            return redirect("register_vehicle")
        else:
            messages.error(request, "❌ Registration failed. Please check the input.")
    
    else:
        form = VehicleForm()
    
    return render(request, "registration/register_vehicle.html", {"form": form})



def log_plate(request):
    junctions = Junction.objects.all()
    violations = Violation.objects.all()  

    if request.method == "POST":
        number_plate = request.POST.get("number_plate")
        junction_id = request.POST.get("junction_id")
        violation_id = request.POST.get("violation_type")

        try:
            vehicle = Vehicle.objects.get(number_plate=number_plate)
            junction = Junction.objects.get(id=junction_id)
            violation = Violation.objects.get(id=violation_id)


            LicensePlateLog.objects.create(vehicle=vehicle, junction=junction, violation=violation)

            return HttpResponse("✅ Plate Logged Successfully")

        except Vehicle.DoesNotExist:
            return HttpResponse("❌ Vehicle not registered")
        except Junction.DoesNotExist:
            return HttpResponse("❌ Invalid junction selected")
        except Violation.DoesNotExist:
            return HttpResponse("❌ Invalid violation selected")

    return render(request, "registration/log_plate.html", {"junctions": junctions, "violations": violations})


def vehicle_list(request):
    query = request.GET.get("search")
    if query:
        vehicles = Vehicle.objects.filter(number_plate__icontains=query)
    else:
        vehicles = Vehicle.objects.all()  

    return render(request, "registration/vehicle_list.html", {"vehicles": vehicles, "query": query})

def dashboard(request):
    return render(request, "registration/dashboard.html")

def violation_list(request):
    violations = Violation.objects.all()  
    return render(request, "registration/violation_list.html", {"violations": violations})

def license_plate_logs(request):
    logs = LicensePlateLog.objects.all().order_by("-timestamp")  
    return render(request, "registration/license_plate_logs.html", {"logs": logs})

def simulation_view(request):
    return render(request, "registration/simulation.html")

def setup_initial_data():
    city, created = City.objects.get_or_create(name="Default City")

    junction_names = [
        "Downtown", "Highway Exit", "Airport Access", "City Center",
        "Train Station", "Shopping District", "University Road", "Industrial Zone"
    ]

    for name in junction_names:
        if not Junction.objects.filter(name=name).exists():
            Junction.objects.create(name=name, City=city.name) 


def log_vehicle_violation(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)

        plate = data.get("number_plate")
        junction_name = data.get("junction")

        try:
            vehicle = Vehicle.objects.get(number_plate=plate)
            junction = Junction.objects.get(name=junction_name)

            # ✅ 50% chance of getting a violation
            violation = None
            if random.choice([True, False]):
                violation = random.choice(Violation.objects.all())

            log_entry = LicensePlateLog.objects.create(
                vehicle=vehicle,
                junction=junction,
                violation=violation if violation else None,
                timestamp=now()
            )

            return JsonResponse({
                "message": "✅ Log recorded",
                "number_plate": vehicle.number_plate,
                "junction": junction.name,
                "violation": violation.violation_type if violation else "No Violation",
                "fine": violation.fine_amount if violation else 0,
                "timestamp": log_entry.timestamp.strftime("%b %d, %Y, %I:%M %p")
            })

        except Vehicle.DoesNotExist:
            return JsonResponse({"error": "❌ Vehicle not registered"}, status=400)
        except Junction.DoesNotExist:
            return JsonResponse({"error": "❌ Invalid junction"}, status=400)

    return JsonResponse({"error": "❌ Invalid request"}, status=400)

def log_violation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        number_plate = data.get("number_plate")
        junction_name = data.get("junction")

        try:
            vehicle = Vehicle.objects.get(number_plate=number_plate)
            junction = Junction.objects.get(name=junction_name)
            
            # Assign a violation randomly or based on a rule
            violation = Violation.objects.order_by("?").first()

            LicensePlateLog.objects.create(vehicle=vehicle, junction=junction, violation=violation)

            return JsonResponse({"status": "success", "message": f"Violation logged at {junction_name} for {number_plate}"})
        
        except Vehicle.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Vehicle not found"})
        except Junction.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Junction not found"})

    return JsonResponse({"status": "error", "message": "Invalid request"})


def get_registered_vehicles(request):
    vehicles = list(Vehicle.objects.values("number_plate"))
    return JsonResponse({"vehicles": vehicles})
