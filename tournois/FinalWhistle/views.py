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