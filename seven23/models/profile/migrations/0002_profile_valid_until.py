# Generated by Django 2.1 on 2019-03-11 08:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='valid_until',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 10, 8, 25, 47, 943230), help_text='On SASS, this is the validation date', verbose_name='Valid until'),
        ),
    ]
