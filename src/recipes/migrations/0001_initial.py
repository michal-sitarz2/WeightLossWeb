# Generated by Django 3.0.2 on 2021-03-24 15:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('energy', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('protein', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('carbs', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('fats', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('servings', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
            ],
        ),
    ]