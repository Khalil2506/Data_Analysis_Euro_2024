from statsbombpy import sb
import pandas as pd
import LanusStats as ls

def match_competition(id_competetion,id_season):
    match = sb.matches(id_competetion,id_season)
    return match

def tarjetas_amarillas_por_partido(id_competencia, id_season):
    # Obtener todos los partidos de la competencia
    data_euro = sb.matches(competition_id=id_competencia, season_id=id_season)
    
    # Crear una lista para almacenar los resultados
    resultados = []
    
    # Iterar sobre cada partido
    for match_id in data_euro['match_id']:
        
        # Obtener todos los eventos del partido
        events_euro = sb.events(match_id=match_id)
        
        # Verificar los nombres de las columnas para tarjetas amarillas
        if 'foul_committed_card' in events_euro.columns:
            card_column_1 = 'foul_committed_card'
        else:
            card_column_1 = None
        
        if 'bad_behaviour_card' in events_euro.columns:
            card_column_2 = 'bad_behaviour_card'
        else:
            card_column_2 = None
        
        # Contar las tarjetas amarillas en ambas columnas
        yellow_card_count = 0
         # Contar tarjetas amarillas y segundas tarjetas amarillas en ambas columnas
        red_card_count = 0
        second_yellow_card_count = 0
        
        if card_column_1:
            red_card_count += events_euro[events_euro[card_column_1] == 'Red Card'].shape[0]
            second_yellow_card_count += events_euro[events_euro[card_column_1] == 'Second Yellow'].shape[0]
        
        if card_column_2:
            red_card_count += events_euro[events_euro[card_column_2] == 'Red Card'].shape[0]
            second_yellow_card_count += events_euro[events_euro[card_column_2] == 'Second Yellow'].shape[0]
        if card_column_1:
            yellow_card_count += events_euro[events_euro[card_column_1] == 'Yellow Card'].shape[0]
        
        if card_column_2:
            yellow_card_count += events_euro[events_euro[card_column_2] == 'Yellow Card'].shape[0]
        
        # Obtener la información del equipo local y visitante
        match_info = data_euro[data_euro['match_id'] == match_id].iloc[0]
        local_team = match_info['home_team']
        visiting_team = match_info['away_team']
        group_stage = match_info['competition_stage']
        
        # Añadir los resultados a la lista
        resultados.append({
            'match_id': match_id,
            'local_country': local_team,
            'visiting_country': visiting_team,
            'group_stage': group_stage,
            'yellow_card_count': yellow_card_count,
            'red_card_count': red_card_count,
            'second_yellow_card_count': second_yellow_card_count
            
        })
    
    # Convertir la lista de resultados a un DataFrame
    yellow_card_df = pd.DataFrame(resultados)
    
    return yellow_card_df

def card_player(id_competition, id_season):
    df_euro = sb.matches(competition_id=id_competition, season_id=id_season)
    results = []
    
    card_types = ['Yellow Card', 'Second Yellow', 'Red Card']
    
    for i, match_id in enumerate(df_euro['match_id']):
        if i >= 51:
            break
        
        df_match = sb.events(match_id=match_id)
        df_result = df_euro[df_euro['match_id'] == match_id]
        competition_stage = df_result['competition_stage'].iloc[0]
        
        card_columns = ['foul_committed_card', 'bad_behaviour_card']
        
        for card_column in card_columns:
            if card_column in df_match.columns:
                for card_type in card_types:
                    card_df = df_match[df_match[card_column] == card_type]
                    for _, row in card_df.iterrows():
                        results.append({
                            'match_id': match_id,
                            'player_id': row['player_id'],
                            'player': row['player'],
                            'country': row['team'],
                            'card': card_type,
                            'competition_stage': competition_stage
                        })
    
    return pd.DataFrame(results)

def player_chance_goal(id_competition, id_season):
    df_euro = sb.matches(competition_id=id_competition, season_id=id_season)
    
    result = []
    
    for i, match_id in enumerate(df_euro['match_id']):
        if i >= 51:
            break
        
        events_euro = sb.events(match_id=match_id)
        
        # Verificar si la columna 'shot_statsbomb_xg' existe
        if 'shot_statsbomb_xg' in events_euro.columns:
            chance_player = events_euro[['player_id','player', 'shot_statsbomb_xg']].dropna(subset=['shot_statsbomb_xg'])
            
            # Añadir resultados solo si hay datos después de eliminar nulos
            if not chance_player.empty:
                for _, row in chance_player.iterrows():
                    result.append({
                        'match_id': match_id,
                        'player_id': row['player_id'],
                        'player': row['player'],
                        'chance_goal': row['shot_statsbomb_xg']
                    })
        else:
            print(f"Columna 'shot_statsbomb_xg' no encontrada en el partido {match_id}")
    
    df_results = pd.DataFrame(result)
    
    return df_results

