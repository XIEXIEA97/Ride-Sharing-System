# Generated by Django 3.1.5 on 2021-02-07 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('didi', '0011_auto_20210206_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='destination',
            field=models.CharField(max_length=50),
        ),
    ]