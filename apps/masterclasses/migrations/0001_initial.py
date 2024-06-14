# Generated by Django 5.0 on 2024-06-14 14:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MasterClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('duration', models.PositiveIntegerField()),
                ('end_register_date', models.DateTimeField()),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('image_url', models.ImageField(blank=True, null=True, upload_to='masterclass_images/')),
                ('location_name', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('province', models.CharField(blank=True, max_length=255, null=True)),
                ('area', models.CharField(blank=True, max_length=255, null=True)),
                ('locality', models.CharField(blank=True, max_length=255, null=True)),
                ('street', models.CharField(max_length=255)),
                ('house', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=20)),
                ('requires_approval', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categories', models.ManyToManyField(related_name='masterclasses', to='masterclasses.category')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organized_masterclasses', to=settings.AUTH_USER_MODEL)),
                ('speaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speaking_masterclasses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteMasterClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('master_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='masterclasses.masterclass')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('masterclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='masterclasses.masterclass')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participating_masterclasses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMasterClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_state', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=50)),
                ('date_register', models.DateTimeField(auto_now_add=True)),
                ('master_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='masterclasses.masterclass')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
