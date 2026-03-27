import os
import pandas as pd
from sqlalchemy import create_engine, text

# --- CONFIGURACIÓ DE LA CONNEXIÓ A MYSQL ---
# Canvia això si el teu usuari o contrasenya de MySQL són diferents.
# Format: mysql+pymysql://USUARI:CONTRASENYA@HOST:PORT/
MYSQL_URL_BASE = "mysql+pymysql://root:administrador@localhost:3306/" 
DB_NAME = "projecte_barca_fc"

print("1. Connectant a MySQL...")
engine_base = create_engine(MYSQL_URL_BASE)

# Crear la base de dades si no existeix i utilitzar-la
with engine_base.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};"))
    
# Connectar-se específicamente a la nova base de dades
engine = create_engine(f"{MYSQL_URL_BASE}{DB_NAME}")

print("2. Llegint l'esquema SQL principal...")
schema_path = r"c:\Users\adria\OneDrive\Documentos\Clase\DAW\proyecte\ProjecteBarca\database_schema.sql"
with engine.connect() as conn:
    # Executem el fitxer SQL sencer
    with open(schema_path, 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')
        for command in sql_commands:
            if command.strip():
                conn.execute(text(command))
    conn.commit()

print("3. Llegint els fitxers CSV...")
data_dir = r"c:\Users\adria\OneDrive\Documentos\Clase\DAW\proyecte\ProjecteBarca\data"

competitions_df = pd.read_csv(os.path.join(data_dir, 'competitions.csv'))
clubs_df = pd.read_csv(os.path.join(data_dir, 'clubs.csv'))
players_df = pd.read_csv(os.path.join(data_dir, 'players.csv'))

# Seleccionem només les columnes del nostre esquema per competicions
comp_cols = ['competition_id', 'name', 'sub_type', 'country_id', 'country_name']
competitions_df = competitions_df[[c for c in comp_cols if c in competitions_df.columns]]

# Seleccionem les columnes per clubs
club_cols = ['club_id', 'name', 'domestic_competition_id', 'total_market_value', 
             'squad_size', 'average_age', 'foreigners_number', 'foreigners_percentage', 
             'stadium_name', 'stadium_seats', 'coach_name', 'url']
clubs_df = clubs_df[[c for c in club_cols if c in clubs_df.columns]]

# Seleccionem les columnes per jugadors
player_cols = ['player_id', 'first_name', 'last_name', 'name', 'current_club_id', 
               'country_of_citizenship', 'date_of_birth', 'sub_position', 'position', 
               'foot', 'height_in_cm', 'contract_expiration_date', 'image_url', 
               'market_value_in_eur', 'highest_market_value_in_eur', 'url']
players_df = players_df[[c for c in player_cols if c in players_df.columns]]

print("4. Important dades a la base de dades (això pot trigar un poc)...")
# Important Competicions (Fem append sobre la taula ja creada amb el nostre SQL)
competitions_df.to_sql('competitions', con=engine, if_exists='append', index=False)
print(" ✔ Competicions importades!")

# Important Clubs
# Ignorem errors de Foreign Keys temporalment per si hi ha clubs sense lliga coneguda
with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
    conn.commit()

clubs_df.to_sql('clubs', con=engine, if_exists='append', index=False)
print(" ✔ Clubs importats!")

# Important Jugadors
players_df.to_sql('players', con=engine, if_exists='append', index=False)
print(" ✔ Jugadors importats!")

with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
    conn.commit()

print("Tota la informació d'Europa s'ha importat correctament a la base de dades MySQL!")
