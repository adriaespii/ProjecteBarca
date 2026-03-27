import os
import sqlite3
import pandas as pd

# Crearem un arxiu de base de dades a prop dels teus fitxers
db_file = 'projecte_barca.db'
print(f"1. Creant la base de dades SQLite '{db_file}'...")

# Ens connectem (això crea l'arxiu si no existeix)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

print("2. Creant les taules SQL per a SQLite...")

schema = """
-- Taula: les Lligues o Competicions
CREATE TABLE IF NOT EXISTS competitions (
    competition_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    sub_type TEXT,
    country_id TEXT,
    country_name TEXT
);

-- Taula: CLUBS
CREATE TABLE IF NOT EXISTS clubs (
    club_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    domestic_competition_id TEXT,
    total_market_value REAL,
    squad_size INTEGER,
    average_age REAL,
    foreigners_number INTEGER,
    foreigners_percentage REAL,
    stadium_name TEXT,
    stadium_seats INTEGER,
    coach_name TEXT,
    url TEXT,
    FOREIGN KEY (domestic_competition_id) REFERENCES competitions(competition_id) ON DELETE SET NULL
);

-- Taula: JUGADORS
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    name TEXT NOT NULL,
    current_club_id INTEGER,
    country_of_citizenship TEXT,
    date_of_birth TEXT,
    sub_position TEXT,
    position TEXT,
    foot TEXT,
    height_in_cm INTEGER,
    contract_expiration_date TEXT,
    image_url TEXT,
    market_value_in_eur REAL,
    highest_market_value_in_eur REAL,
    url TEXT,
    FOREIGN KEY (current_club_id) REFERENCES clubs(club_id) ON DELETE SET NULL
);

-- Taula: MERCAT DE FITXATGES
CREATE TABLE IF NOT EXISTS transfers (
    transfer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    from_club_id INTEGER,
    to_club_id INTEGER NOT NULL,
    transfer_fee REAL NOT NULL,
    transfer_date TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'PENDING',
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (from_club_id) REFERENCES clubs(club_id) ON DELETE CASCADE,
    FOREIGN KEY (to_club_id) REFERENCES clubs(club_id) ON DELETE CASCADE
);

-- Taula Opcional: USUARIS
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    club_id INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(club_id) ON DELETE SET NULL
);
"""
cursor.executescript(schema)
conn.commit()

print("3. Llegint els fitxers CSV d'Europa...")
data_dir = r"c:\Users\adria\OneDrive\Documentos\Clase\DAW\proyecte\ProjecteBarca\data"

competitions_df = pd.read_csv(os.path.join(data_dir, 'competitions.csv'))
clubs_df = pd.read_csv(os.path.join(data_dir, 'clubs.csv'))
players_df = pd.read_csv(os.path.join(data_dir, 'players.csv'))

# Filtrem només les columnes del nostre esquema
comp_cols = ['competition_id', 'name', 'sub_type', 'country_id', 'country_name']
competitions_df = competitions_df[[c for c in comp_cols if c in competitions_df.columns]]

club_cols = ['club_id', 'name', 'domestic_competition_id', 'total_market_value', 
             'squad_size', 'average_age', 'foreigners_number', 'foreigners_percentage', 
             'stadium_name', 'stadium_seats', 'coach_name', 'url']
clubs_df = clubs_df[[c for c in club_cols if c in clubs_df.columns]]

player_cols = ['player_id', 'first_name', 'last_name', 'name', 'current_club_id', 
               'country_of_citizenship', 'date_of_birth', 'sub_position', 'position', 
               'foot', 'height_in_cm', 'contract_expiration_date', 'image_url', 
               'market_value_in_eur', 'highest_market_value_in_eur', 'url']
players_df = players_df[[c for c in player_cols if c in players_df.columns]]

print("4. Important dades a l'arxiu SQLite (això és pràcticament instantani)...")
competitions_df.to_sql('competitions', conn, if_exists='append', index=False)
print(" ✔ Competicions europees importades!")

clubs_df.to_sql('clubs', conn, if_exists='append', index=False)
print(" ✔ Clubs d'Europa importats!")

players_df.to_sql('players', conn, if_exists='append', index=False)
print(" ✔ Jugadors importats!")

conn.close()
print("✔ Tota la base de dades local '(projecte_barca.db)' s'ha creat de forma autònoma!")
