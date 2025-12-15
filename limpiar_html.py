#!/usr/bin/env python3
"""
Script para limpiar HTML de los archivos JSON y dejar solo texto plano.
"""

import json
import re
from pathlib import Path
from html import unescape

def limpiar_html(texto):
    """Elimina tags HTML y decodifica entidades HTML."""
    if not texto:
        return texto
    
    # Decodificar entidades HTML (&amp; -> &, etc.)
    texto = unescape(texto)
    
    # Eliminar tags HTML y sus atributos
    texto = re.sub(r'<[^>]+>', '', texto)
    
    # Limpiar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto)
    
    return texto.strip()

def limpiar_archivo(ruta):
    """Limpia HTML de un archivo JSON."""
    archivo = Path(ruta)
    if not archivo.exists():
        print(f"⚠ Archivo no encontrado: {ruta}")
        return
    
    with open(archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    cambios = False
    
    # Limpiar campos de texto
    if isinstance(datos, dict):
        for clave, valor in datos.items():
            if isinstance(valor, str) and '<' in valor and '>' in valor:
                nuevo_valor = limpiar_html(valor)
                if nuevo_valor != valor:
                    datos[clave] = nuevo_valor
                    cambios = True
                    print(f"  ✓ Limpiado: {clave}")
            elif isinstance(valor, list):
                for item in valor:
                    if isinstance(item, dict):
                        for sub_clave, sub_valor in item.items():
                            if isinstance(sub_valor, str) and '<' in sub_valor and '>' in sub_valor:
                                nuevo_valor = limpiar_html(sub_valor)
                                if nuevo_valor != sub_valor:
                                    item[sub_clave] = nuevo_valor
                                    cambios = True
                                    print(f"  ✓ Limpiado: {item.get('titulo', 'item')}.{sub_clave}")
    
    if cambios:
        # Crear backup
        backup = archivo.with_suffix('.json.bak2')
        archivo.rename(backup)
        print(f"  📦 Backup creado: {backup.name}")
        
        # Guardar archivo limpio
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        print(f"✅ Archivo limpiado: {ruta}")
    else:
        print(f"ℹ Sin cambios: {ruta}")

if __name__ == "__main__":
    data_dir = Path("data")
    
    archivos = [
        "introduccion.json",
        "personajes.json",
        "tramas.json",
        "localizaciones.json",
        "canciones.json"
    ]
    
    print("🧹 Limpiando HTML de archivos JSON...\n")
    
    for archivo in archivos:
        ruta = data_dir / archivo
        print(f"📄 Procesando: {archivo}")
        limpiar_archivo(ruta)
        print()
    
    print("✨ Proceso completado!")


