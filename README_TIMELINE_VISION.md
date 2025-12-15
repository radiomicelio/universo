# Timeline como Guion Expandido — Visión Radio Micelio

> Un mapa conceptual para evolucionar el sistema de timeline hacia una herramienta de escritura narrativa transmedia, inspirada en herramientas de guion pero adaptada al universo único de Radio Micelio.

---

## Visión

### El Timeline como "Guion Expandido"

El timeline de Radio Micelio no es solo una cronología. Es un **guion expandido** que captura la naturaleza transmedia del universo: eventos que pueden ser canciones, acciones, observaciones cósmicas o fragmentos de cómic, todos coexistiendo en el mismo espacio narrativo.

A diferencia de un guion cinematográfico tradicional, aquí no hay una sola línea temporal ni un único punto de vista. El timeline permite que múltiples tramas se superpongan, que eventos simultáneos se entrelacen, y que la música y los narradores no humanos tengan el mismo peso estructural que los diálogos humanos.

**El objetivo no es crear un software de guion clásico**, sino desarrollar una herramienta que respete la naturaleza experimental y transmedia de Radio Micelio, tomando lo útil de las herramientas de guion y rechazando lo que no encaja.

---

## Diferencias con el Guion Cinematográfico Tradicional

### Lo que rechazamos

- **Rigidez de actos**: No hay tres actos obligatorios ni puntos de giro predefinidos. Las tramas fluyen orgánicamente.
- **Formato hollywoodiense**: No necesitamos escenas numeradas, transiciones estándar ni márgenes específicos.
- **Diálogo obligatorio**: Una escena puede ser una canción completa, una observación de Sirius, o el silencio de Tamen detectando una anomalía.
- **Jerarquía narrativa única**: No hay una historia principal con subtramas. Hay múltiples tramas que se entrelazan sin jerarquía fija.
- **Temporalidad lineal estricta**: La simultaneidad es fundamental. Eventos que ocurren "al mismo tiempo" pueden estar en diferentes tramas.

### Lo que nos inspira (sin imitar)

Las herramientas de guion como Final Draft, Arc Studio o KIT Scenarist tienen ideas valiosas que podemos adaptar:

- **Escenas como unidades narrativas**: Una escena es una unidad de sentido, no solo un bloque de texto.
- **Metadatos invisibles**: Cada escena puede tener información oculta (lugar, tiempo, personajes) que estructura la narrativa sin saturar el texto.
- **Vistas múltiples del mismo contenido**: El mismo evento puede verse como timeline, como texto narrativo, como tarjetas, o como red de relaciones.
- **Organización por tramas**: Las tramas son filtros que permiten ver el universo desde diferentes perspectivas narrativas.

---

## Concepto de "Escena Radio Micelio"

### ¿Qué es una escena en este universo?

Una **Escena Radio Micelio** es cualquier unidad narrativa que avanza el universo, independientemente de su formato:

- **Una acción**: El Vaquero Atómico llega a Nueva York.
- **Una canción completa**: "MDMA" como evento narrativo que revela estados internos.
- **Una observación cósmica**: Sirius detecta el deshielo del diamante en el Polo Norte.
- **Un fragmento de cómic**: Una viñeta que muestra el escape de Sísmico.
- **Un silencio narrativo**: Tamen percibe una anomalía sin palabras.

**Características clave:**

- No siempre tiene diálogo.
- Puede ser simultánea con otras escenas.
- Puede pertenecer a múltiples tramas.
- Puede tener música como elemento estructural (no solo como fondo).
- Puede ser narrada por entidades no humanas (Tamen, Sirius, Micelio Negro).

### Ejemplo conceptual

Una escena puede ser:

```
Escena: "Deshielo del diamante"
Tipo: Evento cósmico
Narrador: Sirius (observación)
Simultánea con: "Señal de Sirius despierta a Sísmico"
Tramas: ["origen-nebulosa", "escape-sismico"]
Música asociada: (ninguna, o "MDMA" como eco lejano)
Personajes: Vaquero Atómico (pasivo), Sirius (activo)
Localización: Polo Norte
Etapa: Despertar
```

---

## Propuesta de Metadatos Mínimos

Cada escena/evento debería tener estos campos básicos (estructura conceptual, no código definitivo):

### Metadatos esenciales

- **id**: Identificador único (ya existe)
- **titulo**: Nombre de la escena (ya existe)
- **descripcion**: Texto narrativo de la escena (ya existe)

### Metadatos estructurales

- **tipo**: `accion` | `cancion` | `observacion` | `fragmento_comic` | `silencios`
- **narrador**: `humano` | `sirius` | `tamen` | `micelio_negro` | `ninguno`
- **personajes_implicados**: Array de IDs (ya existe)
- **localizacion**: ID de localización (ya existe)
- **etapa**: Etapa narrativa (ya existe)

