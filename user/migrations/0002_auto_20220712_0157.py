# Generated by Django 3.2.13 on 2022-07-12 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, max_length=130),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_staff',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