def player_dribble_complete(id_competition, id_season):
    # Obtener todos los partidos de la competencia
    df_euro_1 = sb.matches(competition_id=id_competition, season_id=id_season)
    
    # Crear una lista para almacenar los resultados
    result = []
    
    # Iterar sobre cada partido
    for i, match_id in enumerate(df_euro_1['match_id']):
        if i >= 51:
            break
        
        # Obtener todos los eventos del partido
        events_euro_1 = sb.events(match_id=match_id)
        
        # Filtrar los dribles completos
        dribble_complete = events_euro_1[events_euro_1['dribble_outcome'] == 'Complete']
        
        # Verificar si hay dribles completos
        if not dribble_complete.empty:
            for _, row in dribble_complete.iterrows():
                player = row['player']
                team = row['team']
                
                # Añadir los resultados a la lista
                result.append({
                    'match_id': match_id,
                    'player_id': row['player_id'],
                    'player': player,
                    'country': team,
                    'dribble': 'Complete'
                })
    
    # Convertir la lista de resultados a un DataFrame
    result_df = pd.DataFrame(result)
    return result_df    

def penalty_for_player(id_competition,id_season):
    df_euro_2 = sb.matches(competition_id=id_competition,season_id=id_season)
 
    result = []
    
    for i,matches in enumerate(df_euro_2['match_id']):
        if i>=51:
            break
        df_match = sb.events(match_id=matches)
        penalty = df_match[df_match['shot_type']=='Penalty']
    
        
        if not penalty.empty:
            for _, row in penalty.iterrows():
                player = row['player']
                team = row['team']
                goal = row['shot_outcome']
        
                result.append({
                    'match_id':matches,
                    'player_id': row['player_id'],
                    'player':player,
                    'country':team,
                    'Penalty':'Penalty',
                    'goal':goal
                })
    df_result = pd.DataFrame(result)
    return df_result


def pass_key_for_matches(id_competition, id_season):
    df_euro = sb.matches(competition_id=id_competition, season_id=id_season)
    result = []
    for match in df_euro['match_id']:
        df_matches = sb.events(match_id=match)
        for _, row in df_matches.iterrows():
            player = row.get('player')
            team = row.get('team')
            pass_key = row.get('shot_key_pass_id', None)
            
            if pd.notna(pass_key):  # Solo añade si pass_key no es NaN
                result.append({
                    'match_id': match,
                    'player_id': row['player_id'],
                    'player': player,
                    'country': team,
                    'pass_key': pass_key
                })
                
    df_result = pd.DataFrame(result)
    return df_result

def pass_for_match(id_competition, id_season):
    df_euro = sb.matches(competition_id=id_competition, season_id=id_season)
    result = []
    for i, match in enumerate(df_euro['match_id']):
        if i >=51:
            break
        df_matches = sb.events(match_id=match)
        # Filtrar eventos de pase
        pass_m = df_matches[df_matches['type'] == 'Pass']
        # Contar total de pases por jugador
        pass_total = pass_m.groupby(['player_id','player', 'team'])['player'].count().to_frame()
        complete = pass_m[pass_m['pass_outcome'].isnull()]
        incomplete = pass_m[pass_m['pass_outcome'].notnull()]
        # Contar pases completos e incompletos por jugador
        pass_total['pass_complete'] = complete.groupby(['player_id','player', 'team'])['player'].count().to_frame()
        pass_total['pass_incomplete'] = incomplete.groupby(['player_id','player', 'team'])['player'].count().to_frame()
        # Rellenar NaN con 0
        pass_total = pass_total.fillna(0)
        # Renombrar la columna de total de pases
        pass_total = pass_total.rename(columns={'player': 'pass_total'})
        # Resetear el índice para tener player y team como columnas
        pass_total = pass_total.reset_index()
        # Calcular el porcentaje de pases completados
        pass_total['percentage'] = pass_total['pass_complete'] / pass_total['pass_total'] * 100
        for _, row in pass_total.iterrows():
            player = row.get('player')
            player_id = row.get('player_id')
            team = row.get('team')
            pass_total = row.get('pass_total')
            pass_complete = row.get('pass_complete')
            pass_incomplete = row.get('pass_incomplete')
            percentage = row.get('percentage')
            
      
            result.append({
                'match_id': match,
                'player_id':player_id,
                'player': player,
                'team': team,
                'pass_total':pass_total,
                'pass_complete': pass_complete,
                'pass_incomplete': pass_incomplete,
                'percentage': percentage
            })
                
    df_result = pd.DataFrame(result)
    return df_result
  

def goal_for_player(id_competition, id_season):
    df_euro = sb.matches(competition_id=id_competition, season_id=id_season)
    result = []
    for i,match in enumerate(df_euro['match_id']):
        if i >= 51:
            break
        df_matches = sb.events(match_id=match)
        goal_player = df_matches[df_matches['shot_outcome']=='Goal']
        
        for _, row in goal_player.iterrows():
            player = row.get('player')
            team = row.get('team')
    
            result.append({
                'match_id': match,
                'player_id': row['player_id'],
                'player': player,
                'country': team,
                'goal': 1
            })
                
    df_result = pd.DataFrame(result)
    return df_result

