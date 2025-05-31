from django import forms
from .models import Maintenance, Claim, Machine

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = '__all__'

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = [
            'serial_number',
            'model',
            'engine_model',
            'engine_serial',
            'transmission_model',
            'transmission_serial',
            'drive_axle_model',
            'drive_axle_serial',
            'steered_axle_model',
            'steered_axle_serial',
            'supply_contract',
            'shipment_date',
            'customer',
            'location',
            'additional_equipment',
            'client',
            'service_company',
        ]
        widgets = {
            'shipment_date': forms.DateInput(attrs={'type': 'date'}),
            'additional_equipment': forms.Textarea(attrs={'rows': 4}),
        }
