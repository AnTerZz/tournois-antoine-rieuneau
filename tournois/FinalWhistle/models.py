from django.db import models



class Tournament(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    nPoules = models.IntegerField()
    nTeamsInPoule = models.IntegerField()
    def __str__(self):
        return self.name
    
class Poule(models.Model):
    number = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    def __str__(self):
        return self.number
    

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
    def add_player(self, player_name):
        players = self.get_players()
        players.append(player_name)
        self.players = ','.join(players)
        self.save()
    def remove_player(self, player_name):
        players = self.get_players()
        if player_name in players:
            players.remove(player_name)
            self.players = ','.join(players)
            self.save()
    
    
class Game(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    score = models.CharField(max_length=200)
    nPoule = models.IntegerField()
