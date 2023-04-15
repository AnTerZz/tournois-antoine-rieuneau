from django.shortcuts import render
from .models import Tournament
from django.views import generic
class IndexView(generic.ListView):
    template_name = 'FinalWhistle/index.html'
    context_object_name = 'tournament_list'

    def get_queryset(self):
        """Return all the tournaments"""
        return Tournament.objects.order_by('name')[:3]
    
def custom_404(request, exception):
    return render(request, '404.html', status=404)