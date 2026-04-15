CREATE DATABASE IF NOT EXISTS fixture;
USE fixture;

CREATE TABLE IF NOT EXISTS partidos (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    equipo_local VARCHAR(50) NOT NULL,
    equipo_visitante VARCHAR(50) NOT NULL,
    fecha DATETIME NOT NULL,
    fase VARCHAR(50) NOT NULL,
    goles_local INTEGER,
    goles_visitante INTEGER
);





