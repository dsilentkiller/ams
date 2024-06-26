# Generated by Django 5.0.6 on 2024-06-20 05:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_student'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='fullName',
            field=models.CharField(blank=True, help_text='fullName field is required', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subjectCode',
            field=models.CharField(help_text='subjectCode is required', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subjectName',
            field=models.CharField(help_text='subjectName is required', max_length=255),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupName', models.CharField(help_text='groupName is required', max_length=255, unique=True)),
                ('startTime', models.CharField(max_length=255)),
                ('endTime', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('students', models.ForeignKey(help_text='student is required', on_delete=django.db.models.deletion.CASCADE, to='app.student', unique=True)),
                ('subject', models.ForeignKey(help_text='subject is required', max_length=200, on_delete=django.db.models.deletion.CASCADE, to='app.subject')),
                ('teacher', models.ForeignKey(help_text='Teacher is Required ', max_length=255, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
