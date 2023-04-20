import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Tournament(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    nPoules = models.IntegerField()
    nTeamsInPoule = models.IntegerField()
    date_start = models.DateField(default=datetime.date.today)
    date_end = models.DateField(default=datetime.date.today)
    def __str__(self):
        return self.name
    
class Poule(models.Model):
    number = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    def __str__(self):
        return f'Poule {self.number}'
    

class Team(models.Model):
    name = models.CharField(max_length=200)
    manager = models.CharField(max_length=200)
    players = models.TextField()
    poule = models.ForeignKey(Poule, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    def get_players(self):
        return self.players.split(',')
    def __str__(self):
        return self.name
    def total_points(self):
        home_points = self.home_games.aggregate(points=Sum(
            models.Case(
                models.When(home_score__gt=models.F('away_score'), then=3),
                models.When(home_score=models.F('away_score'), then=1),
                default=0,
                output_field=models.IntegerField(),
            )
        ))['points'] or 0
        away_points = self.away_games.aggregate(points=Sum(
            models.Case(
                models.When(away_score__gt=models.F('home_score'), then=3),
                models.When(away_score=models.F('home_score'), then=1),
                default=0,
                output_field=models.IntegerField(),
            )
        ))['points'] or 0
        return home_points + away_points
    
class Game(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    poule = models.ForeignKey(Poule, on_delete=models.CASCADE)
    score = models.CharField(max_length=200)
    nPoule = models.IntegerField()
    def __date__(self):
        return self.date
    def score1_as_list(self):
        return self.score.split(',')[0]
    def score2_as_list(self):
        return self.score.split(',')[1]
    
class Comment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    class Meta:
        ordering = ['date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)
    
    
    
    