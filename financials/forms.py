from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms

from base.choices import PAYMENT_TYPE
from .models import AppointmentFinancials
from django.contrib.admin.widgets import AdminDateWidget

class AppointmentFinancialsForm(ModelForm):
    def clean_payment_proof(self):
        file = self.cleaned_data.get('payment_proof', False)
        if file:
            if not file.content_type in ['application/pdf', 'image/jpeg', 'image/png']:
                raise ValidationError("Apenas formatos pdf, jpeg ou png")
        return file
    
    def clean_invoice(self):
        file = self.cleaned_data.get('invoice', False)
        if file:
            if not file.content_type in ['application/pdf', 'image/jpeg', 'image/png']:
                raise ValidationError("Apenas formatos pdf, jpeg ou png")
        return file
    
    def clean_price(self):
        price = self.cleaned_data.get('price', False)
        if price.amount < 0:
            raise ValidationError("Preço da consulta não pode ser menor que ZERO")
        return price
    
    # def __init__(self, *args, **kwargs):
    #     super(AppointmentFinancialsForm, self).__init__(*args, **kwargs)
    #     for field in ['price',]:
    #         self.fields[field].widget.attrs['class'] = f'mask-{field}'
    
    class Meta:
        exclude = ['deleted', 'enabled']
        model = AppointmentFinancials
        

class ReportFilterForm(forms.Form):
    start_date = forms.DateField(required=False, label="Data Inicial", widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, label="Data Final", widget=forms.DateInput(attrs={'type': 'date'}))
    payment_type = forms.ChoiceField(choices=PAYMENT_TYPE, required=False, label="Tipo de Pagamento")
    all_payment_types = forms.BooleanField(required=False, label="Incluir Todos os Tipos de Pagamento")


class DateRangeForm(forms.Form):
    created_on__gte = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label='Start Date')
    created_on__lt = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label='End Date')
