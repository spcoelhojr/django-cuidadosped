import datetime
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, TextInput
from profiles.models import Medic, Secretary, Patient, Relative
from .models import UserCommons
from validate_docbr import CPF
import re

class UserBasicsForm(ModelForm):
    rg = CharField(required=False, label='RG', widget=TextInput(attrs={'type': 'number'}))

    def clean_cpf(self):
        data = self.cleaned_data['cpf']
        cpf = CPF()
        cpf.repeated_digits = False

        if not cpf.validate(data):
            raise ValidationError("CPF digitado não é válido")

        # Models to check for uniqueness
        models_to_check = [Medic, Secretary, Patient, Relative]

        # Check each model
        for model in models_to_check:
            # If updating an existing instance, exclude it from the check
            query = model.objects.filter(cpf=data)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)

            if query.exists():
                raise ValidationError("Usuário com esse CPF já cadastrado")

        return data

    def clean_birth_date(self):
        data = self.cleaned_data['birth_date']

        if data and data > datetime.date.today():
            raise ValidationError("Data de nascimento não pode ser maior que a data de hoje")

        return data

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        
        cleaned_phone_number = re.sub(r'\D', '', data)
        if len(cleaned_phone_number) > 11 :  # Assuming a minimum length
            raise ValidationError("Número de telefone inválido")
        return cleaned_phone_number
    
    def __init__(self, *args, **kwargs):
        super(UserBasicsForm, self).__init__(*args, **kwargs)
        for field in ['phone_number', 'cpf']:
            self.fields[field].widget.attrs['class'] = f'mask-{field}'

    class Meta:
        exclude = ['deleted', 'enabled']
        model = UserCommons