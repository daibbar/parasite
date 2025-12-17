
-- data/schema.sql

-- Enable Foreign Keys enforcement for SQLite
PRAGMA foreign_keys = ON;

-- 1. Table Responsables
CREATE TABLE IF NOT EXISTS responsable (
    id_responsable INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    cne TEXT UNIQUE NOT NULL
);

-- 2. Table Activites
CREATE TABLE IF NOT EXISTS activite (
    id_activite INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_activite TEXT NOT NULL,
    activite_description TEXT,
    type_activite TEXT CHECK(type_activite IN ('Voyage', 'Atelier', 'Conference', 'Competition')) NOT NULL,
    capacite_max INTEGER CHECK(capacite_max > 0),
    date_debut DATETIME NOT NULL,
    date_fin DATETIME NOT NULL,
    CHECK (date_fin >= date_debut),
    id_club INTEGER,
    id_event INTEGER,
    FOREIGN KEY (id_club) REFERENCES clubs(id_club) ON DELETE CASCADE,
    FOREIGN KEY (id_event) REFERENCES events(id_club) ON DELETE CASCADE,
    CONSTRAINT check_only_one CHECK (
        (id_club IS NULL AND id_event IS NOT NULL) OR (id_club IS NOT NULL AND  id_event IS NULL)
    )
);

-- 3. Table Etudiants
CREATE TABLE IF NOT EXISTS etudiants (
    id_etudiant INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    cne TEXT UNIQUE NOT NULL, 
    email TEXT UNIQUE NOT NULL,
    id_filliere INTEGER,
    FOREIGN KEY (id_filliere) REFERENCES fillieres(id_filliere)
);
CREATE TABLE IF NOT EXISTS clubs_adhesions (
    id_adhesion INTEGER PRIMARY KEY AUTOINCREMENT,
    date_adhesion DATE DEFAULT CURRENT_DATE,
    id_club INTEGER,
    id_event INTEGER,
    FOREIGN KEY (id_club) REFERENCES clubs(id_club) ON DELETE CASCADE,
    FOREIGN KEY (id_etudiant) REFERENCES etudiant(id_etudiant) ON DELETE CASCADE,
    UNIQUE(id_club, id_etudiant)    
);

CREATE TABLE IF NOT EXISTS clubs (
    id_club INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    categroy TEXT CHECK(categroy IN ('entertaiment', 'sport', 'technologique', 'entrepreneuriat social')) NOT NULL,
);

CREATE TABLE IF NOT EXISTS fillieres (
    id_filliere INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT CHECK (nom IN ('IID1', 'GI', 'IRIC', 'GE', 'GPEE', 'MGSI')) NOT NULL,
);

CREATE TABLE IF NOT EXISTS ressources (
    id_ressource INTEGER PRIMARY KEY AUTOINCREMENT,
    type_ressource TEXT CHECK (type_ressource IN ('salle', 'Amphitheatre', 'buvet', 'Bibliotheque', 'terrain', 'labo')) NOT NULL, 
    nom TEXT NOT NULL,
);

CREATE TABLE IF NOT EXISTS reservations (
    id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    date_debut DATETIME NOT NULL,
    date_fin DATETIME NOT NULL,
    CHECK (date_fin >= date_debut),
    id_ressource INTEGER,
    id_activite INTEGER,
    FOREIGN KEY (id_ressource) REFERENCES ressources(id_ressource) ON DELETE CASCADE,
    FOREIGN KEY (id_activite) REFERENCES activite(id_activite) ON DELETE CASCADE,
    UNIQUE(id_ressource, id_activite)
);

CREATE TABLE IF NOT EXISTS events (
    id_event INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_event TEXT NOT NULL,
    date_debut DATETIME NOT NULL,
    date_fin DATETIME NOT NULL,
    CHECK (date_fin >= date_debut),
);
-- 4. Table Inscriptions
CREATE TABLE IF NOT EXISTS inscription (
    id_inscription INTEGER PRIMARY KEY AUTOINCREMENT,
    id_etudiant INTEGER NOT NULL,
    id_activite INTEGER NOT NULL,
    date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_etudiant) REFERENCES etudiant(id_etudiant) ON DELETE CASCADE,
    FOREIGN KEY (id_activite) REFERENCES activite(id_activite) ON DELETE CASCADE,
    UNIQUE(id_etudiant, id_activite) -- Prevents double booking
);