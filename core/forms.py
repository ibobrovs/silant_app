from django import forms
from .models import Maintenance, Claim

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = '__all__'