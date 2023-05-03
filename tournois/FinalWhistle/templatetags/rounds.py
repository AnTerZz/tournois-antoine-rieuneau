from django import template

register = template.Library()

@register.filter
def title(nbr_matchs):
    if nbr_matchs == 1:
        return("Finale")
    elif nbr_matchs == 2:
        return ("Demi-Finale")
    elif nbr_matchs == 4:
        return ("Quart de Finale")
    elif nbr_matchs == 8:
        return ("Huitieme de Finale")
    elif nbr_matchs == 16:
        return ("16e de Finale")