#!/usr/bin/env python3
"""
Script para limpiar textos corruptos en archivos JSON.
Extrae solo texto plano, eliminando código JavaScript y HTML mezclado.
"""

import json
import re
from pathlib import Path
from html import unescape

def extraer_texto_plano(texto):
    """Extrae solo texto plano de un string que puede contener HTML/JavaScript"""
    if not texto or not isinstance(texto, str):
        return texto
    
    # Si no contiene HTML, retornar tal cual
    if '<' not in texto and '>' not in texto:
        return texto.strip()
    
    # Crear un elemento temporal para extraer solo el texto
    # Usar regex para extraer texto de tags HTML
    # Primero, extraer el texto de dentro de los tags <a>
    texto_limpio = re.sub(r'<a[^>]*>([^<]*)</a>', r'\1', texto)
    
    # Eliminar todos los tags HTML restantes
    texto_limpio = re.sub(r'<[^>]+>', '', texto_limpio)
    
    # Limpiar código JavaScript residual
    texto_limpio = re.sub(r'return\s+false[^>]*>', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'onclick="[^"]*"', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'document\.getElementById\([^)]*\)', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'scrollIntoView\([^)]*\)', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'verFicha\([^)]*\)', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'event\.preventDefault\(\)', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'window\.[^;]*', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'setTimeout\([^)]*\)', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'cerrarModalSiAbierto\(\)', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'mostrarIndicadorSeccion\([^)]*\)', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'href="[^"]*"', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'class="[^"]*"', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'data-[^=]*="[^"]*"', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'behavior:\s*\'[^\']*\'', '', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'block:\s*\'[^\']*\'', '', texto_limpio, flags=re.IGNORECASE)
    
    # Decodificar entidades HTML
    texto_limpio = unescape(texto_limpio)
    
    # Normalizar espacios
    texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
    
    return texto_limpio

def limpiar_objeto(obj):
    """Recursivamente limpia textos en un objeto JSON"""
    if isinstance(obj, dict):
        return {k: limpiar_objeto(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [limpiar_objeto(item) for item in obj]
    elif isinstance(obj, str):
        return extraer_texto_plano(obj)
    else:
        return obj

def limpiar_archivo_json(ruta_archivo):
    """Limpia un archivo JSON específico"""
    ruta = Path(ruta_archivo)
    
    if not ruta.exists():
        print(f"⚠️  Archivo no encontrado: {ruta}")
        return False
    
    try:
        # Leer archivo
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        # Crear backup
        backup_ruta = ruta.with_suffix(ruta.suffix + '.bak2')
        with open(backup_ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        print(f"📦 Backup creado: {backup_ruta}")
        
        # Limpiar datos
        datos_limpios = limpiar_objeto(datos)
        
        # Guardar archivo limpio
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos_limpios, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Archivo limpiado: {ruta}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer JSON: {ruta} - {e}")
        return False
    except Exception as e:
        print(f"❌ Error al procesar {ruta}: {e}")
        return False

def main():
    """Función principal"""
    data_dir = Path('data')
    
    # Archivos JSON a limpiar
    archivos = [
        data_dir / 'personajes.json',
        data_dir / 'localizaciones.json',
        data_dir / 'tramas.json',
        data_dir / 'canciones.json',
        data_dir / 'introduccion.json',
    ]
    
    print("🧹 Limpiando textos corruptos en archivos JSON...\n")
    
    resultados = []
    for archivo in archivos:
        if archivo.exists():
            resultado = limpiar_archivo_json(archivo)
            resultados.append((archivo.name, resultado))
        else:
            print(f"⚠️  Archivo no encontrado: {archivo}")
            resultados.append((archivo.name, False))
    
    print("\n" + "="*50)
    print("📊 Resumen:")
    print("="*50)
    for nombre, exito in resultados:
        estado = "✅ Limpiado" if exito else "❌ Error"
        print(f"{estado}: {nombre}")

if __name__ == '__main__':
    main()

