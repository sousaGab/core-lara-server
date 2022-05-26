# Generated by Django 3.2.13 on 2022-05-26 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('description', models.TextField(blank=True, max_length=300)),
                ('type', models.CharField(blank=True, max_length=30)),
                ('location', models.CharField(blank=True, max_length=30)),
            ],
        ),
    ]
