# Generated by Django 3.1.9 on 2021-10-30 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20211030_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.position'),
        ),
    ]
