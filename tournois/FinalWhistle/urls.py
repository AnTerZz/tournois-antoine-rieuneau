from django.urls import path
from django.contrib.auth.views import LoginView
from .views import line_chart
from . import views

app_name = 'FinalWhistle'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tournois/', views.IndexView.as_view(), name='index'),
    path('tournois/<int:pk>/', views.PouleView.as_view(), name='poule'),
    path('match/<int:pk>', views.MatchView.as_view(), name='match'),
    path('comment/<int:pk>/edit/', views.EditCommentView.as_view(), name='edit_comment'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', views.LineChartJSONView.as_view(), name='line_chart_json'),
    path('tournois/<int:tournament_id>/scatter_plot/', views.scatter_plot, name='scatter_plot'),
]