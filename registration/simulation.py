import random
import time
from registration.models import Vehicle, Junction, LicensePlateLog, Violation
from .views import send_violation_email

def generate_unique_plate():
    """Generates a random EU-style license plate"""
    letters = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2))
    numbers = ''.join(random.choices("0123456789", k=3))
    country = "DE"  # Germany as default
    return f"{letters}-{numbers}-{letters} ({country})"

def create_simulated_cars(num=10):
    """Creates and registers random vehicles"""
    for _ in range(num):
        plate = generate_unique_plate()
        vehicle = Vehicle.objects.create(
            number_plate=plate,
            vehicle_type=random.choice(["Car", "Motorcycle", "Truck"]),
            owner_name=f"Driver {_+1}",
            owner_address="Unknown",
            city="Simulated City"
        )
        print(f"🚗 Created Vehicle: {vehicle}")

def simulate_junction_crossing():
    """Simulates vehicles passing junctions, sometimes causing violations"""
    vehicles = list(Vehicle.objects.all())
    junctions = list(Junction.objects.all())

    if not vehicles or not junctions:
        print("❌ No vehicles or junctions available for simulation.")
        return

    for vehicle in vehicles:
        junction = random.choice(junctions)  # Pick a random junction
        log_entry = LicensePlateLog.objects.create(vehicle=vehicle, junction=junction)

        if vehicle.vehicle_type == "emergency":
            print(f"🚨 Emergency vehicle {vehicle.number_plate} passed through {junction.name}.")
            continue

        if random.choice([True, False]):  # 50% chance of violation
            violation_type = random.choice(Violation.objects.all())  # Pick a random violation
            log_entry.violation = violation_type
            log_entry.save()
            print(f"⚠️ Violation: {vehicle.number_plate} committed {violation_type}")

        else:
            print(f"✅ {vehicle.number_plate} passed safely through {junction.name}")

def run_simulation():
    """Runs a full simulation"""
    print("\n🚦 Starting Traffic Simulation 🚦\n")
    create_simulated_cars(num=10)  # Create 10 random vehicles
    time.sleep(2)  # Pause for realism
    simulate_junction_crossing()
    print("\n✅ Simulation Complete!\n")
