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

### 4. `generate_network_image.py`
Genera una imagen estática de alta calidad (PNG, 300 DPI) del grafo de relaciones usando NetworkX y Matplotlib.

**Genera:**
- `data/processed/network_graph.png`

### 5. `generate_timeline_image.py`
Genera una imagen estática de alta calidad (PNG, 300 DPI) del timeline visual usando Matplotlib.

**Genera:**
- `data/processed/timeline_graph.png`

### 6. `preprocess_all.py`
Script maestro que ejecuta todos los scripts de preprocesamiento en orden, incluyendo la generación de imágenes.

## Uso

### Ejecutar todos los preprocesadores

```bash
python3 preprocess_all.py
```

### Ejecutar scripts individuales

**Scripts normales (no requieren conda):**
```bash
python3 preprocess_references.py
python3 preprocess_network.py
python3 preprocess_timeline.py
```

**Scripts de imágenes (requieren conda):**
```bash
# Con conda activado, usa 'python' (no 'python3')
conda activate radio
python generate_network_image.py
python generate_timeline_image.py

# O sin activar conda:
conda run -n radio python generate_network_image.py
conda run -n radio python generate_timeline_image.py
```

**Nota:** Cuando conda está activado, `python3` apunta al Python del sistema. Usa `python` para los scripts que requieren conda.

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
├── data/processed/               # Datos preprocesados e imágenes (generados)
│   ├── personajes_processed.json
│   ├── network_data.json
│   ├── timeline_visual_data.json
│   ├── network_graph.png         # Imagen del grafo (300 DPI)
│   ├── network_graph_web.png     # Imagen del grafo (150 DPI, web)
│   ├── timeline_graph.png        # Imagen del timeline (300 DPI)
│   ├── timeline_graph_web.png    # Imagen del timeline (150 DPI, web)
│   └── ...
├── preprocess_references.py     # Script de referencias
├── preprocess_network.py        # Script del grafo (datos)
├── preprocess_timeline.py       # Script del timeline (datos)
├── generate_network_image.py   # Genera imagen del grafo
├── generate_timeline_image.py   # Genera imagen del timeline
├── preprocess_all.py            # Script maestro
└── requirements.txt             # Dependencias Python
```

## Notas

- Los archivos procesados se generan en `data/processed/` y pueden ser versionados en git si lo deseas
- El HTML funciona tanto con datos preprocesados como sin ellos (compatibilidad hacia atrás)
- Si modificas los datos originales, recuerda ejecutar los scripts de nuevo
- Los scripts son idempotentes: puedes ejecutarlos múltiples veces sin problemas

## Requisitos

- Python 3.6 o superior
- **Para scripts de imágenes** (requieren conda o entorno virtual):
  - `matplotlib` - Para generar imágenes de alta calidad
  - `networkx` - Para generar el grafo de relaciones
  - `numpy` - Dependencia de matplotlib

### Instalación con Conda (Recomendado)

El proyecto usa un entorno conda llamado `radio`:

```bash
# Crear entorno
conda create -n radio python=3.10 -y

# Activar e instalar dependencias
conda activate radio
conda install -y matplotlib networkx numpy -c conda-forge
```

Ver [README_Conda.md](README_Conda.md) para más detalles sobre el uso con conda.

### Instalación con pip (Alternativa)

```bash
pip install -r requirements.txt
```

O manualmente:
```bash
pip install matplotlib networkx numpy
```
