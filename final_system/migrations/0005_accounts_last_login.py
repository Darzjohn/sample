# Generated by Django 4.2.8 on 2024-05-24 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_system', '0004_accounts'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='last_login',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
