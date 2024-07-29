import pandas as pd
from statsbombpy import sb
from fuzzywuzzy import fuzz, process

def add_id_player_df(id_competition, id_season, df_player):
    # Obtener todos los partidos de la Copa América 2024
    df_matches = sb.matches(competition_id=id_competition, season_id=id_season)

    # Inicializar un DataFrame vacío para almacenar todas las alineaciones
    all_lineups = pd.DataFrame()

    # Iterar sobre todos los partidos y obtener las alineaciones de ambos equipos
    for match_id in df_matches['match_id']:
        lineups = sb.lineups(match_id=match_id)
        for team in lineups.keys():  # Iterar sobre equipos (home y away)
            team_lineup = lineups[team]
            all_lineups = pd.concat([all_lineups, team_lineup], ignore_index=True)

    # Preprocesar los nombres para evitar problemas de formato
    def preprocesar_nombre(nombre):
        if pd.isna(nombre):
            return ""
        return nombre.lower().strip()

    # Preprocesar los nombres en el DataFrame de Excel y en las alineaciones
    df_player['Player'] = df_player['Player'].apply(preprocesar_nombre)
    all_lineups['player_nickname'] = all_lineups['player_nickname'].apply(preprocesar_nombre)
    all_lineups['player_name'] = all_lineups['player_name'].apply(preprocesar_nombre)

    def encontrar_mejor_coincidencia(nombre_excel, lineups_df):
        coincidencia_nickname = process.extractOne(
            nombre_excel, lineups_df['player_nickname'], scorer=fuzz.token_set_ratio
        )
        if coincidencia_nickname and coincidencia_nickname[1] > 75:
            return lineups_df.loc[lineups_df['player_nickname'] == coincidencia_nickname[0], 'player_id'].values[0]

        coincidencia_name = process.extractOne(
            nombre_excel, lineups_df['player_name'], scorer=fuzz.token_set_ratio
        )
        if coincidencia_name and coincidencia_name[1] > 75:
            return lineups_df.loc[lineups_df['player_name'] == coincidencia_name[0], 'player_id'].values[0]
        
        return None

    df_player['player_id'] = df_player['Player'].apply(lambda x: encontrar_mejor_coincidencia(x, all_lineups))
    df_player = df_player[['player_id'] + df_player.columns[:-1].tolist()]

    return df_player