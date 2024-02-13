from asyncio import format_helpers
from django.contrib import admin
from base.choices import PAYMENT_TYPE

from financials.forms import AppointmentFinancialsForm, DateRangeForm
from .models import AppointmentFinancials
from django.http import HttpResponse
import csv
from .views import report_view
from django.urls import path
from django.db.models import Sum

from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from datetime import datetime, timedelta

class DateRangeFilter(SimpleListFilter):
    title = 'Date Range'
    parameter_name = 'date_range'
    template = 'admin/financials/date_range_filter.html'
    

    def lookups(self, request, model_admin):
        return (
            ('custom', 'Custom Range'),
        )
    def queryset(self, request, queryset):
        form = DateRangeForm(request.GET or None)
        if form.is_valid():
            start_date = form.cleaned_data.get('created_on__gte')
            end_date = form.cleaned_data.get('created_on__lt')

            if start_date:
                # Combine with minimum time and make timezone-aware
                start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))

            if end_date:
                # Combine with maximum time and make timezone-aware
                end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))

            if start_date and end_date:
                queryset = queryset.filter(created_on__range=(start_date, end_date))
            elif start_date:
                queryset = queryset.filter(created_on__gte=start_date)
            elif end_date:
                queryset = queryset.filter(created_on__lt=end_date)

        return queryset
    
def export_financials_report(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="financials_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Payment Type', 'Appointment', 'Price', 'Date'])

    total_sum = 0
    for payment_type, name in PAYMENT_TYPE:
        filtered_qs = queryset.filter(payment_type=payment_type)
        sum_for_type = filtered_qs.aggregate(total=Sum('price'))['total']
        total_sum += sum_for_type if sum_for_type else 0

        writer.writerow([name])
        for financial in filtered_qs:
            writer.writerow(['', financial.appointment, financial.price, financial.created_on])

        writer.writerow(['', 'Total for ' + name, sum_for_type, ''])
        writer.writerow([])  # Blank row for separation

    writer.writerow(['', 'Grand Total', total_sum, ''])
    return response

export_financials_report.short_description = 'Relatório dos selecionados'

class AppointmentFinancialsInline(admin.StackedInline):
    model = AppointmentFinancials
    extra = 1
    form = AppointmentFinancialsForm

class AppointmentFinancialsAdmin(admin.ModelAdmin):
    model = AppointmentFinancials
    form = AppointmentFinancialsForm
    actions = [export_financials_report]
    list_display = ['get_patient', 'payment_proof_link', 'invoice_link']
    list_filter = [DateRangeFilter,]
    search_fields = ('appointment__patient__django_user__first_name', 'appointment__patient__django_user__last_name', 'created_on')
    ordering = ('appointment__schedule_date',)
    
    fieldsets = (
        ('Consulta', {
            "fields": (
                'appointment',
            ),
        }),
        ( 'Financeiro', {
            "fields": (
                'payment_type', 'price', 'invoice', 'payment_proof'
            ),
        }),
    )
    
    def get_patient(self, obj):
        return f"{obj.appointment.patient.django_user.first_name} {obj.appointment.patient.django_user.last_name}"
    get_patient.short_description = 'Paciente'

    def payment_proof_link(self, obj):
        if obj.payment_proof:
            return format_helpers("<a href='{}'>Download</a>", obj.payment_proof.url)
        return "-"
    payment_proof_link.short_description = 'Comprovante de Pagamento'

    def invoice_link(self, obj):
        if obj.invoice:
            return format_helpers("<a href='{}'>Download</a>", obj.invoice.url)
        return "-"
    invoice_link.short_description = 'Nota Fiscal'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('report/', self.admin_site.admin_view(report_view), name='financials-report'),
        ]
        return custom_urls + urls

    
    # class Media:
    #     js = ("base/js/jquery.mask.min.js",
    #           "financials/js/custom.mask.js")

admin.site.register(AppointmentFinancials, AppointmentFinancialsAdmin)