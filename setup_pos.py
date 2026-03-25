import os

def create_file(path, content):
    # Obtener el directorio del path
    directory = os.path.dirname(path)
    
    # Solo intentar crear directorios si el path contiene carpetas
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ Creado: {path}")

# --- CONTENIDO DE LOS ARCHIVOS (Igual al anterior) ---

core_main = """
import importlib
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="POS Microkernel Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "POS Core Running", "plugins_url": "/docs"}

def load_plugins():
    # Buscamos la carpeta addons un nivel arriba de donde está este archivo
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    addons_path = os.path.join(base_path, "addons")
    
    if not os.path.exists(addons_path):
        print("⚠️ Carpeta addons no encontrada.")
        return

    for item in os.listdir(addons_path):
        if item.startswith("__") or not os.path.isdir(os.path.join(addons_path, item)):
            continue
        
        plugin_module = f"addons.{item}.router"
        try:
            module = importlib.import_module(plugin_module)
            if hasattr(module, "router"):
                app.include_router(module.router, prefix=f"/addons/{item}", tags=[f"Plugin: {item}"])
                print(f"📦 Plugin '{item}' inyectado dinámicamente.")
        except Exception as e:
            print(f"❌ Error al cargar {item}: {e}")

load_plugins()
"""

plugin_router = """
from fastapi import APIRouter

router = APIRouter()

@router.get("/apply")
async def apply_discount(total: float, rate: float):
    discount = total * (rate / 100)
    return {
        "status": "success",
        "original_price": total,
        "discount_applied": discount,
        "final_price": total - discount
    }
"""

admin_panel = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>POS Admin - Microkernel</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #f0f2f5; color: #333; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 600px; margin: auto; }
        h1 { color: #1a73e8; margin-top: 0; }
        .status-badge { padding: 5px 10px; border-radius: 20px; font-size: 0.9em; background: #e8f0fe; color: #1a73e8; }
        code { background: #eee; padding: 2px 5px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>POS Microkernel <span class="status-badge">Core v1.0</span></h1>
        <p>Servidor FastAPI: <strong id="server-status">Verificando...</strong></p>
        <hr>
        <p>Para probar el plugin inyectado, ve a:</p>
        <code><a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a></code>
        <p>Busca la sección <strong>"Plugin: plugin_descuentos"</strong></p>
    </div>

    <script>
        fetch('http://localhost:8000/')
            .then(() => document.getElementById('server-status').innerText = 'CONECTADO ✅')
            .catch(() => document.getElementById('server-status').innerText = 'DESCONECTADO (Inicia uvicorn) ❌');
    </script>
</body>
</html>
"""

# --- EJECUCIÓN DEL SETUP ---

def build_structure():
    files = {
        "core/main.py": core_main,
        "core/__init__.py": "",
        "addons/__init__.py": "",
        "addons/plugin_descuentos/__init__.py": "",
        "addons/plugin_descuentos/router.py": plugin_router,
        "dashboard/index.html": admin_panel,
        "requirements.txt": "fastapi\nuvicorn"
    }

    print("🏗️ Iniciando creación de arquitectura Microkernel...")
    for path, content in files.items():
        create_file(path, content)

    print("\n🚀 ¡Todo listo! Ahora ejecuta los siguientes comandos:")
    print("-" * 50)
    print("1. pip install -r requirements.txt")
    print("2. uvicorn core.main:app --reload")
    print("-" * 50)

if __name__ == "__main__":
    build_structure()
