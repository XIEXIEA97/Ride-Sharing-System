# Generated by Django 3.1.5 on 2021-02-12 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('didi', '0017_ride_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='start_point',
            field=models.CharField(default='default', max_length=50),
            preserve_default=False,
        ),
    ]
