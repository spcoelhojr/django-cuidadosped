from datetime import date
from django.contrib.auth.models import User
from django.db import models
from base.choices import RELATIVE
from base.date_functions import age_to_str, age
from base.models import Base, UserCommons


class Medic(UserCommons):
    crm = models.CharField(verbose_name='CRM nº', max_length=11, unique=True)
    rqe = models.CharField(verbose_name='RQE nº', max_length=11, unique=True)
    # highlighted = models.TextField()

    class Meta:
        verbose_name = "Médico(a)"
        verbose_name_plural = "Médicos"
        ordering = ['-created_on']

    def __str__(self):
        return '{} {}'.format(self.django_user.first_name, self.django_user.last_name)


class Secretary(UserCommons):
    enter_date = models.DateField(verbose_name='Data de entrada', default=date.today)
    exit_date = models.DateField(verbose_name='Data de saída', blank=True, null=True)

    class Meta:
        verbose_name = "Secretária"
        verbose_name_plural = "Secretárias"

    def __str__(self):
        return '{} {}'.format(self.django_user.first_name, self.django_user.last_name)


class Relative(UserCommons):
    relationship = models.CharField(verbose_name='Grau de Parentesco', max_length=1, choices=RELATIVE)
    partner = models.ForeignKey('self', verbose_name='Cônjuge', blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.django_user.first_name, self.django_user.last_name)

    class Meta:
        verbose_name_plural = "Responsáveis"
        verbose_name = "Responsável"


class Patient(UserCommons):
    medic = models.ForeignKey('Medic', related_name='patients', verbose_name='Médico(a)', on_delete=models.PROTECT)
    relative = models.ForeignKey('Relative', related_name='relatives', verbose_name='Responsável',
                                   on_delete=models.PROTECT)
    allergy = models.TextField(verbose_name='Alergias', blank=True, null=True)
    family_history = models.TextField(verbose_name='História Familiar', blank=True, null=True)
    personal_history = models.TextField(verbose_name='História Pessoal', blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.django_user.first_name, self.django_user.last_name)

    class Meta:
        verbose_name_plural = "Pacientes"
        verbose_name = "Paciente"

    def age(self):
        return age(self.birth_date)

    def age_to_str(self):
        return age_to_str(age(self.birth_date))
