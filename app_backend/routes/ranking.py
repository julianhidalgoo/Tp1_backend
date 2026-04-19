from flask import jsonify, request, Blueprint
from db import get_connection
from app_backend.routes.auxiliar import es_id_valido,errores

ranking_bp = Blueprint("ranking",__name__)


@ranking_bp.route("", methods = ["GET"])
def mostrar_puntaje():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
    except:
        return jsonify({"errors":[errors[3]]}),500

    #paginacion, muestra los datos divididos por la cantidad especificada en limit
    limit= request.args.get("_limit", 2, type=int)
    offset= request.args.get("_offset", 0, type=int)

    if limit <= 0 or offset <0:
            cursor.close()
            conn.close()
            return jsonify({"errors":errors[0]}), 400
    cursor.execute("SELECT COUNT(*) AS total FROM ranking")
    total= cursor.fetchone()["total"]

    if not total:
            return jsonify(),204

    cursor.execute("SELECT * FROM ranking LIMIT %s OFFSET %s", (limit, offset))
    usuarios_con_puntaje = cursor.fetchall()
        
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
            "ranking": usuarios_con_puntaje,
            "_links": links
            }), 200