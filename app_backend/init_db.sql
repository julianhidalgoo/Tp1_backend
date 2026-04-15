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

INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase, goles_local, goles_visitante) VALUES
('Argentina', 'Brasil', '2026-06-10', 'grupo', 2, 1),
('Francia', 'Alemania', '2026-06-11', 'grupo', 1, 1),
('España', 'Italia', '2026-06-12', 'grupo', 3, 2),
('Inglaterra', 'Portugal', '2026-06-13', 'grupo', 2, 2),
('Uruguay', 'Chile', '2026-06-14', 'grupo', 1, 0),
('Colombia', 'Perú', '2026-06-15', 'grupo', 2, 1),
('México', 'Estados Unidos', '2026-06-16', 'grupo', 1, 3),
('Países Bajos', 'Bélgica', '2026-06-17', 'grupo', 2, 2),
('Croacia', 'Serbia', '2026-06-18', 'grupo', 1, 1),
('Japón', 'Corea del Sur', '2026-06-19', 'grupo', 2, 0),
('Argentina', 'Uruguay', '2026-06-20', 'cuartos', 3, 1),
('Brasil', 'Colombia', '2026-06-21', 'cuartos', 2, 0),
('Francia', 'España', '2026-06-22', 'cuartos', 1, 2),
('Inglaterra', 'Alemania', '2026-06-23', 'cuartos', 2, 1),
('Argentina', 'Brasil', '2026-06-25', 'semifinal', 2, 2),
('España', 'Inglaterra', '2026-06-26', 'semifinal', 1, 0),
('Brasil', 'Inglaterra', '2026-06-28', 'tercer puesto', 3, 2),
('Argentina', 'España', '2026-06-30', 'final', 2, 1),
('Portugal', 'Italia', '2026-06-18', 'grupo', 1, 0),
('Bélgica', 'Croacia', '2026-06-19', 'grupo', 2, 1);



