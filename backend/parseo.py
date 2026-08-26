from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "homeworks.db"

def obtener_todas_las_tareas_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, materia, descripcion, fecha_limite FROM tareas WHERE completada = 0 ORDER BY id DESC")
    filas = cursor.fetchall()
    conn.close()
    return filas

@app.route('/api/tareas', methods=['GET'])
def api_tareas():
    tareas = obtener_todas_las_tareas_db()
    lista_tareas = [
        {
            "id": t[0], 
            "materia": t[1], 
            "descripcion": t[2],
            "fecha_limite": t[3]
        } 
        for t in tareas
    ]
    return jsonify({"tareas": lista_tareas})

if __name__ == '__main__':
    app.run(port=5000)