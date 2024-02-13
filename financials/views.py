from django.db.models import Sum
from django.shortcuts import render

from base.choices import PAYMENT_TYPE
from .models import AppointmentFinancials
from .forms import ReportFilterForm
from django.utils.timezone import make_aware
from datetime import datetime
import csv
from django.http import HttpResponse

def report_view(request):
    form = ReportFilterForm(request.GET or None)
    report_data = {}
    total_sum_all_types = 0
    action = request.GET.get('action')

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        payment_type = form.cleaned_data.get('payment_type')
        include_all = form.cleaned_data.get('all_payment_types')

        date_filter = {}
        if start_date:
            date_filter['created_on__date__gte'] = start_date
        if end_date:
            date_filter['created_on__date__lte'] = end_date
        if not include_all:
            date_filter['payment_type'] = payment_type

        filtered_financials = AppointmentFinancials.objects.filter(**date_filter)
        
        if action == 'Exportar':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="financials_report.csv"'

            writer = csv.writer(response)
            writer.writerow(['Payment Type', 'Appointment', 'Price', 'Date'])

            total_sum_all_types = 0
            for pt, pt_name in PAYMENT_TYPE:
                pt_data = filtered_financials.filter(payment_type=pt)
                sum_for_type = pt_data.aggregate(Sum('price'))['price__sum'] or 0
                total_sum_all_types += sum_for_type

                writer.writerow([pt_name])
                for financial in pt_data:
                    writer.writerow(['', financial.appointment, financial.price, financial.created_on])

                writer.writerow(['', 'Total for ' + pt_name, sum_for_type, ''])
                writer.writerow([])  # Blank row for separation

            writer.writerow(['', 'Grand Total', total_sum_all_types, ''])
            return response
        
        if include_all:
            for pt, pt_name in PAYMENT_TYPE:
                pt_data = filtered_financials.filter(payment_type=pt)
                total_for_type = pt_data.aggregate(Sum('price'))['price__sum'] or 0
                total_sum_all_types += total_for_type
                report_data[pt_name] = {
                    'items': pt_data,
                    'total': total_for_type
                }
        else:
            payment_type = form.cleaned_data.get('payment_type')
            if payment_type:
                pt_data = filtered_financials.filter(payment_type=payment_type)
                total_for_type = pt_data.aggregate(Sum('price'))['price__sum'] or 0
                total_sum_all_types += total_for_type
                pt_name = dict(PAYMENT_TYPE).get(payment_type)
                report_data[pt_name] = {
                    'items': pt_data,
                    'total': total_for_type
                }

    return render(request, 'financials/report.html', {
        'form': form,
        'report_data': report_data,
        'total_sum_all_types': total_sum_all_types
    })
