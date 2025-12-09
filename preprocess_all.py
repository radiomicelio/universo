#!/usr/bin/env python3
"""
Script maestro que ejecuta todos los preprocesadores.
"""

import subprocess
import sys
from pathlib import Path

def ejecutar_script(nombre_script):
    """Ejecuta un script de Python"""
    script_path = Path(nombre_script)
    if not script_path.exists():
        print(f"✗ Error: No se encuentra {nombre_script}")
        return False
    
    print(f"\n{'='*60}")
    print(f"Ejecutando: {nombre_script}")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error ejecutando {nombre_script}:")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    """Ejecuta todos los scripts de preprocesamiento"""
    scripts = [
        'preprocess_references.py',
        'preprocess_network.py',
        'preprocess_timeline.py'
    ]
    
    print("🚀 Iniciando preprocesamiento de datos...")
    
    exitos = 0
    for script in scripts:
        if ejecutar_script(script):
            exitos += 1
        else:
            print(f"\n⚠️  Advertencia: {script} falló")
    
    print(f"\n{'='*60}")
    print(f"✅ Preprocesamiento completado: {exitos}/{len(scripts)} scripts exitosos")
    print('='*60)
    
    if exitos == len(scripts):
        print("\n✓ Todos los datos han sido preprocesados correctamente.")
        print("  Los archivos procesados están en: data/processed/")
        return 0
    else:
        print("\n⚠️  Algunos scripts fallaron. Revisa los errores arriba.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
