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

def calcular_puntos(pred_local, pred_visitante, real_local, real_visitante):
    if pred_local == real_local and pred_visitante == real_visitante:
        return 3
    elif pred_local > pred_visitante and real_local > real_visitante:
        return 1
    elif pred_local < pred_visitante and real_local < real_visitante:
        return 1
    else:
        return 0

def actualizar_puntos(id_usuario, id_partido, puntos):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM predicciones WHERE id_usuario=%s AND id_partido=%s", (id_usuario, id_partido))
    prediccion = cursor.fetchone()

    cursor.execute("SELECT goles_local, goles_visitante FROM partidos WHERE id=%s", (id_partido,))
    resultado = cursor.fetchone()

    puntos = puntos + calcular_puntos(
        prediccion["goles_local"], prediccion["goles_visitante"],
        resultado["goles_local"], resultado["goles_visitante"]
    )

    cursor.execute("UPDATE ranking SET puntos = %s WHERE id_usuario=%s", (puntos, id_usuario))
    conn.commit()
    cursor.close()
    conn.close()



