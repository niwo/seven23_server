# Generated by Django 2.1 on 2018-09-13 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0006_auto_20171015_0312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='category',
            name='selectable',
        ),
        migrations.AddField(
            model_name='category',
            name='blob',
            field=models.TextField(blank=True, verbose_name='blob'),
        ),
        migrations.AddField(
            model_name='category',
            name='last_edited',
            field=models.DateTimeField(auto_now=True, verbose_name='Last edited'),
        ),
    ]
