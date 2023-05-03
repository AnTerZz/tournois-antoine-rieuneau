import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.forms import IntegerField
from django.db.models import F
import json

#Tournament model, keeps important information on the tournament, self-explanatory
class Tournament(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    nPoules = models.IntegerField()
    nTeamsInPoule = models.IntegerField()
    date_start = models.DateField(default=datetime.date.today)
    date_end = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return self.name
    
    def get_stadiums(self):
        stadiums = list(Stadium.objects.filter(game__poule__tournament = self).values('id','name','latitude','longitude'))
        return stadiums
    
    def get_games(self):
        games = list(Game.objects.filter(poule__tournament = self).values('stadium','home_team__name','away_team__name'))
        return games    
 
    
#Poule model, identified by a number appended to 'Poule '
class Poule(models.Model):
    number = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    def __str__(self):
        return f'Poule {self.number}'
    

#Team model, self explanatory
class Team(models.Model):
    name = models.CharField(max_length=200)
    manager = models.CharField(max_length=200)
    players = models.TextField()
    poule = models.ForeignKey(Poule, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    
    #Method to return the players as a list instead of a single string
    def get_players(self):
        return self.players.split(',')
    
    def __str__(self):
        return self.name
    
    #Method to calculate the sum of all the goals scored by a team in a tournament
    def goals_scored(self):
        home_goals = Game.objects.filter(home_team=self, poule=self.poule).aggregate(Sum('home_score'))['home_score__sum'] or 0
        away_goals = Game.objects.filter(away_team=self, poule=self.poule).aggregate(Sum('away_score'))['away_score__sum'] or 0
        return home_goals + away_goals
    
    #Method to calculate the sum of all the goals conceded by a team in a tournament
    def goals_conceded(self):
        home_goals = Game.objects.filter(home_team=self, poule=self.poule).aggregate(Sum('away_score'))['away_score__sum'] or 0
        away_goals = Game.objects.filter(away_team=self, poule=self.poule).aggregate(Sum('home_score'))['home_score__sum'] or 0
        return home_goals + away_goals
    
    #Method to calculate the total points of a team (win = 3 points, draw = 1 points, loose = 0 points)
    def points(self):
        won = Game.objects.filter(home_team=self, poule=self.poule, home_score__gt=F('away_score')) | \
              Game.objects.filter(away_team=self, poule=self.poule, away_score__gt=F('home_score'))
        drawn = Game.objects.filter(home_team=self, poule=self.poule, home_score=F('away_score')) | \
                Game.objects.filter(away_team=self, poule=self.poule, away_score=F('home_score'))
        return (3* won.count() + drawn.count()) 

class Stadium(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self) -> str:
        return self.name
    
#Team model, self explanatory
class Game(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    poule = models.ForeignKey(Poule, on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, null=True)
    def __date__(self):
        return self.date
    
    def get_stadium(self):
        return list(Stadium.objects.filter(pk=self.stadium.pk).values('name','latitude','longitude'))

    
    
#Comment model, self-explanatory
class Comment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    class Meta:
        ordering = ['date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)
    

    
    
    
    