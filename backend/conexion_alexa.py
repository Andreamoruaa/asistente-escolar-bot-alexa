import ngrok

listener = ngrok.forward(5000, authtoken_from_env=True)

print(f"🚀 Túnel activo en: {listener.url()}")

# Mantiene el túnel abierto
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Túnel cerrado.")