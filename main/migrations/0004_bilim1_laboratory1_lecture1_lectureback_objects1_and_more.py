# Generated by Django 5.1.1 on 2025-02-03 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_profile1_profilefix1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bilim1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='')),
                ('image2', models.ImageField(upload_to='')),
                ('image3', models.ImageField(upload_to='')),
                ('image4', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Laboratory1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('laboratoriya_raqam', models.CharField(max_length=5)),
                ('laboratoriya_nomi', models.CharField(max_length=150)),
                ('laboratoriya_matni', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Lecture1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maruza_raqam', models.CharField(max_length=5)),
                ('maruza_nomi', models.CharField(max_length=150)),
                ('maruza_matni', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LectureBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Objects1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='')),
                ('image2', models.ImageField(upload_to='')),
                ('image3', models.ImageField(upload_to='')),
                ('image4', models.ImageField(upload_to='')),
                ('image5', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Practic1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('practic_raqam', models.CharField(max_length=5)),
                ('practic_nomi', models.CharField(max_length=150)),
                ('practic_matni', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Selfstudy1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mustaqiltalim_matni', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Trio1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='')),
                ('image2', models.ImageField(upload_to='')),
                ('image3', models.ImageField(upload_to='')),
                ('image4', models.ImageField(upload_to='')),
                ('image5', models.ImageField(upload_to='')),
            ],
        ),
    ]
