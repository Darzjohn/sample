# Generated by Django 4.2.8 on 2024-05-30 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_system', '0027_scholars_requirement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='cor_file',
            field=models.FileField(blank=True, null=True, upload_to='cor_files/'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='grade_file',
            field=models.FileField(blank=True, null=True, upload_to='grade_files/'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='schoolid_file',
            field=models.FileField(blank=True, null=True, upload_to='schoolid_files/'),
        ),
    ]