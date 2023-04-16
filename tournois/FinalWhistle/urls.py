from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

app_name = 'FinalWhistle'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    #path('login/', LoginView.as_view(template_name='FinalWhistle/login.html'), name='login')
]