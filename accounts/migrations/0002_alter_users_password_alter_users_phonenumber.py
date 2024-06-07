# Generated by Django 5.0.6 on 2024-06-05 08:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(help_text='Enter your password', max_length=14),
        ),
        migrations.AlterField(
            model_name='users',
            name='phoneNumber',
            field=models.CharField(max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format '+123456789'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]