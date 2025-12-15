#!/usr/bin/env python3
"""
Script para limpiar código JavaScript corrupto de archivos procesados.
"""

import json
import re
from pathlib import Path

def limpiar_codigo_corrupto(texto):
    """Limpia código JavaScript corrupto de un string"""
    if not texto or not isinstance(texto, str):
        return texto
    
    # Limpiar código corrupto específico que aparece comúnmente
    # Patrón 1: "'); return false;">" que aparece fuera de tags
    # Buscar este patrón específico que aparece después de cierres de tags
    texto = re.sub(r"</a>\s*'\s*;\s*return\s+false\s*[^>]*>", '</a>', texto, flags=re.IGNORECASE)
    texto = re.sub(r"'\s*;\s*return\s+false\s*[^>]*>\s*<a", '<a', texto, flags=re.IGNORECASE)
    # Limpiar cualquier instancia suelta de este patrón
    texto = re.sub(r"'\s*;\s*return\s+false\s*[^>]*>", '', texto, flags=re.IGNORECASE)
    
    # Patrón 2: "{ .; }, 300);" que aparece fuera de tags
    texto = re.sub(r'\{\s*\.\s*;\s*\}\s*,\s*\d+\s*\)\s*;', '', texto)
    
    # Normalizar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

def limpiar_objeto(obj):
    """Recursivamente limpia textos en un objeto JSON"""
    if isinstance(obj, dict):
        return {k: limpiar_objeto(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [limpiar_objeto(item) for item in obj]
    elif isinstance(obj, str):
        return limpiar_codigo_corrupto(obj)
    else:
        return obj

def limpiar_archivo(ruta_archivo):
    """Limpia un archivo procesado específico"""
    ruta = Path(ruta_archivo)
    
    if not ruta.exists():
        print(f"⚠️  Archivo no encontrado: {ruta}")
        return False
    
    try:
        # Leer archivo
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        # Crear backup
        backup_ruta = ruta.with_suffix(ruta.suffix + '.bak3')
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
    processed_dir = Path('data/processed')
    
    # Archivos procesados a limpiar
    archivos = [
        processed_dir / 'personajes_processed.json',
        processed_dir / 'localizaciones_processed.json',
        processed_dir / 'tramas_processed.json',
        processed_dir / 'canciones_processed.json',
        processed_dir / 'introduccion_processed.json',
        processed_dir / 'timeline_processed.json',
    ]
    
    print("🧹 Limpiando código corrupto de archivos procesados...\n")
    
    resultados = []
    for archivo in archivos:
        if archivo.exists():
            resultado = limpiar_archivo(archivo)
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

