from base.forms import UserBasicsForm
from .models import Medic, Relative, Patient, Secretary


class MedicForm(UserBasicsForm):
    class Meta:
        model = Medic
        exclude = ['deleted', 'enabled']


class RelativeForm(UserBasicsForm):
    class Meta:
        model = Relative
        exclude = ['deleted', 'enabled']


class PatientForm(UserBasicsForm):
    class Meta:
        model = Patient
        exclude = ['deleted', 'enabled']


class SecretaryForm(UserBasicsForm):
    class Meta:
        model = Secretary
        exclude = ['deleted', 'enabled']
