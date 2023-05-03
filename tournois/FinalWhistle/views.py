from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .models import Tournament, Game, Comment
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin



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




from django.shortcuts import render
from .models import Tournament, Game, Team


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

def team2_goals(request, pk):
    data = Game.objects.get(id=pk)
    return render(request, 'FinalWhistle/team_goals.html', data)

from django.db.models import Q
import json

def team_goals(request, pk):
    game = Game.objects.get(id=pk)
    team_home = game.home_team
    team_away = game.away_team
    games_home = Game.objects.filter(Q(home_team=team_home) | Q(away_team=team_home)).order_by('date')
    games_away = Game.objects.filter(Q(home_team=team_away) | Q(away_team=team_away)).order_by('date')
    scores_home = []
    for game in games_home:
        if game.home_team == team_home:
            scores_home.append(game.home_score)
        else:
            scores_home.append(game.away_score)
    score_data_home = json.dumps(scores_home)
    scores_away = []
    for game in games_away:
        if game.home_team == team_away:
            scores_away.append(game.home_score)
        else:
            scores_away.append(game.away_score)
    score_data_away = json.dumps(scores_away)
    context = {
        'score_data_home': score_data_home,
        'score_data_away': score_data_away,
    }
    return render(request, 'FinalWhistle/team_goals.html', context)