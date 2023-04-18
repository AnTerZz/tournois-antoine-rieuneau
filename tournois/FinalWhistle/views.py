from django.shortcuts import render
from .models import Tournament, Game
from django.views import generic
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


class DetailView(generic.DetailView):
    template_name = 'FinalWhistle/game.html'
    def get_queryset(self):
        return Game.objects.order_by('-date')