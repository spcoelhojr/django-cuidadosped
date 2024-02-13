from django.db import models

from base.choices import APPOINTMENT_TYPE
from base.models import Base
from base.string_texts import default_appointment
from profiles.models import Patient, Medic


class Appointment(Base):
    patient = models.ForeignKey(Patient, related_name='appointment', on_delete=models.PROTECT, verbose_name='Paciente')
    medic = models.ForeignKey(Medic, related_name='attending_medic', on_delete=models.PROTECT,
                              verbose_name='Médico Atendente')
    schedule_date = models.DateTimeField(verbose_name='Agendado para')
    next_appointment = models.DateTimeField(verbose_name='Próxima Consulta', blank=True, null=True,)
    appointment_type = models.CharField(verbose_name='Tipo da Consulta', max_length=2, choices=APPOINTMENT_TYPE)
    is_return_appointment = models.BooleanField(verbose_name='Consulta de Retorno?', default=False)

    class Meta:
        verbose_name = "Consulta Médica"
        verbose_name_plural = "Consulta Médica"
        ordering = ['-created_on']

    def __str__(self):
        return '{} - {} - {}'.format(self.schedule_date.strftime("%d/%m/%Y"), self.patient, self.medic)


class MedicalRecord(Base):
    appointment = models.ForeignKey('Appointment', related_name='medicalrecord', on_delete=models.PROTECT,
                                    verbose_name='Consulta')
    pc = models.FloatField(verbose_name='Perímetro Encefálico(PC)', blank=True, null=True)
    pt = models.FloatField(verbose_name='Perímetro Toráxico(PT)', blank=True, null=True)
    height = models.FloatField(verbose_name='Altura cm', blank=True, null=True)
    weight = models.FloatField(verbose_name='Peso Kg', blank=True, null=True)
    current_disease = models.TextField(verbose_name='História Doença Atual', blank=True, null=True)
    physical_exam = models.TextField(verbose_name='Exame Físico', default=default_appointment, blank=True,
                                     null=True)
    diagnose_hypothesis = models.TextField(verbose_name='Hipótese Diagnóstica', blank=True, null=True)
    conduct = models.TextField(verbose_name='Conduta', blank=True, null=True)

    class Meta:
        verbose_name = "Prontuário"
        verbose_name_plural = "Prontuários"
        ordering = ['-created_on']

    def __str__(self):
        return 'PC: {}cm, PT: {}cm, Altura: {}cm, Peso: {}kg'.format(self.pc, self.pt, self.height, self.weight)
