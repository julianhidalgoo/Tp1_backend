# Fixture y Predicciones API (Mundial 2026)

Esta es una API RESTful construida con Flask y MySQL que permite gestionar un fixture de partidos de fútbol (Mundial 2026), administrar usuarios, registrar predicciones de resultados (prode) y mantener un sistema de ranking basado en los aciertos.

## Estructura del Proyecto

El proyecto está modularizado utilizando Flask Blueprints:

```text
/ (raíz del proyecto)
└── app_backend/
    ├── init_db.sql        # Script SQL para crear la DB y poblar datos iniciales
    ├── init_db.py         # Script de Python para ejecutar el SQL
    ├── db.py              # Configuración y conexión a MySQL
    ├── app.py             # Archivo principal de ejecución de Flask
    └── routes/
        ├── auxiliar.py    # Funciones de validación y cálculo de puntos
        ├── partidos.py    # Endpoints para la gestión de partidos y resultados
        ├── ranking.py     # Endpoints para consultar la tabla de posiciones
        └── usuarios.py    # Endpoints para la gestión de usuarios
