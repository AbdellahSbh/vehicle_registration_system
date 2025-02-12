import random
import string
from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['number_plate', 'vehicle_type', 'owner_name', 'owner_address']

    def clean_number_plate(self):
        number_plate = self.cleaned_data.get("number_plate")

        # ✅ Ensure correct format: "XX-999-XX (Country)"
        if not (len(number_plate) >= 7 and "-" in number_plate and "(" in number_plate and ")" in number_plate):
            raise forms.ValidationError("License plate must follow the format: XX-999-XX (Country)")

        return number_plate

    @staticmethod
    def generate_plate():
        """Generates a random European-style license plate."""
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))  # Two letters
        numbers = ''.join(random.choices(string.digits, k=3))  # Three numbers
        country = "DE"  # Default country code (Germany)
        return f"{letters}-{numbers}-{letters} ({country})"
    
class LicensePlateLogForm(forms.Form):
    number_plate = forms.CharField(max_length=20)
    junction_id = forms.IntegerField()