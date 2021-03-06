# Generated by Django 3.2.7 on 2021-11-18 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_account_reg_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='address',
        ),
        migrations.RemoveField(
            model_name='account',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='account',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='account',
            name='lga',
        ),
        migrations.RemoveField(
            model_name='account',
            name='marital_status',
        ),
        migrations.RemoveField(
            model_name='account',
            name='occupation',
        ),
        migrations.RemoveField(
            model_name='account',
            name='position',
        ),
        migrations.RemoveField(
            model_name='account',
            name='profile_pic',
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=50, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('marital_status', models.CharField(choices=[('Single(Never Married)', 'Single(Never Married)'), ('Engaged', 'Engaged'), ('Married', 'Married'), ('Seperated', 'Seperated'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='default.png', null=True, upload_to='profile_photos')),
                ('lga', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.lga')),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.position')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
