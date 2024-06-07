# Generated by Django 5.0.2 on 2024-06-07 03:23

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_system', '0041_alter_scholars_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scholars',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='scholars',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='scholars',
            name='gpa',
        ),
        migrations.RemoveField(
            model_name='scholars',
            name='remarks',
        ),
        migrations.RemoveField(
            model_name='scholars',
            name='scholar_status',
        ),
        migrations.RemoveField(
            model_name='scholars',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='scholars',
            name='total_units_enrolled',
        ),
        migrations.RemoveField(
            model_name='scholars',
            name='year',
        ),
        migrations.CreateModel(
            name='SemesterDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('1', '1st Semester'), ('2', '2nd Semester')], default='1', max_length=10)),
                ('amount', models.IntegerField(default=0)),
                ('gpa', models.FloatField()),
                ('year', models.CharField(max_length=10, null=True)),
                ('scholar_status', models.CharField(default='ACTIVE', max_length=10)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('date_added', models.DateField(default=django.utils.timezone.now)),
                ('total_units_enrolled', models.IntegerField(null=True)),
                ('scholar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester_details', to='final_system.scholars')),
            ],
            options={
                'unique_together': {('scholar', 'semester')},
            },
        ),
    ]