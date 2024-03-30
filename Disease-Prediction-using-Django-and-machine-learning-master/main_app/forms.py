from django import forms
from .models import PatientInfo

class PatientInfoForm(forms.ModelForm):
    class Meta:
        model = PatientInfo
        exclude = []

    # Add any custom form validations if needed
