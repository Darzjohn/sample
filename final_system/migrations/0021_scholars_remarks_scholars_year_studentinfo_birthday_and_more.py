# Generated by Django 4.2.8 on 2024-05-29 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_system', '0020_rename_status_scholars_scholar_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholars',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='scholars',
            name='year',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='extension',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
