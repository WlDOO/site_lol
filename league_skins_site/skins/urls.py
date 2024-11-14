from django.urls import path
from . import views

urlpatterns = [
    path('', views.skin_list, name='skins'),  # Vérifiez que le nom est 'skins'
]
