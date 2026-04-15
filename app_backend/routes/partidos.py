from flask import Blueprint,jsonify,request
from app_backend.db import get_connection

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route('/partidos',methods=['GET'])  #Falta paginacion y manejo de error 400 404 y 500
def listar_partidos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM partidos")
    partidos = cursor.fetchall()
    cursor.close()
    conn.close()

    if not partidos:
        return jsonify("error, no hay contenido"), 204
    return jsonify(partidos), 200



@partidos_bp.route('/partidos', methods=['POST'])   #Falta manejo de error 409 y 500
def crear_partidos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    datos = request.json
  
    campos_requeridos = ["equipo_local","equipo_visitante","fecha","fase"]

    for campo in campos_requeridos:
        if campo not in datos:
            return jsonify({"Error": f"falta completar el campo {campo}"}), 400
        
    equipo_local = datos.get("equipo_local")
    equipo_visitante = datos.get("equipo_visitante")
    fecha = datos.get("fecha")
    fase = datos.get("fase")

    cursor.execute("""
                   INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase)
                   VALUES (%s, %s, %s, %s)
                   """, (equipo_local,equipo_visitante,fecha,fase))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"Mensaje": "Partido agregado correctamente"}), 201   


@partidos_bp.route('/partidos/<int:id>', methods=['GET'])    # manejo de errores 400 y 500
def buscar_partido_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM partidos WHERE id = %s",(id))
    partido = cursor.fetchone()
    cursor.close()
    conn.close()
    if not partido:
        return ("Partido no encontrado", 404)
    return jsonify(partido), 200


@partidos_bp.route('/partidos/<int:id_buscado>', methods=['PUT'])
def actualizar_partido(id_buscado):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    datos = request.json

    campos_requeridos = ["equipo_local","equipo_visitante","fecha","fase"]

    for campo in campos_requeridos:
        if campo not in datos:
            return jsonify({"Error": f"falta completar el campo {campo}"}), 400


    local_nuevo = datos.get("equipo_local")
    visitante_nuevo = datos.get("equipo_visitante")
    fecha_nueva = datos.get("fecha")
    fase_nueva = datos.get("fase")

    
    cursor.execute("""
                   UPDATE partidos SET equipo_local = %s, equipo_visitante = %s, fecha = %s, fase = %s
                   WHERE id = %s """,(local_nuevo,visitante_nuevo,fecha_nueva,fase_nueva,id_buscado))
    
    conn.commit()
    cursor.close()
    conn.close()

    return "",204

##TERMINAR

@partidos_bp.route('/partidos/<int:id_buscado>', methods=['PATCH'])
def actualizar_partido_parcialmente(id_buscado):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    datos = request.json

    cursor.execute("""
                   SELECT id FROM partidos WHERE id = %s """, (id_buscado))
    partido_existente = cursor.fetchone()

    if not partido_existente:
        cursor.close()
        conn.close()
        return jsonify({"Error": f"No existe el ID buscado"}), 404

    for columna_enviada, valor in datos:
        cursor.execute("""
                       UPDATE partidos SET {columna_enviada} = {valor} WHERE id = %s """, (id_buscado))
        
    
        











