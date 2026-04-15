from flask import Blueprint,jsonify,request
from app_backend.db import get_connection
from app_backend.routes.auxiliar import es_id_valido,errores

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route('/',methods=['GET'])  #Falta paginacion y manejo de error 400 404 y 500
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



@partidos_bp.route('/', methods=['POST'])   #Falta manejo de error 409 y 500
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


@partidos_bp.route('/<int:id>', methods=['GET'])    #500  (valida el 400 en el <int:id>)
def buscar_partido_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM partidos WHERE id = %s",(id,))
    partido = cursor.fetchone()

    cursor.close()
    conn.close()
    
    if not partido:
        return jsonify({"Error": "Partido no encontrado"}), 404
    return jsonify(partido), 200


@partidos_bp.route('/<int:id_buscado>', methods=['PUT'])  # 500
def reemplazar_partido(id_buscado):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    datos = request.json

    if not es_id_valido(id_buscado):
        return jsonify({"Error": "Partido no existente"}), 404

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

# @partidos_bp.route('/partidos/<int:id_buscado>', methods=['PATCH'])
# def actualizar_partido_parcialmente(id_buscado):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
#     datos = request.json

#     cursor.execute("""
#                  SELECT id FROM partidos WHERE id = %s """, (id_buscado))
#     partido_existente = cursor.fetchone()

#     if not partido_existente:
#         cursor.close()
#         conn.close()
#         return jsonify({"Error": f"No existe el ID buscado"}), 404

#     for columna_enviada, valor in datos:
#         cursor.execute("""
#                        UPDATE partidos SET {columna_enviada} = {valor} WHERE id = %s """, (id_buscado))
      

        
    
        
@partidos_bp.route('/<int:id_a_eliminar>', methods=['DELETE']) #(suponemos que el int valida automaticamente el 400)
def eliminar_partido(id_a_eliminar):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if not es_id_valido(id_a_eliminar):
        return jsonify({"Error": "Partido no existente"}), 404
    
    cursor.execute("""
                   DELETE FROM partidos WHERE id = %s """,(id_a_eliminar,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return "" , 204
    


@partidos_bp.route('/<int:id_a_actualizar>/resultado', methods=['PUT'])
def actualizar_resultado(id_a_actualizar):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    datos = request.json    

    if not es_id_valido(id_a_actualizar):
        cursor.close()
        conn.close()
        return jsonify({"Error": "Partido no existente"}), 404
    
    campos_requeridos = ["goles_local","goles_visitante"]

    for campo in campos_requeridos:
        if campo not in datos:
             cursor.close()
             conn.close()
             return jsonify({"Error": f"falta completar el campo {campo}"}), 400


    goles_local_nuevo = datos.get("goles_local")
    goles_visitante_nuevo = datos.get("goles_visitante")

    cursor.execute("""
                   UPDATE partidos SET goles_local = %s, goles_visitante = %s
                   WHERE id = %s """,(goles_local_nuevo,goles_visitante_nuevo,id_a_actualizar))
    
    conn.commit()
    cursor.close()
    conn.close()

    return "", 204













