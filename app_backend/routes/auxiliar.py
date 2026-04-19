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



