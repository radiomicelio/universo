# Biblia del Universo — Radio Micelio

Sistema de documentación y visualización del universo transmedia Radio Micelio.

## 🚀 Inicio Rápido

### Opción 1: Servidor Completo (Recomendado)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt
# O con conda:
conda install fastapi uvicorn python-multipart matplotlib networkx numpy

# 2. Iniciar el servidor
conda activate radio  # Si usas conda
uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# 3. Abrir index.html en tu navegador
```

### Opción 2: Solo Visualización

```bash
# Servidor HTTP simple
python -m http.server 8000
# Luego visita http://localhost:8000
```

## Características

- 📚 **Biblia completa** del universo con personajes, tramas, localizaciones y canciones
- 🎨 **Modo oscuro** como tema predeterminado
- 🔗 **Visualización de relaciones** - Grafo ontológico como imagen de alta calidad (300 DPI)
- ⏱️ **Timeline visual** - Cronología como imagen de alta calidad (300 DPI)
- ✏️ **Sistema de edición** con persistencia local
- 💾 **Guardado automático** en localStorage
- 🐍 **Preprocesamiento Python** - Scripts para optimizar datos y generar imágenes

## Visualizaciones

### Red de Relaciones
Imagen estática de alta calidad (300 DPI) que muestra las conexiones entre personajes:
- Nodos coloreados según tipo (protagonista, antagonista, cósmico)
- Aristas etiquetadas con el tipo de relación
- Generada automáticamente con Python (NetworkX + Matplotlib)
- Haz clic en la imagen para verla en alta resolución

### Timeline Visual
Imagen estática de alta calidad (300 DPI) que muestra la cronología de eventos:
- Eventos organizados por etapas con colores distintivos
- Escala de porcentajes (0-100%)
- Generada automáticamente con Python (Matplotlib)
- Haz clic en la imagen para verla en alta resolución

## Estructura

```
universo/
├── data/
│   ├── personajes.json      # Personajes del universo
│   ├── tramas.json          # Tramas narrativas
│   ├── localizaciones.json  # Lugares del universo
│   ├── canciones.json       # Canciones y su significado
│   ├── timeline.json        # Eventos cronológicos
│   ├── introduccion.json    # Logline, sinopsis, fundamentación
│   └── processed/          # Datos preprocesados (generados)
├── preprocess_*.py         # Scripts de preprocesamiento Python
├── index.html               # Aplicación principal
├── README.md               # Este archivo
└── PREPROCESSING.md        # Documentación de preprocesamiento
```

## Generación de Visualizaciones

El sistema genera imágenes estáticas de alta calidad (300 DPI) para las visualizaciones del grafo de relaciones y el timeline.

### Generar todas las visualizaciones

**Con conda (Recomendado):**
```bash
conda activate radio
python generate_network_image.py
python generate_timeline_image.py
```

**O ejecuta el script maestro que hace todo:**
```bash
conda activate radio
python preprocess_all.py
```

**Nota:** Cuando conda está activado, usa `python` (no `python3`).

### Preprocesamiento de Datos

Para mejorar el rendimiento, el proyecto incluye scripts de Python que preprocesan los datos JSON y generan versiones optimizadas:

```bash
python3 preprocess_all.py
```

Los datos preprocesados se guardan en `data/processed/` y el HTML los carga automáticamente si están disponibles. Si no existen, el sistema funciona normalmente procesando los datos en JavaScript (compatibilidad hacia atrás).

Ver [PREPROCESSING.md](PREPROCESSING.md) para más detalles.

## Publicación en GitHub Pages

1. **Sube el repositorio a GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/tu-repo.git
   git push -u origin main
   ```

2. **Habilita GitHub Pages**
   - Ve a Settings → Pages en tu repositorio
   - Selecciona la rama `main` como fuente
   - Selecciona la carpeta `/ (root)`
   - Guarda los cambios

