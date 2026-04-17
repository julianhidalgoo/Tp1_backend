from flask import Blueprint,jsonify,request
from app_backend.db import get_connection
from app_backend.routes.auxiliar import es_id_valido,errores,es_gol_valido

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route('/',methods=['GET']) 
def listar_partidos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    limit= request.args.get("_limit", 10, type=int)
    offset= request.args.get("_offset", 0, type=int)

    #Capturo los parametros de la URL
    equipo = request.args.get("equipo")
    fecha = request.args.get("fecha")
    fase = request.args.get("fase")

    solicitud = "FROM partidos WHERE 1=1"
    parametros = []
    filtros_url = ""

    if equipo: #Si manda algun equipo busco de local y visitante
        solicitud += "AND equipo_local = %s OR equipo_visitante = %s"
        parametros.extend([equipo, equipo]) #lo agrego 2 veces para los 2 %s
        filtros_url += f"&equipo={equipo}"
    if fecha:
        solicitud += "AND fecha = %s"
        parametros.append(fecha)
        filtros_url += f"&fecha={fecha}"
    if fase:
        solicitud += "AND fase = %s"
        parametros.append(fase)
        filtros_url += f"&fase={fase}"

    if limit <= 0 or offset <0:
       cursor.close()
       conn.close()
       return errores(400,"Parametros invalidos","Bad Request")
    
    cursor.execute("SELECT COUNT(*) AS total {solicitud}", parametros)
    total = cursor.fetchone()["total"]

    solicitud_partidos = f"SELECT id, equipo_local, equipo_visitante, fecha, fase {solicitud} LIMIT %s OFFSET %S"

    cursor.execute(solicitud_partidos, parametros, [limit, offset])
    partidos = cursor.fetchall()

    cursor.close()
    conn.close()

    base_url= request.base_url
    ultimo_offset= ((total-1)//limit) * limit if total > 0 else 0

    links={
    "_first": {"href": f"{base_url}?_offset=0&_limit={limit}{filtros_url}"},
    "_prev": {"href": f"{base_url}?_offset={max(offset - limit, 0)}&_limit={limit}{filtros_url}"},
    "_next": {"href": f"{base_url}?_offset={min(offset + limit, ultimo_offset)}&_limit={limit}{filtros_url}"},
    "_last": {"href": f"{base_url}?_offset={ultimo_offset}&_limit={limit}{filtros_url}"}
    }

    if not partidos:
        return "",204
    return jsonify({ "partidos": partidos,
                    "_links": links}), 200


@partidos_bp.route('/', methods=['POST'])  
def crear_partidos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    datos = request.json
  
    campos_requeridos = ["equipo_local","equipo_visitante","fecha","fase"]

    for campo in campos_requeridos:
        if campo not in datos:
            cursor.close()
            conn.close()
            return errores(400,"Falta Completar algun campo","Bad Request")
        
    equipo_local = datos.get("equipo_local")
    equipo_visitante = datos.get("equipo_visitante")
    fecha = datos.get("fecha")
    fase = datos.get("fase")

    cursor.execute("""
                   SELECT COUNT(*) AS total FROM partidos WHERE equipo_local = %s AND equipo_visitante = %s AND fecha = %s""",(equipo_local,equipo_visitante,fecha))
    existe = cursor.fetchone()["total"]

    if existe > 0:
        cursor.close()
        conn.close()
        return errores(409,"Partido ya existente","Conflict")
        

    cursor.execute("""
                   INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase)
                   VALUES (%s, %s, %s, %s)
                   """, (equipo_local,equipo_visitante,fecha,fase))

    conn.commit()
    cursor.close()
    conn.close()

    return errores(201,"Partido agregado correctamente","Created")


@partidos_bp.route('/<int:id>', methods=['GET'])  # (valida el 400 en el <int:id>) AGREGAR EL ES_ID_VALIDO y ver que sea un digito
def buscar_partido_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM partidos WHERE id = %s",(id,))
    partido = cursor.fetchone()

    cursor.close()
    conn.close()
    
    if not partido:
        return errores(404,"Partido no encontrado","Not Found")
    return jsonify({"Partido": partido}), 200


@partidos_bp.route('/<int:id_buscado>', methods=['PUT'])
def reemplazar_partido(id_buscado):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    datos = request.json

    if not es_id_valido(id_buscado):
        cursor.close()
        conn.close()
        return errores(404,"Partido no existente","Not Found")

    campos_requeridos = ["equipo_local","equipo_visitante","fecha","fase"]

    for campo in campos_requeridos:
        if campo not in datos:
            cursor.close()
            conn.close()
            return errores(400,"Falta completar alguno de los campos","Bad Request")


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


@partidos_bp.route('/<int:id_buscado>', methods=['PATCH'])
def actualizar_partido_parcialmente(id_buscado):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    datos = request.json

    if not es_id_valido(id_buscado):
        cursor.close()
        conn.close()
        return errores(404,"Id no encontrado","Not found")

    campos_posibles = ["equipo_local","equipo_visitante","fecha","fase"]

    claves = []
    valores = []

    for campo in campos_posibles:
        if campo in datos:
            claves.append(f"{campo} = %s")
            valores.append(datos[campo])

    if not claves:
        cursor.close()
        conn.close()
        return errores(400, "No se enviaron campos para actualizar", "Bad request")

    claves_recibidas = ", ".join(claves)

    instruccion_a_ejecutar = f"UPDATE partidos SET {claves_recibidas} WHERE id = %s"
    valores.append(id_buscado)

    cursor.execute(instruccion_a_ejecutar, valores)
    conn.commit()

    cursor.close()
    conn.close()

    return "", 204
    
        
@partidos_bp.route('/<int:id_a_eliminar>', methods=['DELETE']) #(suponemos que el int valida automaticamente el 400)
def eliminar_partido(id_a_eliminar):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if not es_id_valido(id_a_eliminar):
        cursor.close()
        conn.close()
        return errores(404,"Partido no existente","Not Found")
    
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
        return errores(404,"Partido no existente","Not Found")
    
    campos_requeridos = ["goles_local","goles_visitante"]

    for campo in campos_requeridos:
        if campo not in datos:
             cursor.close()
             conn.close()
             return errores(400,"Falta completar alguno de los campos","Bad Request")


    goles_local_nuevo = datos.get("goles_local")
    goles_visitante_nuevo = datos.get("goles_visitante")

    if not es_gol_valido(goles_local_nuevo,goles_visitante_nuevo) or goles_local_nuevo < 0 or goles_visitante_nuevo < 0:
        cursor.close()
        conn.close()
        return errores(400, "Error en el formato de los goles > 0 y de tipo entero", "Bad Request")
    
    
    cursor.execute("""
                   UPDATE partidos SET goles_local = %s, goles_visitante = %s
                   WHERE id = %s """,(goles_local_nuevo,goles_visitante_nuevo,id_a_actualizar))
    
    conn.commit()
    cursor.close()
    conn.close()

    return "", 204













