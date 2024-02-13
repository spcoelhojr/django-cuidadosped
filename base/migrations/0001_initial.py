from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')

    # Create or get medics group
    Group.objects.get_or_create(name='medics')
    # Create or get secretaries group
    Group.objects.get_or_create(name='secretaries')


class Migration(migrations.Migration):

    dependencies = [
        # Specify any dependencies here, if applicable
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
