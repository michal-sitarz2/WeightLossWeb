# Generated by Django 3.0.2 on 2021-04-26 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='anonimity',
            field=models.BooleanField(default=True),
        ),
    ]