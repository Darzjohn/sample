# Generated by Django 5.0.2 on 2024-06-04 22:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_system', '0038_scholars_semester_alter_scholars_scholar_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholars',
            name='date_added',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='scholars',
            name='total_units_enrolled',
            field=models.IntegerField(null=True),
        ),
    ]
