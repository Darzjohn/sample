# Generated by Django 4.2.8 on 2024-05-31 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_system', '0028_alter_requirement_cor_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='extension',
            field=models.CharField(default='N/A', max_length=10),
        ),
    ]
