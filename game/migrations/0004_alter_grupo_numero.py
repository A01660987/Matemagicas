# Generated by Django 4.1.7 on 2023-04-21 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_remove_preguntas_fraccion1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='numero',
            field=models.IntegerField(unique=True),
        ),
    ]