3. **Accede a tu sitio**
   - Tu sitio estará disponible en: `https://tu-usuario.github.io/tu-repo/`

## Instalación y Configuración

### Requisitos Previos

- Python 3.8 o superior
- pip o conda (recomendado conda para las visualizaciones)

### Instalación de Dependencias

**Opción 1: Con pip**
```bash
pip install -r requirements.txt
```

**Opción 2: Con conda (recomendado)**
```bash
conda install fastapi uvicorn python-multipart matplotlib networkx numpy
```

O crea un entorno conda específico:
```bash
conda create -n radio python=3.10
conda activate radio
conda install fastapi uvicorn python-multipart matplotlib networkx numpy
```

## Uso del Sistema

### Modo 1: Servidor FastAPI (Recomendado - Permite guardar cambios)

Este modo permite guardar cambios directamente desde la interfaz web.

1. **Iniciar el servidor backend:**
   ```bash
   # Si usas conda, activa el entorno primero
   conda activate radio
   
   # Iniciar el servidor con uvicorn
   uvicorn server:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Abrir la aplicación:**
   - Abre `index.html` en tu navegador
   - O visita `http://localhost:8000` si el servidor sirve archivos estáticos

3. **Usar la interfaz:**
   - Activa el **Modo Edición** desde el header
   - Edita cualquier campo haciendo clic en él
   - Los cambios se guardan automáticamente en el servidor
   - Los archivos JSON se actualizan directamente en `data/`

**Nota:** El flag `--reload` hace que el servidor se recargue automáticamente cuando cambias el código (modo desarrollo).

### Modo 2: Servidor HTTP Simple (Solo lectura)

Si solo quieres visualizar sin guardar cambios:

```bash
# Con Python
python -m http.server 8000

# Con Node.js
npx serve

# Con PHP
php -S localhost:8000
```

Luego visita `http://localhost:8000` en tu navegador.

### Modo 3: Abrir directamente (Limitado)

Puedes abrir `index.html` directamente en el navegador, pero algunas funcionalidades (como guardar cambios) no funcionarán debido a las restricciones CORS.

## Sistema de Edición

### Con Servidor FastAPI (Recomendado)

1. Asegúrate de que el servidor esté corriendo:
   ```bash
   conda activate radio
   uvicorn server:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Activa el **Modo Edición** desde el header
3. Haz clic en cualquier campo editable para editarlo
4. Los cambios se guardan automáticamente en el servidor
5. Los archivos JSON se actualizan directamente en `data/`

### Sin Servidor (Solo lectura local)

1. Activa el **Modo Edición** desde el header
2. Haz clic en **Editar** en cualquier personaje
3. Los cambios se guardan en localStorage del navegador
4. Usa **Guardar en Archivo** para descargar el JSON actualizado
5. Reemplaza manualmente el archivo en `data/` con el descargado

## Tecnologías

- **HTML5/CSS3** - Estructura y estilos
- **JavaScript Vanilla** - Lógica de la aplicación
- **Python** - Scripts de preprocesamiento y generación de imágenes
- **Matplotlib + NetworkX** - Generación de imágenes de alta calidad
- **localStorage** - Persistencia local

## Documentación Adicional

- **[README_SERVER.md](README_SERVER.md)** - Documentación completa del servidor FastAPI
- **[README_Conda.md](README_Conda.md)** - Configuración y uso con conda
- **[PREPROCESSING.md](PREPROCESSING.md)** - Detalles sobre el preprocesamiento de datos

## Comandos Rápidos de Referencia

### Iniciar el servidor
```bash
conda activate radio
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### Generar visualizaciones
```bash
conda activate radio
python generate_network_image.py
python generate_timeline_image.py
```

### Preprocesar todos los datos
```bash
conda activate radio
python preprocess_all.py
```

### Servidor HTTP simple (solo lectura)
```bash
python -m http.server 8000
```

## Licencia

Documento interno de Radio Micelio.

