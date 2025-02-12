from django.contrib import admin
from .models import Vehicle, Junction, LicensePlateLog,Violation

class VehicleAdmin(admin.ModelAdmin):
    list_display = ("number_plate", "vehicle_type", "owner_name", "owner_address")  # Columns in admin panel
    search_fields = ("number_plate", "owner_name")  # Search bar for quick access

class LicensePlateLogAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "junction", "timestamp")
    list_filter = ("timestamp", "junction")


class JunctionAdmin(admin.ModelAdmin):
    list_display = ("name", "city")

admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Junction)
admin.site.register(LicensePlateLog, LicensePlateLogAdmin)
admin.site.register(Violation)
