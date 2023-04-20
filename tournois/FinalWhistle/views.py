from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from .models import Tournament, Poule, Game, Comment, Team
from django.views import generic
from . import models
class IndexView(generic.ListView):
    template_name = 'FinalWhistle/index.html'
    context_object_name = 'tournament_list'

    def get_queryset(self):
        """Return all the tournaments"""
        return Tournament.objects.order_by('name')
    
def custom_404(request, exception):
    return render(request, 'FinalWhistle/404.html', status=404)

def custom_500(request):
        return render(request,'FinalWhistle/404.html', status=500)


class PouleView(generic.DetailView):
    template_name = 'FinalWhistle/poules.html'
    #context_object_name="poule_list"
    def get_queryset(self):
        return Tournament.objects.order_by('name')
    def teams_view(request):
        teams = Team.objects.annotate(total_points=models.ExpressionWrapper(models.F('home_points') + models.F('away_points'), output_field=models.IntegerField())).order_by('-total_points')
        return render(request, 'teams.html', {'teams': teams})
    
class MatchView(generic.DetailView):
    template_name = 'FinalWhistle/match.html'
    #context_object_name="poule_list"
    def get_queryset(self):
        return Game.objects.order_by('id')
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = Comment.objects.filter(
            game=self.get_object()).order_by('-date')
        data['comments'] = comments_connected
        #if self.request.user.is_authenticated:
        #    data['comment_form'] = NewCommentForm(instance=self.request.user)

        return data
    def post(self, request, *args, **kwargs):
        new_comment = Comment(body=request.POST.get('body'),
                                  user=self.request.user,
                                  game=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)



from django.contrib.auth.mixins import LoginRequiredMixin
class EditCommentView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    fields = ['body']
    template_name = 'FinalWhistle/edit_comment.html'
    success_url = reverse_lazy('FinalWhistle:index')

    def get_success_url(self):
        return reverse('FinalWhistle:match', args=[self.object.game.pk])

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)