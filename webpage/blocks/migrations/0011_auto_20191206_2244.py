# Generated by Django 2.2.7 on 2019-12-06 22:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0010_auto_20191206_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 6, 22, 44, 25, 378910), verbose_name='creation date'),
        ),
    ]
