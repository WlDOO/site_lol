# skins/views.py

from django.shortcuts import render
from .models import Skin

def skin_list(request):
    # Récupère tous les skins et les trie par personnage
    skins_by_champion = {}
    for skin in Skin.objects.all().order_by('champion'):
        if skin.champion not in skins_by_champion:
            skins_by_champion[skin.champion] = []
        skins_by_champion[skin.champion].append(skin)
    
    return render(request, 'skins/skin_list.html', {'skins_by_champion': skins_by_champion})
