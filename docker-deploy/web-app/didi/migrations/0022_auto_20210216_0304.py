# Generated by Django 3.1.5 on 2021-02-16 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('didi', '0021_auto_20210215_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='license_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='plate_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
