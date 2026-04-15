from flask import Flask
from app_backend.routes.partidos import partidos_bp

app = Flask(__name__)

app.register_blueprint(partidos_bp, url_prefix="/partidos")


if __name__ == '__main__':
    app.run(port=5000,debug=True)

