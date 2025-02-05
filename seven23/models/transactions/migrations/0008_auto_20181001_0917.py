# Generated by Django 2.1 on 2018-10-01 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_auto_20171015_0312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paidby',
            name='attendee',
        ),
        migrations.RemoveField(
            model_name='paidby',
            name='transaction',
        ),
        migrations.RemoveField(
            model_name='abstracttransaction',
            name='date',
        ),
        migrations.RemoveField(
            model_name='abstracttransaction',
            name='local_amount',
        ),
        migrations.RemoveField(
            model_name='abstracttransaction',
            name='local_currency',
        ),
        migrations.RemoveField(
            model_name='abstracttransaction',
            name='name',
        ),
        migrations.RemoveField(
            model_name='change',
            name='new_amount',
        ),
        migrations.RemoveField(
            model_name='change',
            name='new_currency',
        ),
        migrations.RemoveField(
            model_name='debitscredits',
            name='event',
        ),
        migrations.RemoveField(
            model_name='debitscredits',
            name='used_by',
        ),
        migrations.AddField(
            model_name='abstracttransaction',
            name='blob',
            field=models.TextField(blank=True, verbose_name='blob'),
        ),
        migrations.AddField(
            model_name='abstracttransaction',
            name='deleted',
            field=models.BooleanField(default=False, help_text='If true, this entry has been deleted and we keep this is as deleted as a tombstone.', verbose_name='Deleted'),
        ),
        migrations.DeleteModel(
            name='PaidBy',
        ),
    ]
