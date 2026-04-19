from flask import jsonify, request, Blueprint
from db import get_connection
from app_backend.routes.auxiliar import es_id_valido_usuarios,errores


usuarios_bp = Blueprint("usuarios",__name__)

@usuarios_bp.route("", methods = ["GET"])
def listar_usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
    except:
        errores(500, "Error interno con la base de datos", "Internal server error")

    #paginacion, muestra los datos divididos por la cantidad especificada en limit
    limit= request.args.get("_limit", 10, type=int)
    offset= request.args.get("_offset", 0, type=int)

    if limit <= 0 or offset <0:
            cursor.close()
            conn.close()
            errores(400, "Url no encontrada", "Bad Request")
    cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
    total= cursor.fetchone()["total"]

    if not total:
        return "",204

    cursor.execute("SELECT * FROM usuarios LIMIT %s OFFSET %s", (limit, offset))
    usuarios = cursor.fetchall()
        
    base_url= request.base_url
    ultimo_offset= ((total-1)//limit) * limit if total > 0 else 0
   
    links={
       "_first": {"href": f"{base_url}?_offset=0"},
       "_prev": {"href": f"{base_url}?_offset={max(offset - limit, 0)}"},
       "_next": {"href": f"{base_url}?_offset={min(offset + limit, ultimo_offset)}"},
       "_last": {"href": f"{base_url}?_offset={ultimo_offset}"}
        }
    cursor.close()
    conn.close()
    return jsonify({
            "usuarios": usuarios,
            "_links": links
            }), 200

@usuarios_bp.route("", methods = ["POST"])
def agregar_usuario():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
    except:
         errores(500, "Error interno con la base de datos", "Internal server error")


    datos = request.json
    
    campos_requeridos = ["nombre","email"]

    for campo in campos_requeridos:
        if campo not in datos:
            cursor.close()
            conn.close()
            return errores(400,"Falta Completar algun campo","Bad Request")
        
    nombre = datos.get("nombre")
    email = datos.get("email")
    
    cursor.execute("""
                        SELECT 1 FROM usuarios WHERE email == %s 
                    """,(email,)
                )
    usuario_existe = cursor.fetchone()

    if usuario_existe:
        errores(409, "El usuario ya existe", "Conflict")
    

    cursor.execute("""INSERT INTO usuarios(nombre,email)VALUES(%s, %s)""",(nombre,email))
    conn.commit()
    cursor.close()
    conn.close()
    return "Created",201

@usuarios_bp.route("/<id>", methods = ["GET"])
def obtener_usuario_por_id(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
    except:
        errores(500, "Error interno con la base de datos", "Internal server error")
   
    if type(id)!= int or id <= 0:
        errores(404,"No se encuentra la URL", "Not Found")

    es_valido = es_id_valido_usuarios(id)
    
    if not es_valido:
        errores(400, "No se encontró el usuario", "Bad Request")
    
    cursor.execute("SELECT * FROM usuarios WHERE id = %s",(id,))
    usuario_existe= cursor.fetchone()
    cursor.close()
    conn.close()

    return jsonify({"usuario": usuario_existe}),200

@usuarios_bp.route("/<int:id>", methods = ["PUT"])
def reemplazar_usuario_por_id(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
    except: 
        errores(500, "Error interno con la base de datos", "Internal server error")

    datos = request.json
    
    campos_requeridos = ["nombre","email"]

    for campo in campos_requeridos:
        if campo not in datos:
            cursor.close()
            conn.close()
            return errores(400,"Falta Completar algun campo","Bad Request")
    
    nombre = datos.get("nombre")
    email = datos.get("email")

    cursor.execute("""
                        SELECT 1 FROM usuarios WHERE email == %s AND nombre == %s
                    """,(email,nombre,)
                )
    usuario_existe = cursor.fetchone()

    if usuario_existe:
        errores(409, "El usuario ya existe", "Conflict")
    
    cursor.execute( """UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s """,(nombre,email,id,))
    conn.commit()
    cursor.close()
    conn.close()
    return "",204

@usuarios_bp.route("/<id>", methods = ["DELETE"])
def borrar_usuario(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
    except:
        errores(500, "Error interno con la base de datos", "Internal server error")
    
    if type(id)!= int or id <= 0:
        errores(404,"No se encuentra la URL", "Not Found")

    es_valido = es_id_valido_usuarios(id)
    
    if not es_valido:
        errores(400, "No se encontró el usuario", "Bad Request")
   
    cursor.execute("""DELETE FROM usuarios WHERE id = %s""",(id,))
    conn.commit()
    cursor.close()
    conn.close()
   
    return "",204
    