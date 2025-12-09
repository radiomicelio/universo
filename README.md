# Biblia del Universo — Radio Micelio

Sistema de documentación y visualización del universo transmedia Radio Micelio.

## Características

- 📚 **Biblia completa** del universo con personajes, tramas, localizaciones y canciones
- 🎨 **Modo oscuro** como tema predeterminado
- 🔗 **Visualización de relaciones** - Grafo ontológico interactivo de personajes
- ⏱️ **Timeline visual** - Cronología interactiva de eventos
- ✏️ **Sistema de edición** con persistencia local
- 💾 **Guardado automático** en localStorage

## Visualizaciones

### Red de Relaciones
Grafo interactivo que muestra las conexiones entre personajes:
- Nodos coloreados según tipo (protagonista, antagonista, cósmico)
- Aristas etiquetadas con el tipo de relación
- Click en nodos para ver fichas completas
- Arrastrar y zoom para explorar

### Timeline Visual
Cronología interactiva de eventos:
- Eventos organizados por etapas con colores distintivos
- Zoom y navegación temporal
- Click en eventos para ver detalles

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

## Optimización: Preprocesamiento de Datos

Para mejorar el rendimiento, el proyecto incluye scripts de Python que preprocesan los datos JSON y generan versiones optimizadas. Esto reduce significativamente el procesamiento necesario en JavaScript.

**Ejecutar preprocesamiento:**
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

## Uso Local

Simplemente abre `index.html` en tu navegador o usa un servidor local:

```bash
# Con Python
python -m http.server 8000

# Con Node.js
npx serve
```

Luego visita `http://localhost:8000`

## Sistema de Edición

1. Activa el **Modo Edición** desde el header
2. Haz click en **Editar** en cualquier personaje
3. Los cambios se guardan automáticamente en localStorage
4. Usa **Guardar en Archivo** para descargar el JSON actualizado
5. Reemplaza `data/personajes.json` con el archivo descargado

## Tecnologías

- **HTML5/CSS3** - Estructura y estilos
- **JavaScript Vanilla** - Lógica de la aplicación
- **vis-network** - Visualización de grafos
- **vis-timeline** - Timeline interactivo
- **localStorage** - Persistencia local

## Licencia

Documento interno de Radio Micelio.

