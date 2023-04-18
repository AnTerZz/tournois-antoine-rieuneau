from django.contrib import admin
from .models import Tournament, Poule, Team, Game



class GameInline(admin.TabularInline):
    model = Game
    extra = 1


class PouleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['number']}),
    ]
    inlines = [GameInline]
    #list_display = ('poule','number')
    list_filter = ['number']
    search_fields = ['number']




# Register your models here.
admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(Poule, PouleAdmin)