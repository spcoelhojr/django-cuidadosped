# Generated by Django 5.0 on 2023-12-18 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financials', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentfinancials',
            name='payment_type',
            field=models.CharField(choices=[('P', 'PIX'), ('D', 'Dinheiro'), ('T', 'Transferência Bancária'), ('C', 'Cartão')], default='D', max_length=1, verbose_name='Tipo de Pagamento'),
            preserve_default=False,
        ),
    ]
