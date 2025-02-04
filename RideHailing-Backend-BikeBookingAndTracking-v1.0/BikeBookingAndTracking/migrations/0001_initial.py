# Generated by Django 5.0.7 on 2024-07-24 08:38

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(max_length=50)),
                ('rating', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='FareEstimation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('traffic_level', models.FloatField()),
                ('time_of_day', models.TimeField(auto_now=True)),
                ('weather_condition', models.CharField(max_length=50)),
                ('day_of_week', models.CharField(max_length=20)),
                ('distance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_location', models.CharField(max_length=255)),
                ('dropoff_location', models.CharField(max_length=255)),
                ('pickup_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('dropoff_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('accepted', 'Accepted'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='requested', max_length=50)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('rider_rating', models.FloatField(default=1.0)),
                ('rider_feedback', models.TextField(blank=True, null=True)),
                ('estimated_fare', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rides', to='BikeBookingAndTracking.driver')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('mobile_money', 'Mobile Money'), ('cash', 'Cash')], max_length=50)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('succeded', 'Succeded'), ('failed', 'Failed')], default='pending', max_length=50)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('ride', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BikeBookingAndTracking.ride')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_driver', models.BooleanField(default=False)),
                ('phone_number', models.CharField(db_index=True, max_length=15, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='bike_booking_users', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='bike_booking_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='ride',
            name='rider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rides', to='BikeBookingAndTracking.user'),
        ),
        migrations.AddField(
            model_name='driver',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BikeBookingAndTracking.user'),
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('license_plate', models.CharField(db_index=True, max_length=20)),
                ('is_electric', models.BooleanField(default=False)),
                ('driver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BikeBookingAndTracking.driver')),
            ],
        ),
        migrations.AddField(
            model_name='ride',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='BikeBookingAndTracking.vehicle'),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='BikeBookingAndTracking.ride')),
            ],
            options={
                'indexes': [models.Index(fields=['latitude', 'longitude'], name='BikeBooking_latitude_28032a_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['phone_number'], name='BikeBooking_phone_n_fb61d8_idx'),
        ),
        migrations.AddIndex(
            model_name='vehicle',
            index=models.Index(fields=['license_plate'], name='BikeBooking_license_bfe1f0_idx'),
        ),
        migrations.AddIndex(
            model_name='ride',
            index=models.Index(fields=['pickup_location'], name='BikeBooking_pickup__96d757_idx'),
        ),
        migrations.AddIndex(
            model_name='ride',
            index=models.Index(fields=['dropoff_location'], name='BikeBooking_dropoff_f61377_idx'),
        ),
    ]