### Metadatos temporales

- **simultaneo_con**: Array de IDs de escenas simultáneas (ya existe parcialmente)
- **tiempo_relativo**: Porcentaje en el timeline (0-100%) (ya existe implícitamente)

### Metadatos narrativos

- **tramas**: Array de IDs de tramas (ya existe implícitamente)
- **musica_asociada**: ID de canción si aplica (nuevo)
- **tono**: `epico` | `intimo` | `cosmico` | `caotico` | `silencioso`
- **punto_de_vista**: `vaquero` | `sismico` | `sirius` | `omnisciente` | `multiple`

### Metadatos opcionales (para futuro)

- **duracion_estimada**: Si la escena tiene duración conocida (para cómic o audio)
- **formato_original**: `cancion` | `comic` | `texto` | `audio`
- **referencias_cruzadas**: Links a otras escenas relacionadas
- **notas_internas**: Comentarios para el equipo creativo

### Ejemplo conceptual en pseudo-JSON

```json
{
  "id": "deshielo",
  "titulo": "Deshielo del diamante y despertar inicial",
  "descripcion": "El calentamiento global fractura la capa de hielo...",
  "tipo": "accion",
  "narrador": "omnisciente",
  "personajes_implicados": ["vaquero-atomico"],
  "localizacion": "polo-norte",
  "etapa": "despertar",
  "simultaneo_con": ["senal-sirius"],
  "tramas": ["origen-nebulosa"],
  "musica_asociada": null,
  "tono": "cosmico",
  "punto_de_vista": "omnisciente"
}
```

---

## Vistas Futuras del Timeline

El sistema actual tiene una **Vista Datos** (timeline visual con eventos organizados). Estas son las vistas que podrían evolucionar:

### Vista Datos (actual)

La vista cronológica visual donde los eventos se organizan por etapas y tramas. Esta es la base y debe mantenerse.

**Mejoras potenciales:**
- Filtros por tipo de escena (solo canciones, solo acciones, etc.)
- Resaltado de simultaneidades
- Zoom temporal para ver detalles de períodos específicos

### Vista Guion (texto narrativo)

Una vista que muestra las escenas como texto continuo, similar a un guion pero sin el formato rígido. Cada escena aparece como un bloque narrativo con sus metadatos visibles o colapsables.

**Características:**
- Texto fluido, no formato de guion tradicional
- Metadatos colapsables (personajes, localización, música)
- Navegación por tramas como "capítulos"
- Exportación a texto plano o markdown

### Vista Tarjetas / Index Cards

Una vista tipo Kanban donde cada escena es una tarjeta que se puede mover entre columnas (tramas, etapas, o estados de producción).

**Características:**
- Drag & drop para reorganizar
- Filtros visuales por color (tramas, tipos, tonos)
- Vista compacta para ver muchas escenas a la vez
- Útil para reestructurar narrativamente

### Vista por Tramas Superpuestas

Una vista que muestra múltiples tramas como líneas paralelas que se entrelazan, permitiendo ver cómo se cruzan y dónde convergen.

**Características:**
- Cada trama es una línea de color
- Los eventos aparecen en su trama correspondiente
- Las simultaneidades se muestran como conexiones verticales
- Zoom para ver detalles de cruces narrativos

### Vista Música

Una vista especializada que muestra las canciones como eventos narrativos principales, con sus letras y conexiones a escenas relacionadas.

**Características:**
- Canciones como bloques destacados
- Letras visibles/colapsables
- Conexiones a escenas que referencian la canción
- Timeline musical paralelo al narrativo

---

## Rol de la Música y Narradores No Humanos

### Canciones como Eventos Narrativos

En Radio Micelio, las canciones no son solo banda sonora. Son **eventos narrativos** que pueden:

- Revelar estados internos de personajes
- Avanzar la trama directamente
- Funcionar como narrador (la canción cuenta algo)
- Estar simultáneas con acciones (mientras suena "MDMA", el Vaquero Atómico hace algo)

**Implicaciones para el sistema:**
- Las canciones deben aparecer en el timeline como eventos iguales a las acciones
- Deben poder conectarse con escenas relacionadas
- Sus letras pueden ser parte del "texto narrativo" de una escena
- Pueden tener metadatos especiales (género, tempo, estado emocional)

### Tamen, Sirius, Micelio Negro como Entidades Estructurales

Estos narradores no humanos no son solo voces. Son **entidades estructurales** que:

