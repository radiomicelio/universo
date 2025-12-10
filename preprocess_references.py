#!/usr/bin/env python3
"""
Script para preprocesar referencias en texto.
Convierte nombres de personajes, localizaciones, canciones y tramas a enlaces HTML.
"""

import json
import re
import os
from pathlib import Path

def escape_regex(text):
    """Escapa caracteres especiales para regex"""
    return re.escape(text)

def crear_enlace_personaje(id_personaje, texto, personajes):
    """Crea enlace HTML para personaje - solo data attributes, sin onclick inline"""
    personaje = next((p for p in personajes if p['id'] == id_personaje), None)
    if not personaje:
        return texto or id_personaje
    nombre = texto or personaje['nombre']
    return f'<a href="#" class="referencia-link" data-tipo="personaje" data-id="{id_personaje}">{nombre}</a>'

def crear_enlace_localizacion(id_localizacion, texto, localizaciones):
    """Crea enlace HTML para localización - solo data attributes, sin onclick inline"""
    localizacion = next((l for l in localizaciones if l['id'] == id_localizacion), None)
    if not localizacion:
        return texto or id_localizacion
    nombre = texto or localizacion['nombre']
    return f'<a href="#localizaciones" class="referencia-link" data-tipo="localizacion" data-id="{id_localizacion}">{nombre}</a>'

def crear_enlace_cancion(id_cancion, texto, canciones):
    """Crea enlace HTML para canción - solo data attributes, sin onclick inline"""
    cancion = next((c for c in canciones if c['id'] == id_cancion), None)
    if not cancion:
        return texto or id_cancion
    nombre = texto or cancion['titulo']
    return f'<a href="#canciones" class="referencia-link" data-tipo="cancion" data-id="{id_cancion}">{nombre}</a>'

def crear_enlace_trama(id_trama, texto, tramas):
    """Crea enlace HTML para trama - solo data attributes, sin onclick inline"""
    trama = next((t for t in tramas if t['id'] == id_trama), None)
    if not trama:
        return texto or id_trama
    nombre = texto or trama['titulo']
    return f'<a href="#tramas" class="referencia-link" data-tipo="trama" data-id="{id_trama}">{nombre}</a>'

def limpiar_codigo_corrupto(texto):
    """Limpia código JavaScript corrupto de un string antes de procesar"""
    if not texto:
        return texto
    
    # Limpiar código corrupto específico que aparece comúnmente
    # Patrón 1: "'); return false;">" que aparece fuera de tags
    texto = re.sub(r"'\s*;\s*return\s+false\s*[^>]*>", '', texto, flags=re.IGNORECASE)
    # Patrón 2: "{ .; }, 300);" que aparece fuera de tags
    texto = re.sub(r'\{\s*\.\s*;\s*\}\s*,\s*\d+\s*\)\s*;', '', texto)
    # Normalizar espacios
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

