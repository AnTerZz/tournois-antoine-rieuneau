from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Tournament, Game, Comment, Stadium, Team
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db.models import Q



#Base index view which displays all the tournaments in the database
class IndexView(generic.ListView):
    template_name = 'FinalWhistle/index.html'
    context_object_name = 'tournament_list'

    def get_queryset(self):
        """Return all the tournaments"""
        return Tournament.objects.order_by('name')
    

#DetailView which loads the poule template to show all the poules in a tournament and the poule information (games/scores)
class PouleView(generic.DetailView):
    template_name = 'FinalWhistle/poules.html'
    
    def get_queryset(self):
        
        return Tournament.objects.order_by('name')
    

#DetailView which loads the match template and displays information on the game, also handles the comment post function
class MatchView(generic.DetailView):
    template_name = 'FinalWhistle/match.html'
    def get_queryset(self):
        return Game.objects.order_by('id')
    
    #gets the comments in the database to be displayed by the match page, orders them by date
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(game=self.get_object()).order_by('-date')
        data['comments'] = comments_connected
        return data
    
    #post function when a new comment is added
    def post(self, request, *args, **kwargs):
        new_comment = Comment(body=request.POST.get('body'),
                                  user=self.request.user,
                                  game=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


#UpdateView which allows an authenticated user to update his comments' 'body'
class EditCommentView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    fields = ['body']
    template_name = 'FinalWhistle/edit_comment.html'
    success_url = reverse_lazy('FinalWhistle:index') 

    def get_success_url(self):
        #redirect the user to the game page when the comment has been succesfully modified
        return reverse('FinalWhistle:match', args=[self.object.game.pk]) 

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    
#Custom 404 view, loads the right template
def custom_404(request, exception):
    return render(request, 'FinalWhistle/404.html', status=404)




def scatter_plot(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    teams = tournament.team_set.all()
    data = [(team.goals_scored(), team.goals_conceded()) for team in teams]
    context = {'data': data, 'tournament': tournament} # Add tournament to the context
    return render(request, 'FinalWhistle/scatter_plot.html', context)

def goal_plot(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    teams = tournament.team_set.all()
    data = [(team.goals_scored(), team.goals_conceded()) for team in teams]
    context = {'data': data, 'tournament': tournament} # Add team names to the context
    return render(request, 'FinalWhistle/goal_plot.html', context)


import json


def team_goals(request, pk):
    game = Game.objects.get(id=pk)
    team_home = game.home_team
    team_away = game.away_team
    games_home = Game.objects.filter(Q(home_team=team_home) | Q(away_team=team_home)).order_by('date')
    games_away = Game.objects.filter(Q(home_team=team_away) | Q(away_team=team_away)).order_by('date')
    scores_home = []
    opponent_names_home = []
    game_dates_home = []
    for game in games_home:
        if game.home_team == team_home:
            scores_home.append(game.home_score)
            opponent_names_home.append(game.away_team.name)
            game_dates_home.append(game.date.strftime("%b %d, %Y"))
        else:
            scores_home.append(game.away_score)
            opponent_names_home.append(game.home_team.name)
            game_dates_home.append(game.date.strftime("%b %d, %Y"))
    score_data_home = json.dumps(scores_home)
    opponent_names_away = []
    game_dates_away = []
    scores_away = []
    for game in games_away:
        if game.home_team == team_away:
            scores_away.append(game.home_score)
            opponent_names_away.append(game.away_team.name)
            game_dates_away.append(game.date.strftime("%b %d, %Y"))
        else:
            scores_away.append(game.away_score)
            opponent_names_away.append(game.home_team.name)
            game_dates_away.append(game.date.strftime("%b %d, %Y"))
    score_data_away = json.dumps(scores_away)
    context = {
        'score_data_home': score_data_home,
        'score_data_away': score_data_away,
        'opponent_names_home': opponent_names_home,
        'opponent_names_away': opponent_names_away,
        'game_dates_home': game_dates_home,
        'game_dates_away': game_dates_away,
        'home_team': team_home,
        'away_team': team_away,
    }
    return render(request, 'FinalWhistle/team_goals.html', context)

#Search
def search(request):
        query = request.GET.get('q')
        search_mode = request.GET.get('search_mode')
        game_date = request.GET.get('date')
        game_location = request.GET.get('location')
        home_team = request.GET.get('home_team')
        away_team = request.GET.get('away_team')
        home_score = request.GET.get('home_score')
        away_score = request.GET.get('away_score')
        tournament_list = None
        team_list = None
        game_list = None
        
        if not (game_date or game_location or home_team or away_team or home_score or away_score):
            #two modes for searching tournaments and teams
            if search_mode == 'Tournament':
                tournament_list = Tournament.objects.filter(name__contains=query).union(
                Tournament.objects.filter(location__contains=query))
            elif search_mode == 'Team':
                team_list = Team.objects.filter(name__icontains=query)
            
        #filter of matches
        query1 = ((Q(date__contains=game_date) | Q(date__isnull=True)) 
                    & (Q(location__contains=game_location) | Q(location__isnull=True))
                    & (Q(home_score__contains=home_score) | Q(home_score__isnull=True))
                    & (Q(away_score__contains=away_score) | Q(away_score__isnull=True))
                    & (Q(home_team__name__contains=home_team) | Q(home_team__name__isnull=True))
                    & (Q(away_team__name__contains=away_team) | Q(away_team__name__isnull=True)))
        if query1:
            game_list = Game.objects.order_by("-date").filter(query1)

                
        return render(request, 'FinalWhistle/search.html', {'tournament_list': tournament_list, 
                                                           'team_list':team_list, "game_list":game_list})

def map_view(request):
    stadiums = list(Stadium.objects.values('name','latitude','longitude')) 
    return render(request, 'FinalWhistle/test_map.html', context={'stadiums':stadiums}) 

