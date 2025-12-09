#!/usr/bin/env python3
"""
Servidor FastAPI para guardar archivos JSON desde la UI.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List
import json
import os
from pathlib import Path

app = FastAPI(title="Radio Micelio API", version="1.0.0")

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar el origen exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directorio base donde están los archivos JSON
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Montar directorio de datos como estático (para servir los JSON procesados si es necesario)
app.mount("/data", StaticFiles(directory=str(DATA_DIR)), name="data")

# Archivos permitidos para guardar (seguridad)
ALLOWED_FILES = {
    "introduccion.json",
    "personajes.json",
    "tramas.json",
    "localizaciones.json",
    "canciones.json",
    "timeline.json"
}


class SaveRequest(BaseModel):
    ruta: str
    datos: Dict[str, Any] | List[Any]


@app.get("/", response_class=HTMLResponse)
async def root():
    """Sirve el archivo index.html como página principal."""
    index_path = BASE_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    else:
        return HTMLResponse(
            content="<h1>Error</h1><p>index.html no encontrado</p>",
            status_code=404
        )


@app.post("/api/save")
async def save_file(request: SaveRequest):
    """
    Guarda datos en un archivo JSON.
    
    Args:
        request: Objeto con 'ruta' (ej: 'data/personajes.json') y 'datos' (el contenido JSON)
    
    Returns:
        Mensaje de éxito o error
    """
    try:
        # Validar que el archivo esté en la lista permitida
        nombre_archivo = request.ruta.split("/")[-1]
        if nombre_archivo not in ALLOWED_FILES:
            raise HTTPException(
                status_code=403,
                detail=f"Archivo no permitido: {nombre_archivo}"
            )
        
        # Construir ruta completa
        file_path = DATA_DIR / nombre_archivo
        
        # Validar que la ruta esté dentro del directorio permitido
        if not str(file_path.resolve()).startswith(str(DATA_DIR.resolve())):
            raise HTTPException(
                status_code=403,
                detail="Ruta no permitida"
            )
        
        # Crear backup antes de guardar
        if file_path.exists():
            backup_path = file_path.with_suffix('.json.bak')
            with open(file_path, 'r', encoding='utf-8') as f:
                backup_data = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(backup_data)
        
        # Guardar el archivo
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(request.datos, f, ensure_ascii=False, indent=2)
        
        return {
            "success": True,
            "message": f"✓ {request.ruta} guardado correctamente",
            "archivo": nombre_archivo
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar archivo: {str(e)}"
        )


@app.get("/api/files")
async def list_files():
    """Lista los archivos JSON disponibles."""
    files = []
    for filename in ALLOWED_FILES:
        file_path = DATA_DIR / filename
        if file_path.exists():
            files.append({
                "nombre": filename,
                "ruta": f"data/{filename}",
                "existe": True
            })
        else:
            files.append({
                "nombre": filename,
                "ruta": f"data/{filename}",
                "existe": False
            })
    return {"archivos": files}


if __name__ == "__main__":
    import uvicorn
    import sys
    
    print("🚀 Iniciando servidor FastAPI...")
    print(f"📁 Directorio de datos: {DATA_DIR}")
    print("🌐 Servidor disponible en: http://localhost:8000")
    print("📄 Interfaz web: http://localhost:8000/")
    print("📚 Documentación API: http://localhost:8000/docs")
    print("\n💡 Para ejecutar con uvicorn directamente (recomendado):")
    print("   uvicorn server:app --host 0.0.0.0 --port 8000 --reload\n")
    
    # Usar import string para que funcione con uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
