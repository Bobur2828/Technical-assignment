# Generated by Django 5.0.7 on 2024-07-18 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='public',
            field=models.BooleanField(),
        ),
    ]
