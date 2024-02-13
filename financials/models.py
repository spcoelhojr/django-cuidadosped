from django.db import models
from base.choices import PAYMENT_TYPE
from base.models import Base
from appointment.models import Appointment
from djmoney.models.fields import MoneyField


class AppointmentFinancials(Base):
    appointment = models.ForeignKey(Appointment, related_name='financials', on_delete=models.PROTECT, verbose_name='Consulta')
    payment_type = models.CharField(verbose_name='Tipo de Pagamento', max_length=1, choices=PAYMENT_TYPE, default='D')
    price = MoneyField(verbose_name='Preço', max_digits=9, decimal_places=2, default_currency='BRL')
    payment_proof = models.FileField(verbose_name='Comprovante de Pagamento', upload_to='payment_proofs/', blank=True, null=True)
    invoice = models.FileField(verbose_name='Nota fiscal', upload_to='notas_fiscais/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Finança"
        verbose_name_plural = "Finanças"
        ordering = ['-created_on']
        
    def __str__(self):
        return '{} - {}'.format(self.appointment, self.price)