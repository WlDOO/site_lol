# skins/views.py

from django.shortcuts import render
from .models import Skin
from django.db.models import Q  # Import pour faire des recherches avec "OU"

def skin_list(request):
    query = request.GET.get('q')  # Récupère le terme de recherche depuis la requête GET
    if query:
        # Filtrer les skins selon le nom du champion ou le nom du skin
        skins = Skin.objects.filter(Q(champion__icontains=query) | Q(skin_name__icontains=query)).order_by('champion')
    else:
        skins = Skin.objects.all().order_by('champion')
    
    # Trier les skins par champion pour le template
    skins_by_champion = {}
    for skin in skins:
        if skin.champion not in skins_by_champion:
            skins_by_champion[skin.champion] = []
        # Ajoute chaque skin avec son champ skin_id
        skins_by_champion[skin.champion].append({
            'champion': skin.champion,
            'skin_name': skin.skin_name,
            'skin_id': skin.skin_id  # Ajout du champ skin_id
        })
    
    return render(request, 'skins/skin_list.html', {'skins_by_champion': skins_by_champion, 'query': query})
