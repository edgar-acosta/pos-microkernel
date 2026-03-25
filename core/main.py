import importlib
import os
import sys
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="POS Microkernel")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diccionario para rastrear qué rutas ya inyectamos y evitar duplicados
INSTALLED_PLUGINS = set()

@app.get("/api/plugins")
async def list_plugins():
    return {"active_plugins": list(INSTALLED_PLUGINS)}

@app.post("/api/admin/install-runtime")
async def install_plugins_runtime():
    """Escanea la carpeta addons e inyecta lo nuevo sin reiniciar"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    addons_path = os.path.join(base_path, "addons")
    
    nuevos = 0
    for item in os.listdir(addons_path):
        if item.startswith("__") or not os.path.isdir(os.path.join(addons_path, item)):
            continue
        
        module_name = f"addons.{item}.router"
        
        # FORZAR RECARGA: Si el plugin ya existía, lo borramos del caché de Python
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "router") and item not in INSTALLED_PLUGINS:
                app.include_router(module.router, prefix=f"/addons/{item}", tags=[f"Plugin: {item}"])
                INSTALLED_PLUGINS.add(item)
                nuevos += 1
        except Exception as e:
            return {"status": "error", "message": f"Error en {item}: {str(e)}"}
            
    return {"status": "success", "added": nuevos, "total_active": len(INSTALLED_PLUGINS)}