# Generated by Django 4.2.8 on 2024-05-26 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final_system', '0012_requirement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requirement',
            old_name='student',
            new_name='studID',
        ),
    ]