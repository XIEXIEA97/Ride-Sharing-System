# Generated by Django 3.1.5 on 2021-01-31 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('rider_id', models.AutoField(primary_key=True, serialize=False)),
                ('destination', models.CharField(default='null', max_length=50)),
                ('arrival_time', models.DateTimeField()),
                ('owner_psger_num', models.PositiveSmallIntegerField(default=1)),
                ('vehicle_type', models.CharField(choices=[('CR', 'Car'), ('VN', 'Van'), ('BS', 'Bus'), ('TK', 'Truck')], max_length=2)),
                ('sharable', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('CONFIRMED', 'Confirmed'), ('COMPLETE', 'Complete')], default='OPEN', max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='SpecialInfo',
            fields=[
                ('info_id', models.AutoField(primary_key=True, serialize=False)),
                ('information', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=20)),
                ('vehicle_type', models.CharField(choices=[('CR', 'Car'), ('VN', 'Van'), ('BS', 'Bus'), ('TK', 'Truck')], max_length=2, null=True)),
                ('plate_number', models.CharField(max_length=20, null=True)),
                ('liscense_number', models.CharField(max_length=20, null=True)),
                ('vehicle_capacity', models.PositiveSmallIntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserShareRide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_time', models.DateTimeField(auto_now_add=True)),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sharer_rid', to='didi.ride')),
                ('user_sharer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sharer_uid', to='didi.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserOwnRide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_rid', to='didi.ride')),
                ('user_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_uid', to='didi.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserDriveRide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_time', models.DateTimeField(auto_now_add=True)),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_rid', to='didi.ride')),
                ('user_driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_uid', to='didi.user')),
            ],
        ),
        migrations.CreateModel(
            name='SpecialVehicleInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_info_id', to='didi.specialinfo')),
                ('vehicle_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_uid', to='didi.user')),
            ],
        ),
        migrations.CreateModel(
            name='RideSpecialRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ride_request_info_id', to='didi.specialinfo')),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='srequest_rid', to='didi.ride')),
            ],
        ),
    ]
