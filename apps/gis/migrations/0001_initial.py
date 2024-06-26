# Generated by Django 5.0 on 2024-04-28 11:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masterclasses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GISMasterClass',
            fields=[
                ('masterclass_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='masterclasses.masterclass')),
                ('participants', models.ManyToManyField(blank=True, related_name='gis_masterclasses', to='masterclasses.participant')),
            ],
            options={
                'verbose_name': 'GIS Мастер-класс',
                'verbose_name_plural': 'GIS Мастер-классы',
            },
            bases=('masterclasses.masterclass',),
        ),
    ]
