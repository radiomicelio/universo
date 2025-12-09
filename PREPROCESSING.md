# Preprocesamiento de Datos

Este proyecto incluye scripts de Python para preprocesar los datos JSON y generar versiones optimizadas que reducen significativamente el procesamiento necesario en JavaScript.

## ¿Por qué preprocesar?

El procesamiento de referencias en texto, construcción de grafos y generación de datos del timeline puede ser pesado cuando se ejecuta en el navegador. Los scripts de Python realizan este trabajo una vez y generan archivos preprocesados que el JavaScript simplemente carga y muestra.

## Scripts disponibles

### 1. `preprocess_references.py`
Preprocesa referencias en texto, convirtiendo nombres de personajes, localizaciones, canciones y tramas a enlaces HTML directamente en los JSON.

**Genera:**
- `data/processed/personajes_processed.json`
- `data/processed/localizaciones_processed.json`
- `data/processed/canciones_processed.json`
- `data/processed/tramas_processed.json`
- `data/processed/introduccion_processed.json`
- `data/processed/timeline_processed.json`

### 2. `preprocess_network.py`
Preprocesa datos del grafo de relaciones, generando nodos y aristas ya estructurados para la visualización de red.

**Genera:**
- `data/processed/network_data.json`

### 3. `preprocess_timeline.py`
Preprocesa datos del timeline visual, generando items y groups ya procesados con fechas y porcentajes calculados.

**Genera:**
- `data/processed/timeline_visual_data.json`

### 4. `preprocess_all.py`
Script maestro que ejecuta todos los scripts de preprocesamiento en orden.

## Uso

### Ejecutar todos los preprocesadores

```bash
python3 preprocess_all.py
```

### Ejecutar scripts individuales

```bash
python3 preprocess_references.py
python3 preprocess_network.py
python3 preprocess_timeline.py
```

## Integración con el HTML

El archivo `index.html` está configurado para:

1. **Intentar cargar datos preprocesados primero** - Si existen en `data/processed/`, los usa automáticamente
2. **Fallback a datos originales** - Si no hay datos preprocesados, carga los originales y los procesa en JavaScript (compatibilidad hacia atrás)
3. **Detección automática** - Detecta si los textos ya contienen enlaces HTML (preprocesados) y evita procesarlos de nuevo

## Cuándo ejecutar los scripts

Ejecuta los scripts de preprocesamiento cuando:

- **Modifiques los datos JSON** - Después de editar `personajes.json`, `timeline.json`, etc.
- **Antes de desplegar** - Para optimizar el rendimiento en producción
- **Cuando el JavaScript sea lento** - Si notas que la página tarda en cargar o procesar

## Estructura de archivos

```
universo/
├── data/
│   ├── personajes.json          # Datos originales
│   ├── timeline.json
│   └── ...
├── data/processed/               # Datos preprocesados (generados)
│   ├── personajes_processed.json
│   ├── network_data.json
│   ├── timeline_visual_data.json
│   └── ...
├── preprocess_references.py     # Script de referencias
├── preprocess_network.py        # Script del grafo
├── preprocess_timeline.py       # Script del timeline
└── preprocess_all.py            # Script maestro
```

## Notas

- Los archivos procesados se generan en `data/processed/` y pueden ser versionados en git si lo deseas
- El HTML funciona tanto con datos preprocesados como sin ellos (compatibilidad hacia atrás)
- Si modificas los datos originales, recuerda ejecutar los scripts de nuevo
- Los scripts son idempotentes: puedes ejecutarlos múltiples veces sin problemas

## Requisitos

- Python 3.6 o superior
- No se requieren librerías externas (usa solo la biblioteca estándar)
