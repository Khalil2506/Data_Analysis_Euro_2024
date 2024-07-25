import pandas as pd
from rapidfuzz import process, fuzz
from statsbombpy import sb

def add_id_player_df(id_competition,id_season,df_player):
    # Leer datos de Excel
    df_excel = pd.read_excel('Euro_2024.xlsx', sheet_name='Player_euro')

    # Obtener todos los partidos de la Eurocopa 2024
    df_euros = sb.matches(competition_id=id_competition, season_id=id_season)

    # Inicializar un DataFrame vacío para almacenar todos los eventos
    all_events = pd.DataFrame()

    # Iterar sobre todos los match_id y obtener los eventos
    for match_id in df_euros['match_id']:
        events = sb.events(match_id=match_id)
        all_events = pd.concat([all_events, events], ignore_index=True)

    # Filtrar datos de StatsBomb para eliminar filas con NaN en las columnas relevantes
    all_events = all_events.dropna(subset=['player', 'player_id'])

    def preprocesar_nombre(nombre):
        return nombre.lower().strip()

    # Preprocesar los nombres en el DataFrame de Excel y en los eventos
    df_player['Player'] = df_player['Player'].apply(preprocesar_nombre)
    all_events['player'] = all_events['player'].apply(preprocesar_nombre)

    def encontrar_mejor_coincidencia(nombre_excel, nombres_statsbomb, ids_statsbomb):
        mejor_coincidencia = process.extractOne(nombre_excel, nombres_statsbomb, scorer=fuzz.ratio)
        if mejor_coincidencia:
            nombre_mas_parecido, similitud = mejor_coincidencia[:2]
            if similitud > 75:  # Puedes ajustar este umbral según tus necesidades
                return ids_statsbomb[nombres_statsbomb.index(nombre_mas_parecido)]
        return None

    nombres_statsbomb = all_events['player'].tolist()
    ids_statsbomb = all_events['player_id'].tolist()

    df_player['player_id'] = df_player['Player'].apply(lambda x: encontrar_mejor_coincidencia(x, nombres_statsbomb, ids_statsbomb))
    df_player = df_player[['player_id'] + df_player.columns[:-1].tolist()]

    return df_player