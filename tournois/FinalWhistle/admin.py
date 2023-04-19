from django.contrib import admin
from .models import Tournament, Poule, Team, Game, Comment



class GameInline(admin.TabularInline):
    model = Game
    extra = 1
    
class TeamInline(admin.TabularInline):
    model = Team
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
    #list_filter = ('date')
    search_fields = ('user', 'body')



# Register your models here.
admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(Poule, PouleAdmin)