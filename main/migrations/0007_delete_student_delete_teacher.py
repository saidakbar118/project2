# Generated by Django 5.1.1 on 2025-02-11 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_userprofile_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
