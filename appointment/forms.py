from django.forms import ModelForm
from .models import Appointment, MedicalRecord


class AppointmentForm(ModelForm):
    class Meta:
        exclude = ['deleted', 'enabled']
        model = Appointment


class MedicalRecordForm(ModelForm):
    class Meta:
        exclude = ['deleted', 'enabled']
        model = MedicalRecord