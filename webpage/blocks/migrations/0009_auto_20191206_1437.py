# Generated by Django 2.2.7 on 2019-12-06 14:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0008_auto_20191206_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 6, 14, 37, 9, 747658), verbose_name='creation date'),
        ),
    ]
