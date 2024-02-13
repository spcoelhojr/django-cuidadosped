from django.contrib.auth.models import User
from django.db import models
from base.choices import GENDER, RACE


class Base(models.Model):
    enabled = models.BooleanField('Ativo', default=True)
    deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['pk']

    def __str__(self):
        return '%s' % self.updated_on


class UserCommons(Base):
    django_user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='Usuário',)
    cpf = models.CharField(verbose_name='CPF', max_length=11, blank=True, null=True, help_text='Apenas Números')
    rg = models.CharField(verbose_name='RG', max_length=20, blank=True, null=True)
    birth_date = models.DateField(verbose_name='Nascimento', blank=True, null=True)
    profession = models.CharField(verbose_name='Profissão', max_length=255, blank=True, null=True)
    address = models.CharField(verbose_name='Endereço', max_length=255, blank=True, null=True)
    phone_number = models.CharField(verbose_name='Telefone', max_length=11, blank=True, null=True, help_text='Apenas Números')
    gender = models.CharField(verbose_name='Sexo', max_length=1, choices=GENDER, blank=True, null=True)
    religion = models.CharField(verbose_name='Religião', max_length=30, blank=True, null=True, default='Católica')
    race = models.CharField(verbose_name='Cor/Raça/Etnia', max_length=2, choices=RACE, blank=True, null=True)
    nationality = models.CharField(verbose_name='Nacionalidade', max_length=30, default='Brasileiro(a)',
                                   blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['pk']

    def __str__(self):
        return '%s' % self.django_user
