# Generated by Django 3.0.7 on 2023-03-03 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0002_alter_experiment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
