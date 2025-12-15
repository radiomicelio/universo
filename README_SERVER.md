# Servidor FastAPI para Radio Micelio

Este servidor permite guardar archivos JSON directamente desde la interfaz web.

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

O si usas conda:
```bash
conda install fastapi uvicorn python-multipart
```

## Uso

### Iniciar el servidor

**Opción 1: Con uvicorn directamente (recomendado para ver logs)**

Asegúrate de estar en el entorno conda "radio":
```bash
conda activate radio
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

**Opción 2: Con el script helper**
```bash
./start_server.sh
```

**Opción 3: Con Python directamente**
```bash
python server.py
```

El servidor se iniciará en `http://localhost:8000`

### Documentación de la API

Una vez iniciado, puedes ver la documentación interactiva en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### POST `/api/save`
Guarda un archivo JSON.

**Body:**
```json
{
  "ruta": "data/personajes.json",
  "datos": { ... }
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "✓ data/personajes.json guardado correctamente",
  "archivo": "personajes.json"
}
```

### GET `/api/files`
Lista los archivos JSON disponibles.

## Seguridad

El servidor solo permite guardar archivos en la lista de archivos permitidos:
- `introduccion.json`
- `personajes.json`
- `tramas.json`
- `localizaciones.json`
- `canciones.json`
- `timeline.json`

Todos los archivos se guardan en el directorio `data/` y se crea un backup automático (`.bak`) antes de sobrescribir.

## Notas

- El servidor crea backups automáticos antes de guardar
- CORS está habilitado para desarrollo (cambiar en producción)
- El servidor se recarga automáticamente cuando cambias el código (modo desarrollo)


