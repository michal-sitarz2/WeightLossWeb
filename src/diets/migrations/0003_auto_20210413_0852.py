# Generated by Django 3.0.2 on 2021-04-13 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diets', '0002_auto_20210406_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diet',
            name='total_carbs',
        ),
        migrations.RemoveField(
            model_name='diet',
            name='total_energy',
        ),
        migrations.RemoveField(
            model_name='diet',
            name='total_fats',
        ),
        migrations.RemoveField(
            model_name='diet',
            name='total_protein',
        ),
    ]