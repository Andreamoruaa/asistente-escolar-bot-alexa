import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
#Name db, inicializaciones y funciones clave como consulta e inclusion
DB_N = "homeworks.db"

def init_db():
    conn = sqlite3.connect(DB_N)
    try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tareas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    materia TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    completada INTEGER DEFAULT 0,
                    fecha_limite TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    finally:
            conn.close()

def obtener_tareas_db():
    conn = sqlite3.connect(DB_N)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT materia, descripcion, fecha_limite FROM tareas WHERE completada = 0")
        filas = cursor.fetchall()
        return filas
    finally:
        conn.close()
    
def guardar_tarea_db(materia: str, descripcion: str,fecha_limite: str):
    conn = sqlite3.connect(DB_N)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tareas (materia, descripcion,fecha_limite ) VALUES (?, ?, ?)",
            (materia, descripcion,fecha_limite)
        )
        conn.commit()
    finally:
        conn.close()

# Configuracion del bot de telegram y handles (comandos)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        f"¡Hola!\n\n"
        "Soy tu bot gestor de tareas local.\n\n"
        "*¿Cómo guardar una tarea?*\n"
        "Envía un mensaje con el formato:\n"
        "`Materia | Descripción de la tarea | Fecha de entrega `\n\n"
        "*Ver tus tareas:* /tareas"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def listar_tareas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tareas = obtener_tareas_db()

    if not tareas:
        await update.message.reply_text("No tienes ninguna tarea pendiente.")
        return

    respuesta = "*Tus tareas pendientes son:*\n\n"
    for materia, descripcion, fecha_limite in tareas:
        respuesta += f"🔹 *[{materia}]* {descripcion} (Fecha Limite: {fecha_limite})\n"
    await update.message.reply_text(respuesta, parse_mode="Markdown")

async def procesar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    if "|" in texto:
        partes = texto.split("|", 2)
        materia = partes[0].strip()
        descripcion = partes[1].strip()
        fecha_limite = partes[2].strip()

        guardar_tarea_db(materia, descripcion, fecha_limite)

        await update.message.reply_text(
            f"*Guardado:*\n *Materia:* {materia}\n *Tarea:* {descripcion}\n*Fecha Limite:*{fecha_limite}",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "Formato no reconocido.\nRecuerda usar: `Materia | Tarea | Fecha Limite`",
            parse_mode="Markdown"
        )

#FUNCION MAIN 
if __name__ == '__main__':
    init_db()
    TOKEN = "Token_Teodoro"
    custom_request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0,
        pool_timeout=30.0
    )
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(custom_request)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tareas", listar_tareas))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_mensaje))
    print("Teodoro Online")
    app.run_polling(bootstrap_retries=-1)
