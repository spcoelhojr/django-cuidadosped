import os
import django
import random
from faker_populate import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cuidadosped.settings')
django.setup()

from django.contrib.auth.models import User
from profiles.models import Medic, Secretary, Relative, Patient
from appointment.models import Appointment, MedicalRecord
from base.choices import GENDER, RACE, RELATIVE, APPOINTMENT_TYPE
from validate_docbr import CPF  
from financials.models import AppointmentFinancials  
from djmoney.money import Money


fake = Faker('pt_BR')  # Brazilian Portuguese locale

def create_user_commons():
    user = create_user()
    cpf_generator = CPF()
    return {
        'django_user': user,
        'cpf': cpf_generator.generate(),
        'rg': fake.random_number(digits=7, fix_len=True),
        'birth_date': fake.date_of_birth(),
        'profession': fake.job(),
        'address': fake.address(),
        'phone_number': fake.phone_number(),
        'gender': random.choice([gender[0] for gender in GENDER]),
        'religion': 'Católica',
        'race': random.choice([race[0] for race in RACE]),
        'nationality': 'Brasileiro(a)'
    }

def create_user():
    first_name = fake.first_name()
    last_name = fake.last_name()
    user = User.objects.create_user(
        username=fake.user_name(),
        email=fake.email(),
        first_name=first_name,
        last_name=last_name,
        password='password123'
    )
    return user

def create_relative():
    relative_data = create_user_commons()
    relative_data['relationship'] = random.choice([rel[0] for rel in RELATIVE])
    relative_data['partner'] = None  # Assuming no partner, adjust as needed
    return Relative.objects.create(**relative_data)

def create_patient():
    patient_data = create_user_commons()
    patient_data['medic'] = Medic.objects.first()  # Using the first available Medic
    patient_data['relative'] = random.choice(Relative.objects.all())
    patient_data['allergy'] = fake.text() if fake.boolean() else ''
    patient_data['family_history'] = fake.text() if fake.boolean() else ''
    patient_data['personal_history'] = fake.text() if fake.boolean() else ''
    return Patient.objects.create(**patient_data)

def create_appointment():
    appointment_data = {
        'patient': random.choice(Patient.objects.all()),
        'medic': Medic.objects.first(),  # Using the first available Medic
        'schedule_date': fake.future_datetime(end_date="+30d"),
        'next_appointment': fake.future_datetime(end_date="+60d") if fake.boolean() else None,
        'appointment_type': random.choice([appt_type[0] for appt_type in APPOINTMENT_TYPE]),
        'is_return_appointment': fake.boolean()
    }
    return Appointment.objects.create(**appointment_data)

def create_medical_record():
    medical_record_data = {
        'appointment': random.choice(Appointment.objects.all()),
        'pc': fake.pyfloat(right_digits=2, positive=True),
        'pt': fake.pyfloat(right_digits=2, positive=True),
        'height': fake.pyfloat(right_digits=2, positive=True),
        'weight': fake.pyfloat(right_digits=2, positive=True),
        'current_disease': fake.text() if fake.boolean() else '',
        'physical_exam': fake.text(),
        'diagnose_hypothesis': fake.text() if fake.boolean() else '',
        'conduct': fake.text() if fake.boolean() else ''
    }
    return MedicalRecord.objects.create(**medical_record_data)

def create_appointment_financials():
    # Assuming Appointment model has at least one entry
    if not Appointment.objects.exists():
        raise ValueError("No appointments available to associate financials with.")

    appointment = random.choice(Appointment.objects.all())
    price = Money(amount=fake.pydecimal(left_digits=7, right_digits=2, positive=True), currency='BRL')
    payment_proof = None  
    invoice = None        

    appointment_financial = AppointmentFinancials.objects.create(
        appointment=appointment,
        price=price,
        payment_proof=payment_proof,
        invoice=invoice
    )
    return appointment_financial

def populate(N=10):
    for _ in range(N):
        create_relative()
        create_patient()

    for _ in range(N * 2):
        create_appointment()
        create_medical_record()
    create_appointment_financials()

    print(f'Populated {N} instances of Relative and Patient')

    for _ in range(N * 2):
        create_appointment()
        create_medical_record()

    print(f'Populated {N * 2} instances of Appointment and Medical Record')

if __name__ == '__main__':
    populate(10)  # Populating 10 instances of Relative and Patient, and 20 of Appointment and Medical Record
