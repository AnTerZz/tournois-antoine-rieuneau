# Generated by Django 4.2 on 2023-04-20 19:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FinalWhistle', '0004_alter_game_poule_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='date_end',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='tournament',
            name='date_start',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
