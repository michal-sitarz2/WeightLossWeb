# Generated by Django 3.0.2 on 2021-04-19 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20210419_0935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='recipe_spoonacular_id',
            new_name='recipe_id',
        ),
    ]
