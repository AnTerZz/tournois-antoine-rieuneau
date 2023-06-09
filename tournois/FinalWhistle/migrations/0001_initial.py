# Generated by Django 4.2 on 2023-05-03 14:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_quantity', models.IntegerField()),
                ('round_filled', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('nPoules', models.IntegerField()),
                ('nTeamsInPoule', models.IntegerField()),
                ('date_start', models.DateField(default=datetime.date.today)),
                ('date_end', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('manager', models.CharField(max_length=200)),
                ('players', models.TextField()),
                ('poule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FinalWhistle.poule')),
                ('round', models.ManyToManyField(null=True, to='FinalWhistle.round')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FinalWhistle.tournament')),
            ],
        ),
        migrations.AddField(
            model_name='round',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FinalWhistle.tournament'),
        ),
        migrations.AddField(
            model_name='poule',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FinalWhistle.tournament'),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('home_score', models.IntegerField(blank=True, null=True)),
                ('away_score', models.IntegerField(blank=True, null=True)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_games', to='FinalWhistle.team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_games', to='FinalWhistle.team')),
                ('poule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='FinalWhistle.poule')),
                ('round', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='FinalWhistle.round')),
                ('stadium', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FinalWhistle.stadium')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FinalWhistle.game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
