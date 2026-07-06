import os
from datetime import datetime

LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))

def log_action(categoria: str, accion: str, usuario_email: str, detalles: str):
    os.makedirs(LOGS_DIR, exist_ok=True)
    filename = os.path.join(LOGS_DIR, f"{categoria}.log")
    
    LIMIT_BYTES = 200 * 1024 * 1024
    if os.path.exists(filename) and os.path.getsize(filename) >= LIMIT_BYTES:
        try:
            os.remove(filename)
        except Exception as e:
            print(f"[Audit Logger] Error al borrar log excedido: {str(e)}")
            
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now_str}] [{usuario_email}] {accion.upper()}: {detalles}\n"
    
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception as e:
        print(f"[Audit Logger] Error al escribir en log {categoria}: {str(e)}")
