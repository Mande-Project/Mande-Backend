# Generated by Django 4.2.5 on 2023-10-01 00:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_worker_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='account',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(default=django.utils.timezone.now, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]
