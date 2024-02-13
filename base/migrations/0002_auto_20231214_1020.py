from django.db import migrations
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Create or get medics group
    medics_group, _ = Group.objects.get_or_create(name='medics')
    # Create or get secretaries group
    secretaries_group, _ = Group.objects.get_or_create(name='secretaries')

    # Define a list of permission codenames
    permission_codenames = [
        'add_appointment', 'change_appointment', 'view_appointment',
        'add_medicalrecord', 'change_medicalrecord', 'view_medicalrecord',
        'add_medic', 'change_medic', 'view_medic',
        'add_patient', 'change_patient', 'view_patient',
        'add_relative', 'change_relative', 'view_relative',
        'add_secretary', 'change_secretary', 'view_secretary'
    ]
    codename_to_app_label = {
        'medicalrecord': 'appointment',
        'medic': 'profiles',
        'patient': 'profiles',
        'relative': 'profiles',
        'secretary': 'profiles',
    }
    # Fetch and add each permission to both groups, if not already added
    for codename in permission_codenames:
        app_label = codename.split('_')[1]
        app_label = codename_to_app_label.get(app_label, app_label)
        
        perm, _ = Permission.objects.get_or_create(
            codename=codename,
            content_type__app_label=app_label,
        )

        # Add the permission to medics_group if it doesn't have it
        if not medics_group.permissions.filter(id=perm.id).exists():
            medics_group.permissions.add(perm)

        # Add the permission to secretaries_group if it doesn't have it
        if not secretaries_group.permissions.filter(id=perm.id).exists():
            secretaries_group.permissions.add(perm)

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
