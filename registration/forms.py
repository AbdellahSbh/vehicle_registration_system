from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['number_plate', 'vehicle_type', 'owner_name', 'owner_address']
class LicensePlateLogForm(forms.Form):
    number_plate = forms.CharField(max_length=20)
    junction_id = forms.IntegerField()
