from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Ruta base para verificar que la API de conexión está activa."""
    return jsonify({
        "status": "ok",
        "mensaje": "Servidor de conexión Flask activo"
    }), 200

if __name__ == '__main__':
    # Servidor local ejecutándose en el puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=True)