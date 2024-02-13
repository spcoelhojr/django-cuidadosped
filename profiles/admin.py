from django.contrib import admin
from appointment.admin import AppointmentInline, MedicNameFilterAppointment
from base.forms import UserBasicsForm
from profiles.forms import PatientForm
from profiles.models import Medic, Secretary, Patient, Relative


class PatientInline(admin.StackedInline):
    model = Patient
    extra = 0
    form = PatientForm


class MedicAdmin(admin.ModelAdmin):
    form = UserBasicsForm
    ordering = ['django_user__username']
    search_fields = ['django_user__first_name', 'django_user__last_name']

    list_display = ('django_user',)
    list_filter = ('cpf', 'rg', 'django_user__first_name',)

    fieldsets = (
        ('Usuário do Sistema', {
            'classes': ('collapse',),
            'fields': ('django_user', )
        }),
        ('Dados pessoais do médico', {
            'classes': ('collapse',),
            'fields': ('cpf', 'rg', 'birth_date', 'address', 'phone_number', 'gender', 'religion', 'race', 'nationality', 'crm', 'rqe', 'profession')
        }),

    )

    class Media:
        js = ("base/js/jquery.mask.min.js",
              "base/js/custom.mask.js")

    inlines = [AppointmentInline, ]


class SecretaryAdmin(admin.ModelAdmin):
    class Media:
        js = ("base/js/jquery.mask.min.js",
              "base/js/custom.mask.js")

    form = UserBasicsForm

    fieldsets = (
        ('Dados pessoais do secretária', {
            'classes': ('collapse',),
            'fields': ('cpf', 'rg', 'birth_date', 'address', 'phone_number', 'gender', 'religion', 'race', 'nationality')
        }),

    )

class PatientAdmin(admin.ModelAdmin):
    ordering = ['django_user__username']
    search_fields = ['django_user__first_name', 'django_user__last_name']
    list_filter = [MedicNameFilterAppointment]
    change_form_template = 'admin/profiles/patient_change_form.html'
    class Media:
        js = ("base/js/jquery.mask.min.js",
              "base/js/custom.mask.js")

    form = UserBasicsForm
    #inlines = [MedicalRecordInline, ]
    
    def relative_partner(self, obj):
        return obj.relative.partner if obj.relative else None
    relative_partner.short_description = 'Segundo Responsável'
    
    fieldsets = (
        ('Dados do Responsável', {
            'fields': ('relative','relative_partner')
        }),
        ('Dados pessoais do paciente', {
            'fields': ('birth_date', ('cpf', 'rg'), ('address', 'phone_number'), 'gender', 'religion', 'race',
                       'nationality', 'allergy', 'family_history', 'personal_history')
        }),

    )
    readonly_fields = ('relative_partner',)


class RelativeAdmin(admin.ModelAdmin):
    class Media:
        js = ("base/js/jquery.mask.min.js",
              "base/js/custom.mask.js")

    form = UserBasicsForm
    inlines = [PatientInline]


admin.site.register(Medic, MedicAdmin)
admin.site.register(Secretary, SecretaryAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Relative, RelativeAdmin)
