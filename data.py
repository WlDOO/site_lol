import requests
import sqlite3

# Configuration de l'API Riot
API_VERSION = '13.20.1'  # Version actuelle de Data Dragon
CHAMPION_LIST_URL = f'https://ddragon.leagueoflegends.com/cdn/{API_VERSION}/data/fr_FR/champion.json'
CHAMPION_DATA_URL = f'https://ddragon.leagueoflegends.com/cdn/{API_VERSION}/data/fr_FR/champion/'

# Connexion à la base de données SQLite
conn = sqlite3.connect('league_skins.db')
cursor = conn.cursor()

# Création de la table pour les skins
cursor.execute('''
CREATE TABLE IF NOT EXISTS skins (
    champion TEXT,
    skin_id INTEGER,
    skin_name TEXT
)
''')

def get_champion_list():
    response = requests.get(CHAMPION_LIST_URL)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print("Erreur lors de la récupération de la liste des champions.")
        return None

def get_champion_skins(champion_id):
    response = requests.get(f"{CHAMPION_DATA_URL}{champion_id}.json")
    if response.status_code == 200:
        champ_data = response.json()['data'][champion_id]
        skins_data = []
        for skin in champ_data['skins']:
            skin_id = skin['num']
            skin_name = skin['name'] if skin['name'] != "default" else f"{champ_data['name']} Classique"
            skins_data.append((champ_data['name'], skin_id, skin_name))
        return skins_data
    else:
        print(f"Erreur lors de la récupération des skins pour {champion_id}.")
        return []

def insert_skins_to_db(skins_data):
    cursor.executemany('INSERT INTO skins (champion, skin_id, skin_name) VALUES (?, ?, ?)', skins_data)
    conn.commit()
    print("Skins insérés dans la base de données.")

def main():
    champion_list = get_champion_list()
    if champion_list:
        all_skins_data = []
        for champion_id in champion_list.keys():
            skins_data = get_champion_skins(champion_id)
            all_skins_data.extend(skins_data)
        insert_skins_to_db(all_skins_data)
    conn.close()
    print("Base de données créée et remplie avec succès.")

if __name__ == "__main__":
    main()
