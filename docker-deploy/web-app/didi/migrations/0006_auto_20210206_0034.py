# Generated by Django 3.1.5 on 2021-02-06 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('didi', '0005_auto_20210204_2228'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='liscense_number',
            new_name='license_number',
        ),
    ]
