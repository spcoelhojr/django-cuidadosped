from django.contrib import admin
from datetime import datetime, timedelta
from appointment.forms import AppointmentForm, MedicalRecordForm
from appointment.models import Appointment, MedicalRecord
from financials.admin import AppointmentFinancialsInline
from django.utils import timezone
from django.db.models import Q


class MedicNameFilter(admin.SimpleListFilter):
    title = 'Médico'
    parameter_name = 'medic_name'

    def lookups(self, request, model_admin):
        medic_names = set()
        for medical_record in model_admin.model.objects.all().select_related('appointment__medic__django_user'):
            medic = medical_record.appointment.medic.django_user
            full_name = f'{medic.first_name} {medic.last_name}'.strip()
            medic_names.add((full_name, full_name))
        return sorted(medic_names)

    def queryset(self, request, queryset):
        if self.value():
            name_parts = self.value().split()
            queries = []
            if name_parts:
                # Create queries for first and last name
                first_name_query = Q(appointment__medic__django_user__first_name__icontains=name_parts[0])
                last_name_query = Q(appointment__medic__django_user__last_name__icontains=name_parts[-1])

                # Combine queries
                queries.append(first_name_query)
                if len(name_parts) > 1:
                    queries.append(last_name_query)

            # Apply filters
            if queries:
                query = queries.pop()
                for item in queries:
                    query |= item
                return queryset.filter(query)

        return queryset

class MedicNameFilterAppointment(admin.SimpleListFilter):
    title = 'Médico'
    parameter_name = 'medic_name'

    def lookups(self, request, model_admin):
        medic_names = set()
        for appointment in model_admin.model.objects.all().select_related('medic__django_user'):
            medic = appointment.medic.django_user
            full_name = f'{medic.first_name} {medic.last_name}'.strip()
            medic_names.add((full_name, full_name))
        return sorted(medic_names)

    def queryset(self, request, queryset):
        if self.value():
            name_parts = self.value().split()
            queries = []
            if name_parts:
                # Create queries for first and last name
                first_name_query = Q(medic__django_user__first_name__icontains=name_parts[0])
                last_name_query = Q(medic__django_user__last_name__icontains=name_parts[-1])

                # Combine queries
                queries.append(first_name_query)
                if len(name_parts) > 1:
                    queries.append(last_name_query)

            # Apply filters
            if queries:
                query = queries.pop()
                for item in queries:
                    query |= item
                return queryset.filter(query)

        return queryset


class TodayAppointmentsFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the right admin sidebar
    title = 'Consultas de hoje'

    # Parameter for the filter that will be used in the URL query
    parameter_name = 'schedule_date'

    def lookups(self, request, model_admin):
        # This is where you define the filter options; in this case, it's only one option
        return (
            ('today', 'Hoje'),
            ('this_week', 'Essa semana'),
            ('rest_of_week', 'Restante da semana'),
            ('current_month', 'Mês Atual')
        )
    def queryset(self, request, queryset):
        today = timezone.localdate()

        if self.value() == 'today':
            start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
            end_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))
            return queryset.filter(schedule_date__range=(start_of_day, end_of_day))

        elif self.value() == 'this_week':
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            start_of_week = timezone.make_aware(timezone.datetime.combine(start_of_week, timezone.datetime.min.time()))
            end_of_week = timezone.make_aware(timezone.datetime.combine(end_of_week, timezone.datetime.max.time()))
            return queryset.filter(schedule_date__range=(start_of_week, end_of_week))

        elif self.value() == 'rest_of_week':
            tomorrow = today + timedelta(days=1)
            end_of_week = today + timedelta(days=6 - today.weekday())
            start_of_tomorrow = timezone.make_aware(timezone.datetime.combine(tomorrow, timezone.datetime.min.time()))
            end_of_week = timezone.make_aware(timezone.datetime.combine(end_of_week, timezone.datetime.max.time()))
            return queryset.filter(schedule_date__range=(start_of_tomorrow, end_of_week))
        
        elif self.value() == 'current_month':
            month = today.month
            
            return queryset.filter(schedule_date__month=month)
        return queryset

class AppointmentInline(admin.TabularInline):
    model = Appointment
    form = AppointmentForm
    extra = 0
    
    def get_queryset(self, request):
        # Get the current date
        today = timezone.localdate()
        
        start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        end_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))

        # Filter appointments to only include today's appointments
        qs = super().get_queryset(request)
        return qs.filter(schedule_date__range=(start_of_day, end_of_day))


class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment
    form = AppointmentForm

    list_display = ('get_medic', 'get_patient', 'get_relative', 'schedule_date', 'is_return_appointment')
    list_filter = (TodayAppointmentsFilter, MedicNameFilterAppointment,)
    search_fields = ('medic__django_user__first_name','patient__django_user__first_name','patient__django_user__last_name', )
    autocomplete_fields = ['medic', 'patient']
    ordering = ('schedule_date',)
    inlines = (AppointmentFinancialsInline,)
    fieldsets = (
        (None, {
            'fields': ('patient', 'medic')
        }),
        ('Consulta', {
            'classes': ('wide', ),
            'fields': ('schedule_date', 'next_appointment', 'appointment_type', 'is_return_appointment'),
        }),
    )

    def get_medic(self, obj):
        return f"{obj.medic.django_user.first_name} {obj.medic.django_user.last_name}"
    get_medic.short_description = 'Médico'

    def get_patient(self, obj):
        return f"{obj.patient.django_user.first_name} {obj.patient.django_user.last_name}"
    get_patient.short_description = 'Paciente'
    
    def get_relative(self, obj):
        return f"{obj.patient.relative.django_user.first_name} {obj.patient.relative.django_user.last_name}"
    get_relative.short_description = 'Responsável'

class MedicalRecordAdmin(admin.ModelAdmin):
    model = MedicalRecord
    form = MedicalRecordForm

    list_display = ('appointment',)
    list_filter = (MedicNameFilter, 'appointment__patient')
    search_fields = ('appointment__patient__django_user__first_name', 'appointment__patient__django_user__last_name')
    ordering = ('appointment__schedule_date',)
    fieldsets = (
        ('Consulta', {
            'fields': ('appointment', ),
        }),
        ('Avaliação', {
            'fields': (('pc', 'pt',), ('height', 'weight'), 'current_disease', 'physical_exam', 'diagnose_hypothesis', 'conduct'),
        }),
    )

    def get_medic(self, obj):
        return f"{obj.appointment.medic.django_user.first_name} {obj.appointment.medic.django_user.last_name}"
    get_medic.short_description = 'Médico'

    def get_patient(self, obj):
        return f"{obj.appointment.patient.django_user.first_name} {obj.appointment.patient.django_user.last_name}"
    get_patient.short_description = 'Paciente'

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