def procesar_referencias_en_texto(texto, personajes, localizaciones, canciones, tramas):
    """Procesa referencias en texto y las convierte a enlaces HTML"""
    if not texto:
        return texto
    
    # Limpiar código corrupto ANTES de procesar
    texto = limpiar_codigo_corrupto(texto)
    
    # Si el texto ya contiene HTML (enlaces), no procesar para evitar duplicados
    if '<a' in texto or '<span' in texto:
        return texto
    
    resultado = texto
    
    # Procesar localizaciones primero (nombres más largos primero)
    if localizaciones:
        localizaciones_ordenadas = sorted(localizaciones, 
                                         key=lambda l: len(l['nombre'].split('(')[0].strip()), 
                                         reverse=True)
        
        for l in localizaciones_ordenadas:
            nombre_completo = l['nombre']
            nombre_base = nombre_completo.split('(')[0].strip()
            
            # Escapar para regex
            nombre_completo_esc = re.escape(nombre_completo)
            nombre_completo_esc = nombre_completo_esc.replace(r'\s+', r'\s+')
            nombre_base_esc = re.escape(nombre_base)
            nombre_base_esc = nombre_base_esc.replace(r'\s+', r'\s+')
            
            # Regex para nombre completo
            regex_completo = re.compile(
                r'(^|[^\w])' + nombre_completo_esc + r'(?![\w])',
                re.IGNORECASE
            )
            
            # Reemplazar nombre completo
            def reemplazar_completo(match):
                # Verificar que no esté dentro de un enlace existente
                pos = match.start()
                antes = resultado[:pos]
                if '<a' in antes and '</a>' not in antes[antes.rfind('<a'):]:
                    return match.group(0)
                nombre_match = match.group(0).lstrip()
                if not nombre_match[0].isalnum():
                    nombre_match = nombre_match[1:]
                return match.group(1) + crear_enlace_localizacion(l['id'], nombre_match, localizaciones)
            
            resultado = regex_completo.sub(reemplazar_completo, resultado)
            
            # Si el nombre completo no coincide, intentar con el nombre base
            if nombre_base != nombre_completo and nombre_base:
                regex_base = re.compile(
                    r'(^|[^\w])' + nombre_base_esc + r'(?![\w])',
                    re.IGNORECASE
                )
                
                def reemplazar_base(match):
                    pos = match.start()
                    antes = resultado[:pos]
                    if '<a' in antes and '</a>' not in antes[antes.rfind('<a'):]:
                        return match.group(0)
                    # Verificar que no sea parte del nombre completo ya procesado
                    contexto = resultado[max(0, pos-15):min(len(resultado), pos+len(match.group(0))+15)]
                    if 'href="#"' in contexto and 'localizaciones' in contexto:
                        return match.group(0)
                    nombre_match = match.group(0).lstrip()
                    if not nombre_match[0].isalnum():
                        nombre_match = nombre_match[1:]
                    return match.group(1) + crear_enlace_localizacion(l['id'], nombre_match, localizaciones)
                
                resultado = regex_base.sub(reemplazar_base, resultado)
    
    # Procesar personajes
    if personajes:
        personajes_ordenados = sorted(personajes, key=lambda p: len(p['nombre']), reverse=True)
        
        for p in personajes_ordenados:
            nombre_esc = re.escape(p['nombre'])
            nombre_esc = nombre_esc.replace(r'\s+', r'\s+')
            regex = re.compile(
                r'(^|[^\w])' + nombre_esc + r'(?![\w])',
                re.IGNORECASE
            )
            
            def reemplazar_personaje(match):
                pos = match.start()
                antes = resultado[:pos]
                if '<a' in antes and '</a>' not in antes[antes.rfind('<a'):]:
                    return match.group(0)
                nombre_match = match.group(0).lstrip()
                if not nombre_match[0].isalnum():
                    nombre_match = nombre_match[1:]
                return match.group(1) + crear_enlace_personaje(p['id'], nombre_match, personajes)
            
            resultado = regex.sub(reemplazar_personaje, resultado)
    
    # Procesar canciones
    if canciones:
        canciones_ordenadas = sorted(canciones, key=lambda c: len(c['titulo']), reverse=True)
        
        for c in canciones_ordenadas:
            titulo_esc = re.escape(c['titulo'])
            titulo_esc = titulo_esc.replace(r'\s+', r'\s+')
            regex = re.compile(
                r'(^|[^\w])' + titulo_esc + r'(?![\w])',
                re.IGNORECASE
            )
            
            def reemplazar_cancion(match):
                pos = match.start()
                antes = resultado[:pos]
                if '<a' in antes and '</a>' not in antes[antes.rfind('<a'):]:
                    return match.group(0)
                titulo_match = match.group(0).lstrip()
                if not titulo_match[0].isalnum():
                    titulo_match = titulo_match[1:]
                return match.group(1) + crear_enlace_cancion(c['id'], titulo_match, canciones)
            
            resultado = regex.sub(reemplazar_cancion, resultado)
    
    # Procesar tramas
    if tramas:
        tramas_ordenadas = sorted(tramas, key=lambda t: len(t['titulo']), reverse=True)
        
        for t in tramas_ordenadas:
            titulo_esc = re.escape(t['titulo'])
            titulo_esc = titulo_esc.replace(r'\s+', r'\s+')
            regex = re.compile(
                r'(^|[^\w])' + titulo_esc + r'(?![\w])',
                re.IGNORECASE
            )
            
            def reemplazar_trama(match):
                pos = match.start()
                antes = resultado[:pos]
                if '<a' in antes and '</a>' not in antes[antes.rfind('<a'):]:
                    return match.group(0)
                titulo_match = match.group(0).lstrip()
                if not titulo_match[0].isalnum():
                    titulo_match = titulo_match[1:]
                return match.group(1) + crear_enlace_trama(t['id'], titulo_match, tramas)
            
            resultado = regex.sub(reemplazar_trama, resultado)
    
    return resultado

