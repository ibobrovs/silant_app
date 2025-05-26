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
        fields = '__all__'