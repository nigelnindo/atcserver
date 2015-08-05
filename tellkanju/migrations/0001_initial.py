# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_number', models.CharField(default=b'No id', help_text=b'ID of uploader', max_length=20)),
                ('description', models.CharField(help_text=b'Describe the report', max_length=200)),
                ('reportedImage', models.ImageField(help_text=b'Image addded to the report', upload_to=b'/media/images')),
                ('latitude', models.CharField(help_text=b'Latitude coordinates', max_length=30)),
                ('longitude', models.CharField(help_text=b'Longitude coordinates', max_length=30)),
            ],
        ),
    ]
