from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

def return_date():
    return date.today() + timedelta(days=30)

def age(birth_date):
    today = date.today()
    diff = relativedelta(today, birth_date)
    years, months, days = diff.years, diff.months, diff.days
    total_months = 12 * diff.years + diff.months
    total_weeks = (today - birth_date).days // 7

    return years, months, days, total_months, total_weeks, (today - birth_date).days

def age_to_str(age_tuple):
    years, months, days, total_months, total_weeks, total_days = age_tuple
    return (f"{years} {'ano' if years == 1 else 'anos'}, "
            f"{months} {'mês' if months == 1 else 'meses'}, "
            f"{days} {'dia' if days == 1 else 'dias'}, "
            f"{total_months} {'mês' if total_months == 1 else 'meses'}, "
            f"{total_weeks} {'semana' if total_weeks == 1 else 'semanas'}, "
            f"{total_days} {'dia' if total_days == 1 else 'dias'}.")
