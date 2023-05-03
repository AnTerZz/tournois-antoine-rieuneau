from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Tournament, Game, Comment, Round, Poule
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
    
    def get_context_data(self, **kwargs):
        context=super(PouleView,self).get_context_data(**kwargs)
        context['tournoi'] = Tournament.objects.get(pk=self.kwargs["pk"])
        tournoi = Tournament.objects.get(pk=self.kwargs["pk"])
        context['list_rounds'] = tournoi.round_set.all()
        return context
    
    
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

#Methode pour creer un match de Round avec les qualifies du Round precedent, qui n'est pas une poule
def create_match_from_round(nbr_matchs, previous_round, current_round):
    for j in range(0, nbr_matchs, 2):
        team1 = previous_round.next_qualified()[j]
        team2 = previous_round.next_qualified()[j+1]
        Game(home_team=team1, away_team=team2,round = current_round).save()
    current_round.round_filled=1
    current_round.save()
    
#Methode pour creer un match de Round avec les qualifies d'une poule
def create_match_from_poule(tournoi, round):
    for poule in tournoi.poule_set.all():
        team1 = poule.classement()[0]
        team2 = poule.classement()[1]
        Game(home_team=team1, away_team=team2,round = round).save()
    round.round_filled=1
    round.save()

#Vue de l'arborescence des matchs d'un tournoi
def TournamentTree(request, tournoi_id):
    tournoi = get_object_or_404(Tournament, pk = tournoi_id)
    nbr_matchs_poules = tournoi.poule_set.all().count()
    for i in range(0, nbr_matchs_poules):
        print(i)
        nbr_matchs=int(nbr_matchs_poules/(2**i))
        print(nbr_matchs)
        
        #Case where the next round is preceded by draws
        if i == 0:
            print("previous round is draws")
            if Round.objects.filter(tournament=tournoi, match_quantity=nbr_matchs).exists():
                print("using existing round")
                existant_round = Round.objects.get(tournament=tournoi, match_quantity=nbr_matchs)
                if existant_round.round_filled==0:
                    existant_round.game_set.all().delete()
                    print("filling round")
                    create_match_from_poule(tournoi, existant_round)
                    print(existant_round.round_filled)
            else:
                print("creating new round")
                new_round = Round(match_quantity=nbr_matchs, tournament=tournoi)
                new_round.save()
                print(new_round)  
                create_match_from_poule(tournoi, new_round)
                
        #Case where the next round isn't preceded by draws
        else:
            print("previous round isn't draws")
            previous_round = Round.objects.filter(tournament=tournoi, match_quantity=nbr_matchs*2)[0]
            if Round.objects.filter(tournament=tournoi, match_quantity=nbr_matchs).exists():
                print("using existing round")
                
                existant_round = Round.objects.get(tournament=tournoi, match_quantity=nbr_matchs)
                
                if existant_round.round_filled==0 and previous_round.next_qualified() != None:
                    existant_round.game_set.all().delete()
                    create_match_from_round(nbr_matchs, previous_round, existant_round)
            else:
                print("creating new round")
                new_round = Round(match_quantity=nbr_matchs, tournament=tournoi)
                new_round.save()
                if previous_round.next_qualified() != None:
                    create_match_from_round(nbr_matchs, previous_round, new_round)
                    
    list_rounds=tournoi.round_set.all()
    return render(request, 'FinalWhistle/tree.html', context= {'tournoi':tournoi, 'list_rounds' : list_rounds})
                    
        
                       
            
                
                    
            
            
    