def assist_player(id_competition, id_season):
    df_euro = sb.matches(competition_id=id_competition, season_id=id_season)
    result = []
    for i, match in enumerate(df_euro['match_id']):
        if i >= 51:  # Limitar a los primeros 5 partidos
            break
        df_matches = sb.events(match_id=match)
        
        # Verificar si la columna 'pass_goal_assist' está presente
        if 'pass_goal_assist' in df_matches.columns:
            assist_player = df_matches[df_matches['pass_goal_assist'] == True]
            
            for _, row in assist_player.iterrows():
                player = row.get('player')
                team = row.get('team')
                result.append({
                    'match_id': match,
                    'player_id': row['player_id'],
                    'player': player,
                    'country': team,
                    'assist': 1
                })
        else:
            print(f"Partido {match} no tiene columna 'pass_goal_assist'")
                
    df_result = pd.DataFrame(result)
    return df_result

def shot_for_player(id_competition, id_season):
    df_euro = sb.matches(competition_id=id_competition, season_id=id_season)
    result = []
    for i,match in enumerate(df_euro['match_id']):
        if i >= 51:
            break
        df_matches = sb.events(match_id=match)
        goal_player = df_matches[pd.notna(df_matches['shot_outcome']) & (df_matches['shot_type'] != 'Penalty')]
        
        for _, row in goal_player.iterrows():
            player = row.get('player')
            team = row.get('team')
            shot = row.get('shot_outcome')
    
            result.append({
                'match_id': match,
                'player_id': row['player_id'],
                'player': player,
                'country': team,
                'shot': shot,
            })
                
    df_result = pd.DataFrame(result)
    return df_result

def porteria_zero(id_competition, id_season):
    # Obtener datos de los partidos
    df_euro = sb.matches(competition_id=id_competition, season_id=id_season)
    result = []
    
    # Filtrar los partidos donde al menos un equipo no recibió goles
    score_zero = df_euro[(df_euro['home_score'] == 0) | (df_euro['away_score'] == 0)]
    
    for match in score_zero.itertuples():
        # Obtener eventos para el partido actual
        events_euro = sb.events(match_id=match.match_id)
        arquero = events_euro[events_euro['position'] == 'Goalkeeper']
        goalkeepers_info = arquero[['player_id','player', 'team']].drop_duplicates().reset_index(drop=True)    
        
        # Agregar datos del equipo local si tiene portería a cero
        if match.away_score == 0:
            home_goalkeeper = goalkeepers_info[goalkeepers_info['team'] == match.home_team]
           
            if not home_goalkeeper.empty:
                result.append({
                    'match_id': match.match_id,
                    'country': match.home_team,
                    'player_id': home_goalkeeper['player_id'].iloc[0],
                    'player': home_goalkeeper['player'].iloc[0],
                    'score': 1
                })
        
        # Agregar datos del equipo visitante si tiene portería a cero
        if match.home_score == 0:
            away_goalkeeper = goalkeepers_info[goalkeepers_info['team'] == match.away_team]
           
            if not away_goalkeeper.empty:
                result.append({
                    'match_id': match.match_id,
                    'country': match.away_team,
                    'player_id': away_goalkeeper['player_id'].iloc[0],
                    'player': away_goalkeeper['player'].iloc[0],
                    'score': 1
                })
                
    # Crear un DataFrame con los resultados
    df_result = pd.DataFrame(result)
    return df_result

def calcular_minutos_jugados(id_competition, id_season):
    df_euro = sb.matches(competition_id=id_competition, season_id=id_season)
    result = []

    for match in df_euro.itertuples():
        events = sb.events(match_id=match.match_id)
        players = events['player_id'].unique()
        
        for player in players:
            player_events = events[events['player_id'] == player]
            
            if player_events.empty:
                continue
            
            player_name = player_events['player'].iloc[0]
            team_name = player_events['team'].iloc[0]
            start_minute = player_events['minute'].min()
            end_minute = player_events['minute'].max()

            # Verifica si el jugador fue sustituido
            sub_out = events[(events['type'] == 'Substitution') & (events['player_id'] == player)]
            sub_in = events[(events['type'] == 'Substitution') & (events['substitution_replacement_id'] == player)]
            
            if not sub_out.empty:
                end_minute = sub_out['minute'].min()
            
            if not sub_in.empty:
                start_minute = sub_in['minute'].min()

            minutos_jugados = end_minute - start_minute
            
            result.append({
                'match_id': match.match_id,
                'country': team_name,
                'player_id': player,
                'player': player_name,
                'minutos_jugados': minutos_jugados
            })
    
    df_result = pd.DataFrame(result)
    return df_result


def calcular_partidos_jugados(id_competition, id_season):
    df_euro = sb.matches(competition_id=id_competition, season_id=id_season)
    result = []
    
    for match in df_euro.itertuples():
        events = sb.events(match_id=match.match_id)
        players = events[['player_id', 'player']].drop_duplicates()

        for player in players.itertuples():
            result.append({
                'match_id': match.match_id,
                'player_id': player.player_id,
                'player': player.player
            })
    
    df_result = pd.DataFrame(result)
    partidos_jugados = df_result.groupby(['player_id', 'player'])['match_id'].nunique().reset_index()
    partidos_jugados.columns = ['player_id', 'player', 'partidos_jugados']
    
    return partidos_jugados