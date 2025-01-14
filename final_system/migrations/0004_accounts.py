# Generated by Django 4.2.8 on 2024-05-24 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('final_system', '0003_delete_accounts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('accountID', models.AutoField(primary_key=True, serialize=False)),
                ('personal_emailadd', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=128)),
                ('studID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='final_system.studentinfo')),
            ],
        ),
    ]
