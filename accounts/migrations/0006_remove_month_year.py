# Generated by Django 3.1.9 on 2021-10-24 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20211025_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='month',
            name='year',
        ),
    ]
