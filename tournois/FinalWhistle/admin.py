from django.contrib import admin
from .models import Tournament, Poule, Team, Game, Comment



class GameInline(admin.TabularInline):
    model = Game
    extra = 1
    
class TeamInline(admin.TabularInline):
    model = Team
    extra = 1
    
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class PouleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['number']}),
    ]
    inlines = [GameInline,TeamInline]
    #list_display = ('poule','number')
    list_filter = ['number']
    search_fields = ['number']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'game', 'date')
    search_fields = ('user', 'body')

class GameAdmin(admin.ModelAdmin):
    inlines=[CommentInline]
    list_display = ('date', 'location', 'home_team', 'away_team','poule','score')
    search_fields = ('location', 'home_team','away_team','poule')


# Register your models here.
admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Game, GameAdmin)
admin.site.register(Poule, PouleAdmin)