import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from registration.models import Vehicle

class VehicleSimulationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("vehicle_simulation", self.channel_name)
        await self.send_existing_vehicles()

    async def send_existing_vehicles(self):
        vehicles = list(Vehicle.objects.all())  # Get all registered vehicles
        for vehicle in vehicles:
            await self.send(text_data=json.dumps({
                "id": vehicle.id,
                "number_plate": vehicle.number_plate,
                "lat": 51.1657 + (random.random() - 0.01),  # Small variation
                "lng": 10.4515 + (random.random() - 0.01),
                "violation": random.choice([True, False])  # Random violation
            }))

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "new_vehicle":
            await self.send(text_data=json.dumps({
                "id": data["vehicle_id"],
                "number_plate": data["number_plate"],
                "lat": data["lat"],
                "lng": data["lng"],
                "violation": random.choice([True, False])  # Assign a random violation
            }))
