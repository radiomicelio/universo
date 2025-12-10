#!/usr/bin/env python3
"""
Script maestro que ejecuta todos los preprocesadores.
"""

import subprocess
import sys
from pathlib import Path

def ejecutar_script(nombre_script, usar_conda=False):
    """Ejecuta un script de Python"""
    script_path = Path(nombre_script)
    if not script_path.exists():
        print(f"✗ Error: No se encuentra {nombre_script}")
        return False
    
    print(f"\n{'='*60}")
    print(f"Ejecutando: {nombre_script}")
    print('='*60)
    
    try:
        if usar_conda:
            # Usar conda run para ejecutar en el entorno radio
            cmd = ['conda', 'run', '-n', 'radio', 'python', str(script_path)]
        else:
            cmd = [sys.executable, str(script_path)]
        
        result = subprocess.run(
            cmd,
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
    # Scripts que no requieren conda (solo biblioteca estándar)
    scripts_normales = [
        'preprocess_references.py',
        'preprocess_network.py',
        'preprocess_timeline.py'
    ]
    
    # Scripts que requieren conda (matplotlib, networkx)
    scripts_conda = [
        'generate_network_image.py',
        'generate_timeline_image.py'
    ]
    
    print("🚀 Iniciando preprocesamiento de datos...")
    
    exitos = 0
    total = len(scripts_normales) + len(scripts_conda)
    
    # Ejecutar scripts normales
    for script in scripts_normales:
        if ejecutar_script(script, usar_conda=False):
            exitos += 1
        else:
            print(f"\n⚠️  Advertencia: {script} falló")
    
    # Ejecutar scripts que requieren conda
    for script in scripts_conda:
        if ejecutar_script(script, usar_conda=True):
            exitos += 1
        else:
            print(f"\n⚠️  Advertencia: {script} falló")
            print("   💡 Asegúrate de tener el entorno conda 'radio' activado")
            print("   💡 O ejecuta: conda activate radio")
    
    print(f"\n{'='*60}")
    print(f"✅ Preprocesamiento completado: {exitos}/{total} scripts exitosos")
    print('='*60)
    
    if exitos == total:
        print("\n✓ Todos los datos han sido preprocesados correctamente.")
        print("  Los archivos procesados están en: data/processed/")
        return 0
    else:
        print("\n⚠️  Algunos scripts fallaron. Revisa los errores arriba.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

