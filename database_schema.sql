-- Creació de la Base de Dades per al Projecte
CREATE DATABASE IF NOT EXISTS projecte_barca_fc;
USE projecte_barca_fc;

-- Taula: les Lligues o Competicions (Opcional, però recomanable per "Tota Europa")
CREATE TABLE IF NOT EXISTS competitions (
    competition_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    sub_type VARCHAR(50),      -- Ex: first_tier, cup, etc.
    country_id VARCHAR(10),
    country_name VARCHAR(50)
);

-- Taula: CLUBS
CREATE TABLE IF NOT EXISTS clubs (
    club_id INT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    domestic_competition_id VARCHAR(10),
    total_market_value DECIMAL(15, 2),
    squad_size INT,
    average_age DECIMAL(4, 2),
    foreigners_number INT,
    foreigners_percentage DECIMAL(5, 2),
    stadium_name VARCHAR(150),
    stadium_seats INT,
    coach_name VARCHAR(100),
    url VARCHAR(500),
    FOREIGN KEY (domestic_competition_id) REFERENCES competitions(competition_id) ON DELETE SET NULL
);

-- Taula: JUGADORS
CREATE TABLE IF NOT EXISTS players (
    player_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    name VARCHAR(150) NOT NULL,
    current_club_id INT,
    country_of_citizenship VARCHAR(50),
    date_of_birth DATE,
    sub_position VARCHAR(50),
    position VARCHAR(50),
    foot VARCHAR(10),
    height_in_cm INT,
    contract_expiration_date DATE,
    image_url VARCHAR(500),
    market_value_in_eur DECIMAL(15, 2),
    highest_market_value_in_eur DECIMAL(15, 2),
    url VARCHAR(500),
    FOREIGN KEY (current_club_id) REFERENCES clubs(club_id) ON DELETE SET NULL
);

-- Taula: MERCAT DE FITXATGES (Per permetre comprar i vendre a l'App)
-- Aquesta taula registrarà totes les ofertes i traspassos.
CREATE TABLE IF NOT EXISTS transfers (
    transfer_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    from_club_id INT,
    to_club_id INT NOT NULL,
    transfer_fee DECIMAL(15, 2) NOT NULL,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED') DEFAULT 'PENDING',
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (from_club_id) REFERENCES clubs(club_id) ON DELETE CASCADE,
    FOREIGN KEY (to_club_id) REFERENCES clubs(club_id) ON DELETE CASCADE
);

-- Taula Opcional: USUARIS (Si assignes un equip a usuaris reals o per l'autenticació de la web)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    club_id INT, -- Quin equip gestiona l'usuari
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(club_id) ON DELETE SET NULL
);