- **Sirius**: Observa eventos cósmicos, detecta anomalías, envía señales. Su punto de vista es panorámico y temporalmente amplio.
- **Tamen**: Percibe cambios ecológicos y energéticos. Su narración es sensorial y no verbal.
- **Micelio Negro**: (Si aplica) Conecta eventos aparentemente desconectados, revela patrones ocultos.

**Implicaciones para el sistema:**
- Las escenas pueden tener un campo `narrador` que indica quién cuenta la escena
- Las vistas pueden filtrar por narrador
- Las escenas narradas por entidades no humanas pueden tener un estilo visual diferente
- La "Vista Guion" puede mostrar estas escenas con un formato especial

---

## Hoja de Ruta Suave

Esta es una propuesta de evolución gradual, enfocada en exploración más que en refactor masivo. Cada paso es pequeño y no intrusivo.

### Fase 1: Metadatos Invisibles (Exploración)

**Objetivo**: Agregar campos nuevos sin romper lo existente.

- Agregar campos opcionales `tipo`, `narrador`, `tono` a eventos existentes
- Estos campos pueden estar vacíos inicialmente
- El sistema actual sigue funcionando igual
- Crear una vista de "edición de metadatos" opcional

**Resultado**: Los datos empiezan a tener más estructura, pero nada se rompe.

### Fase 2: Vista Guion (Prototipo)

**Objetivo**: Crear una segunda vista del timeline como texto narrativo.

- Nueva página o pestaña: `timeline-guion.html`
- Muestra eventos como bloques de texto continuo
- Metadatos colapsables
- Filtros básicos (por trama, por tipo)
- No reemplaza la vista actual, la complementa

**Resultado**: Se puede ver el universo como texto narrativo, además de como timeline visual.

### Fase 3: Canciones Integradas (Exploración)

**Objetivo**: Mostrar canciones como eventos en el timeline.

- Conectar `canciones.json` con `timeline.json`
- Agregar campo `musica_asociada` a eventos
- Crear eventos de tipo `cancion` en el timeline
- Vista especial para ver solo canciones

**Resultado**: La música tiene el mismo peso narrativo que las acciones.

### Fase 4: Vista Tarjetas (Prototipo)

**Objetivo**: Crear una vista alternativa tipo Kanban.

- Nueva vista: `timeline-cards.html`
- Eventos como tarjetas arrastrables
- Organización por tramas como columnas
- Filtros visuales por color

**Resultado**: Otra forma de ver y reorganizar el universo narrativo.

### Fase 5: Simultaneidades Mejoradas (Refinamiento)

**Objetivo**: Visualizar mejor los eventos simultáneos.

- Mejorar la visualización de `simultaneo_con` en todas las vistas
- Conectar visualmente eventos simultáneos
- Filtro "mostrar solo simultaneidades"

**Resultado**: La naturaleza no lineal del universo es más clara.

### Fase 6: Narradores No Humanos (Exploración)

**Objetivo**: Dar presencia visual a los narradores no humanos.

- Agregar campo `narrador` a eventos
- Estilos visuales diferentes según narrador
- Filtro "vista desde Sirius" o "vista desde Tamen"
- Texto narrativo adaptado al punto de vista del narrador

**Resultado**: Los narradores no humanos tienen presencia estructural clara.

---

## Filosofía de Desarrollo

### Principios

1. **No romper lo existente**: Cada cambio debe ser compatible hacia atrás.
2. **Exploración sobre perfección**: Mejor un prototipo funcional que un diseño perfecto nunca implementado.
3. **Múltiples vistas, mismo dato**: Las vistas son filtros del mismo contenido, no datos separados.
4. **Metadatos invisibles**: La estructura debe estar ahí, pero no saturar la experiencia visual.
5. **Retomable en frío**: Cada fase debe poder retomarse después de semanas sin contexto.

### Criterios de Éxito

Una fase está completa cuando:

- Se puede usar sin romper nada existente
- Agrega valor sin complicar innecesariamente
- Se puede documentar en 5 minutos para alguien nuevo
- Funciona aunque algunos campos estén vacíos

---

## Notas Finales

Este documento es un **mapa conceptual**, no un plan de implementación detallado. Su propósito es:

- Recordar el **porqué** de cada decisión
- Servir como referencia cuando se retome el trabajo
- Mantener la visión clara sin perderse en detalles técnicos
- Inspirar sin constreñir

El universo de Radio Micelio es experimental y transmedia por naturaleza. El sistema de timeline debe reflejar eso: flexible, múltiple, y siempre abierto a nuevas formas de ver la narrativa.

**La meta no es crear el mejor software de guion del mundo. Es crear la mejor herramienta para escribir Radio Micelio.**

---

*Última actualización: [fecha cuando se retome]*

