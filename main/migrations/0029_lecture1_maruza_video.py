# Generated by Django 5.1.1 on 2025-02-23 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_profileuser_birthdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture1',
            name='maruza_video',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
