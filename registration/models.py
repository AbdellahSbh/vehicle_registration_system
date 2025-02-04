from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Junction(models.Model):
    name = models.CharField(max_length=255)
    City= models.CharField(max_length=255)


    def __str__(self):
       return f"{self.name} ({self.City})"

class Vehicle(models.Model):
    number_plate = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=100)
    owner_address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.number_plate} - {self.vehicle_type}"

class LicensePlateLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    junction = models.ForeignKey(Junction, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.number_plate} at {self.junction.name} on {self.timestamp}"
