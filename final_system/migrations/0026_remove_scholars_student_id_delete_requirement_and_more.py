# Generated by Django 4.2.8 on 2024-05-29 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final_system', '0025_requirement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scholars',
            name='student_ID',
        ),
        migrations.DeleteModel(
            name='Requirement',
        ),
        migrations.DeleteModel(
            name='scholars',
        ),
    ]
