# skins/models.py
from django.db import models

class Skin(models.Model):
    champion = models.CharField(max_length=100)
    skin_id = models.IntegerField(primary_key=True)  # Utiliser skin_id comme clé primaire
    skin_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'skins'  # Indique à Django d'utiliser la table existante

    def __str__(self):
        return f"{self.champion} - {self.skin_name}"
