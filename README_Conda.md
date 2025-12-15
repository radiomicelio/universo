# Uso con Conda

Este proyecto usa un entorno conda llamado `radio` para ejecutar los scripts de generación de imágenes.

## Configuración inicial

### 1. Crear el entorno conda (si no existe)

```bash
conda create -n radio python=3.10 -y
```

### 2. Instalar dependencias

```bash
conda activate radio
conda install -y matplotlib networkx numpy -c conda-forge
```

O si ya tienes el entorno creado:

```bash
conda activate radio
conda install matplotlib networkx numpy -c conda-forge
```

## Ejecutar scripts

### Opción 1: Activar el entorno manualmente

**⚠️ Importante:** Cuando el entorno conda está activado, usa `python` (no `python3`):

```bash
conda activate radio
python generate_network_image.py
python generate_timeline_image.py
```

**Nota:** `python3` apunta al Python del sistema, no al del entorno conda. Usa `python` cuando conda esté activado.

### Opción 2: Usar conda run (sin activar)

```bash
conda run -n radio python generate_network_image.py
conda run -n radio python generate_timeline_image.py
```

### Opción 3: Usar el script maestro (recomendado)

El script `preprocess_all.py` está configurado para usar automáticamente el entorno conda para los scripts de imágenes:

```bash
python3 preprocess_all.py
```

Este script:
- Ejecuta los scripts normales con el Python del sistema
- Ejecuta los scripts de imágenes (`generate_network_image.py`, `generate_timeline_image.py`) usando `conda run -n radio`

## Verificar que funciona

```bash
conda run -n radio python -c "import matplotlib; import networkx; print('✓ Todo OK')"
```

## Notas

- El entorno conda `radio` solo es necesario para los scripts de generación de imágenes
- Los otros scripts de preprocesamiento (`preprocess_references.py`, etc.) funcionan con Python estándar
- Si prefieres usar pip en lugar de conda, puedes crear un entorno virtual normal


