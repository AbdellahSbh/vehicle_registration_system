from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Vehicle, LicensePlateLog, Junction, City, Violation
from .forms import VehicleForm
from django.contrib import messages
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def register_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Vehicle registered successfully!")  
            return redirect("register_vehicle")  
        else:
            logger.error(f"❌ Form Errors: {form.errors}")  
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


            vehicle_detection = LicensePlateLog.objects.create(vehicle=vehicle, junction=junction, violation=violation)
            # if violation and violation.type != "No Violation":
            send_violation_email(vehicle_detection)

            return HttpResponse("✅ Plate Logged Successfully")

        except Vehicle.DoesNotExist:
            return HttpResponse("❌ Vehicle not registered")
        except Junction.DoesNotExist:
            return HttpResponse("❌ Invalid junction selected")
        except Violation.DoesNotExist:
            return HttpResponse("❌ Invalid violation selected")

    return render(request, "registration/log_plate.html", {"junctions": junctions, "violations": violations})

def send_violation_email(vehicle_detection):
    subject = "Traffic Violation Notice"
    vehicle = vehicle_detection.vehicle
    violation = vehicle_detection.violation
    recipient_email = "" #owner_email

    message = f"""
    Dear {vehicle.owner_name},

    Your vehicle ({vehicle.number_plate}) was detected at {vehicle_detection.junction} on {vehicle_detection.timestamp}.
    
    Violation: {violation.type}
    Fine Amount: ${violation.fine_amount}

    Regards,
    Traffic Management
    """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [recipient_email],
        fail_silently=False
    )

def vehicle_list(request):
    query = request.GET.get("search")
    if query:
        vehicles = Vehicle.objects.filter(number_plate__icontains=query)
    else:
        vehicles = Vehicle.objects.all()  

    return render(request, "registration/vehicle_list.html", {"vehicles": vehicles, "query": query})

def dashboard(request):
    return render(request, "registration/dashboard.html")

def license_plate_logs(request):
    logs = LicensePlateLog.objects.all().order_by("-timestamp")  
    return render(request, "registration/license_plate_logs.html", {"logs": logs})



def setup_initial_data():
    city, created = City.objects.get_or_create(name="Default City")

    junction_names = [
        "Downtown", "Highway Exit", "Airport Access", "City Center",
        "Train Station", "Shopping District", "University Road", "Industrial Zone"
    ]

    for name in junction_names:
        if not Junction.objects.filter(name=name).exists():
            Junction.objects.create(name=name, City=city.name) 
