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
('Portugal', 'Italia', '2026-07-01', 'grupo', 1, 0),
('Bélgica', 'Croacia', '2026-07-02', 'grupo', 2, 1),

('Suiza', 'Austria', '2026-07-03', 'grupo', 1, 1),
('Dinamarca', 'Suecia', '2026-07-04', 'grupo', 2, 0),
('Noruega', 'Finlandia', '2026-07-05', 'grupo', 1, 2),
('Grecia', 'Turquía', '2026-07-06', 'grupo', 0, 0),
('Irlanda', 'Escocia', '2026-07-07', 'grupo', 2, 1),
('Polonia', 'República Checa', '2026-07-08', 'grupo', 1, 1),
('Hungría', 'Rumania', '2026-07-09', 'grupo', 3, 2),
('Ucrania', 'Rusia', '2026-07-10', 'grupo', 2, 2),
('Senegal', 'Ghana', '2026-07-11', 'grupo', 1, 0),
('Costa de Marfil', 'Argelia', '2026-07-12', 'grupo', 2, 1),

('Qatar', 'Emiratos Árabes', '2026-07-13', 'grupo', NULL, NULL),
('Irán', 'Irak', '2026-07-14', 'grupo', NULL, NULL),
('China', 'India', '2026-07-15', 'grupo', NULL, NULL),
('Nueva Zelanda', 'Fiyi', '2026-07-16', 'grupo', NULL, NULL),
('Panamá', 'Honduras', '2026-07-17', 'grupo', NULL, NULL),
('El Salvador', 'Guatemala', '2026-07-18', 'grupo', NULL, NULL),
('Ecuador', 'Venezuela', '2026-07-19', 'grupo', NULL, NULL),
('Sudáfrica', 'Túnez', '2026-07-20', 'grupo', NULL, NULL),
('Camerún', 'Nigeria', '2026-07-21', 'grupo', NULL, NULL),
('Egipto', 'Marruecos', '2026-07-22', 'grupo', NULL, NULL),

('Suiza', 'Dinamarca', '2026-07-23', 'octavos', 2, 1),
('Grecia', 'Irlanda', '2026-07-24', 'octavos', 1, 0),
('Polonia', 'Hungría', '2026-07-25', 'octavos', 3, 2),
('Senegal', 'Costa de Marfil', '2026-07-26', 'octavos', 2, 2),
('Qatar', 'Irán', '2026-07-27', 'octavos', NULL, NULL),
('China', 'Nueva Zelanda', '2026-07-28', 'octavos', NULL, NULL),
('Panamá', 'Ecuador', '2026-07-29', 'octavos', NULL, NULL),
('Sudáfrica', 'Camerún', '2026-07-30', 'octavos', NULL, NULL),

('Suiza', 'Grecia', '2026-07-31', 'cuartos', 1, 0),
('Polonia', 'Senegal', '2026-08-01', 'cuartos', 2, 1);
