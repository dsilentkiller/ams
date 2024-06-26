# Generated by Django 5.0.6 on 2024-06-05 08:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_users_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phoneNumber',
            field=models.CharField(help_text="Phone number in the format '+977 9823456789'. Up to 15 digits allowed.", max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format '+977 9823456789'. Up to 15 digits allowed.", regex='^(\\+\\d{1,2}\\s?)?\\d{7,10}$')]),
        ),
    ]
