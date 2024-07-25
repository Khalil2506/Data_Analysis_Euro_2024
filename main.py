import module as md  # Importa un módulo personalizado
import pandas as pd  
import concat as ct  # Importa otro módulo personalizado para encontrar el player_id
import LanusStats as ls  # Importa un módulo específico para estadísticas

# Inicializa una instancia de Fbref para obtener estadísticas de jugadores
fbref = ls.Fbref()
player = fbref.get_player_season_stats('stats', 'Euros', '2024')  # Obtiene estadísticas de jugadores para la Euro 2024
player_euro = pd.DataFrame(player)  # Convierte las estadísticas a un DataFrame

# Agrega identificadores de jugador al DataFrame usando una función del módulo 'concat'
df_player_euro = ct.add_id_player_df(55, 282, player_euro)

# Obtiene datos de partidos y estadísticas relacionadas usando funciones del módulo 'module'
match_euro = md.match_competition(55, 282)
tarjetas_amarillas_df = md.tarjetas_amarillas_por_partido(55, 282)  # Tarjetas amarillas por partido
df_red = md.card_player(55, 282)  # Tarjetas por jugador (incluye tarjetas rojas)
df_chance_goal = md.player_chance_goal(55, 282)  # Oportunidades de gol por jugador
df_player_dribllle = md.player_dribble_complete(55, 282)  # Dribles completos por partido
df_penalty_player = md.penalty_for_player(55, 282)  # Penales por jugador
df_pass_key = md.pass_key_for_matches(55, 282)  # Pases clave por partido
df_pass = md.pass_for_match(55, 282)  # Pases por partido
df_goal = md.goal_for_player(55, 282)  # Goles por jugador

# Agrupa los datos de goles por jugador y país
df_goal_player = df_goal.groupby(['player', 'country'])['goal'].sum().to_frame()

# Agrupa los datos de asistencias por jugador y país
df_assist = md.assist_player(55, 282)
df_assist_player = df_assist.groupby(['player', 'country'])['assist'].sum().to_frame()

# Agrupa los datos de tiros por jugador y país
df_shot = md.shot_for_player(55, 282)
df_shot_player = df_shot.groupby(['player', 'country'])['shot'].count().to_frame()

df_port = md.porteria_zero(55, 282)  # Datos de porterías a cero
df_minutes = md.calcular_minutos_jugados(55, 282)  # Calcula minutos jugados por jugador
df_match_for_player = md.calcular_partidos_jugados(55, 282)  # Calcula partidos jugados por jugador

# Escribe todos los DataFrames en un archivo Excel con múltiples hojas
with pd.ExcelWriter('Euro_2024.xlsx') as writer:
    match_euro.to_excel(writer, sheet_name='Match Euro', index=False)
    df_player_euro.to_excel(writer, sheet_name='Player Euro', index=False)
    df_pass.to_excel(writer, sheet_name='Pases', index=False)
    df_goal.to_excel(writer, sheet_name='Goles Por Jugador', index=False)
    df_assist.to_excel(writer, sheet_name='Asistencias Por Jugador', index=False)
    df_chance_goal.to_excel(writer, sheet_name='Oportunidades de Gol', index=False)
    df_player_dribllle.to_excel(writer, sheet_name='Dribles Completos', index=False)
    df_penalty_player.to_excel(writer, sheet_name='Penales Por Jugador', index=False)
    df_pass_key.to_excel(writer, sheet_name='Pases Clave', index=False)
    df_port.to_excel(writer, sheet_name='Porteria a cero', index=False)
    df_shot.to_excel(writer, sheet_name='Tiro por jugador', index=False)
    df_minutes.to_excel(writer, sheet_name='Minutos por jugador', index=False)
    df_match_for_player.to_excel(writer, sheet_name='partidos por jugador', index=False)
    tarjetas_amarillas_df.to_excel(writer, sheet_name='Tarjetas por Partido', index=False)
    df_red.to_excel(writer, sheet_name='Tarjetas por Jugador', index=False)
