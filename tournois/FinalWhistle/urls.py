from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

app_name = 'FinalWhistle'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tournois/', views.IndexView.as_view(), name='index'),
    path('tournois/<int:tournament_id>/', views.tournamentDetail, name='poule'),
    path('match/<int:pk>', views.MatchView.as_view(), name='match'),
    path('comment/<int:pk>/edit/', views.EditCommentView.as_view(), name='edit_comment'),
    path('map/', views.map_view, name='test_map'),
]