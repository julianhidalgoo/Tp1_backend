from flask import Blueprint,jsonify,request
from app_backend.db import get_connection


def es_id_valido(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT 1 FROM partidos WHERE id = %s """,(id,))
    partido = cursor.fetchone()

    if not partido:
        cursor.close()
        conn.close()
        return False
    
    cursor.close()
    conn.close()
    
    return True

def es_id_valido_usuarios(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT 1 FROM usuarios WHERE id = %s """,(id,))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        conn.close()
        return False
    
    cursor.close()
    conn.close()
    
    return True
    
    
    
def errores(codigo,mensaje,descripcion):
    return jsonify({
        "errors": [
            {
                "code": codigo,
                "message": mensaje,
                "description": descripcion,
                "level": "error"
            }
        ]
    }), codigo


def es_gol_valido(goles_local,goles_visitante):
    if isinstance(goles_local,int) and isinstance(goles_visitante,int):
        return True
    return False

def actualizar_puntos(id_usuario,id_partido):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""SELECT * FROM predicciones WHERE id_usuario=%s""", (id_usuario,))
    predicciones= cursor.fetchone()
    cursor.execute("""SELECT goles_local, goles_visitante FROM partidos WHERE id=%s""", (id_partido,))
    resultado_final= cursor.fetchone()

    if (predicciones["goles_local"] == resultado_final["goles_local"]) and (predicciones["goles_visitante"] == resultado_final["goles_visitante"]):
        cursor.execute("""UPDATE ranking SET puntos=3 WHERE id_usuario=%s""", (id_usuario,))
        cursor.commit()
    return 204



