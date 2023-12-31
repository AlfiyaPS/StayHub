# Generated by Django 4.2.5 on 2023-11-05 15:39

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stayhubapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('property_id', models.AutoField(primary_key=True, serialize=False)),
                ('property_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('number_of_bedrooms', models.PositiveIntegerField()),
                ('number_of_bathrooms', models.PositiveIntegerField()),
                ('capacity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_guest',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_host',
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'guest'), (2, 'host'), (3, 'admin')], default=1),
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_guest', models.BooleanField(default=True)),
                ('is_host', models.BooleanField(default=False)),
                ('guest_first_name', models.CharField(max_length=30)),
                ('guest_last_name', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('stayhubapp.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_guest', models.BooleanField(default=False)),
                ('is_host', models.BooleanField(default=True)),
                ('approved', models.BooleanField(default=False, null=True)),
                ('host_first_name', models.CharField(max_length=100)),
                ('host_last_name', models.CharField(max_length=100)),
                ('license_upload', models.FileField(upload_to='licenses/')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('stayhubapp.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='property_images/')),
                ('description', models.TextField(blank=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stayhubapp.property')),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='property_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stayhubapp.propertytype'),
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('is_available', models.BooleanField(default=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stayhubapp.property')),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='host',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='stayhubapp.host'),
        ),
    ]