def procesar_campo_texto(obj, campo, personajes, localizaciones, canciones, tramas):
    """Procesa un campo de texto en un objeto"""
    if campo in obj and obj[campo]:
        obj[campo] = procesar_referencias_en_texto(
            obj[campo], personajes, localizaciones, canciones, tramas
        )

def procesar_array_texto(obj, campo, personajes, localizaciones, canciones, tramas):
    """Procesa un array de textos en un objeto"""
    if campo in obj and obj[campo]:
        obj[campo] = [
            procesar_referencias_en_texto(
                item, personajes, localizaciones, canciones, tramas
            )
            for item in obj[campo]
        ]

def procesar_datos():
    """Procesa todos los datos y genera versiones con referencias preprocesadas"""
    data_dir = Path('data')
    
    # Cargar datos originales
    with open(data_dir / 'personajes.json', 'r', encoding='utf-8') as f:
        personajes = json.load(f)
    
    with open(data_dir / 'localizaciones.json', 'r', encoding='utf-8') as f:
        localizaciones = json.load(f)
    
    with open(data_dir / 'canciones.json', 'r', encoding='utf-8') as f:
        canciones = json.load(f)
    
    with open(data_dir / 'tramas.json', 'r', encoding='utf-8') as f:
        tramas = json.load(f)
    
    with open(data_dir / 'introduccion.json', 'r', encoding='utf-8') as f:
        introduccion = json.load(f)
    
    with open(data_dir / 'timeline.json', 'r', encoding='utf-8') as f:
        timeline = json.load(f)
    
    # Procesar personajes
    for personaje in personajes:
        procesar_campo_texto(personaje, 'origen', personajes, localizaciones, canciones, tramas)
        procesar_campo_texto(personaje, 'descripcion', personajes, localizaciones, canciones, tramas)
        procesar_array_texto(personaje, 'motivaciones', personajes, localizaciones, canciones, tramas)
        procesar_array_texto(personaje, 'habilidades', personajes, localizaciones, canciones, tramas)
    
    # Procesar localizaciones
    for localizacion in localizaciones:
        procesar_campo_texto(localizacion, 'descripcion', personajes, localizaciones, canciones, tramas)
        procesar_array_texto(localizacion, 'elementos_clave', personajes, localizaciones, canciones, tramas)
    
    # Procesar canciones
    for cancion in canciones:
        procesar_campo_texto(cancion, 'descripcion', personajes, localizaciones, canciones, tramas)
        procesar_campo_texto(cancion, 'significado', personajes, localizaciones, canciones, tramas)
        procesar_array_texto(cancion, 'letra', personajes, localizaciones, canciones, tramas)
    
    # Procesar tramas
    for trama in tramas:
        procesar_campo_texto(trama, 'resumen', personajes, localizaciones, canciones, tramas)
    
    # Procesar introducción
    procesar_campo_texto(introduccion, 'logline', personajes, localizaciones, canciones, tramas)
    procesar_campo_texto(introduccion, 'sinopsis', personajes, localizaciones, canciones, tramas)
    procesar_campo_texto(introduccion, 'fundamentacion', personajes, localizaciones, canciones, tramas)
    if 'storyline' in introduccion:
        for item in introduccion['storyline']:
            procesar_campo_texto(item, 'resumen', personajes, localizaciones, canciones, tramas)
    
    # Procesar timeline
    for evento in timeline:
        procesar_campo_texto(evento, 'descripcion', personajes, localizaciones, canciones, tramas)
    
    # Guardar datos preprocesados
    output_dir = Path('data/processed')
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / 'personajes_processed.json', 'w', encoding='utf-8') as f:
        json.dump(personajes, f, ensure_ascii=False, indent=2)
    
    with open(output_dir / 'localizaciones_processed.json', 'w', encoding='utf-8') as f:
        json.dump(localizaciones, f, ensure_ascii=False, indent=2)
    
    with open(output_dir / 'canciones_processed.json', 'w', encoding='utf-8') as f:
        json.dump(canciones, f, ensure_ascii=False, indent=2)
    
    with open(output_dir / 'tramas_processed.json', 'w', encoding='utf-8') as f:
        json.dump(tramas, f, ensure_ascii=False, indent=2)
    
    with open(output_dir / 'introduccion_processed.json', 'w', encoding='utf-8') as f:
        json.dump(introduccion, f, ensure_ascii=False, indent=2)
    
    with open(output_dir / 'timeline_processed.json', 'w', encoding='utf-8') as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)
    
    print("✓ Referencias preprocesadas guardadas en data/processed/")

if __name__ == '__main__':
    procesar_datos()

