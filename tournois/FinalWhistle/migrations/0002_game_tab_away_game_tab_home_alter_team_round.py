# Generated by Django 4.2 on 2023-05-04 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FinalWhistle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='tab_away',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='tab_home',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='round',
            field=models.ManyToManyField(blank=True, null=True, to='FinalWhistle.round'),
        ),
    ]
