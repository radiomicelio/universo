#!/usr/bin/env python3
"""
Script para preprocesar datos del timeline visual.
Genera items y groups ya procesados para la visualización de timeline.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

def procesar_timeline():
    """Procesa eventos del timeline y genera datos visuales preprocesados"""
    data_dir = Path('data')
    
    # Cargar timeline
    with open(data_dir / 'timeline.json', 'r', encoding='utf-8') as f:
        timeline_data = json.load(f)
    
    items = []
    groups = []
    
    # Definir etapas y sus propiedades
    etapas_config = {
        'origen': {
            'nombre': 'Origen Cósmico',
            'color': '#9b59b6',
            'porcentajeInicio': 0,
            'porcentajeFin': 15,
            'orden': 0
        },
        'despertar': {
            'nombre': 'Despertar',
            'color': '#3498db',
            'porcentajeInicio': 15,
            'porcentajeFin': 35,
            'orden': 1
        },
        'inventrola': {
            'nombre': 'Inventrola',
            'color': '#e74c3c',
            'porcentajeInicio': 35,
            'porcentajeFin': 55,
            'orden': 2
        },
        'sismico': {
            'nombre': 'Sísmico',
            'color': '#f39c12',
            'porcentajeInicio': 55,
            'porcentajeFin': 70,
            'orden': 3
        },
        'tamen': {
            'nombre': 'Tamen y Amethystos',
            'color': '#27ae60',
            'porcentajeInicio': 70,
            'porcentajeFin': 90,
            'orden': 4
        },
        'futuro': {
            'nombre': 'Convergencia Futura',
            'color': '#1abc9c',
            'porcentajeInicio': 90,
            'porcentajeFin': 100,
            'orden': 5
        }
    }
    
    # Crear grupos por etapa
    for etapa_key, config in etapas_config.items():
        groups.append({
            'id': etapa_key,
            'content': config['nombre'],
            'className': f'timeline-group-{etapa_key}'
        })
    
    # Mapear eventos a porcentajes según etapa y orden narrativo
    eventos_por_etapa = {}
    for evento in timeline_data:
        etapa = evento.get('etapa', 'futuro')
        if etapa not in eventos_por_etapa:
            eventos_por_etapa[etapa] = []
        eventos_por_etapa[etapa].append(evento)
    
    # Crear items con porcentajes
    fecha_base = datetime(2020, 1, 1)
    
    for etapa_key, config in etapas_config.items():
        eventos = eventos_por_etapa.get(etapa_key, [])
        
        if len(eventos) == 0:
            continue
        
        # Calcular rango de porcentajes para esta etapa
        rango_etapa = config['porcentajeFin'] - config['porcentajeInicio']
        porcentaje_por_evento = rango_etapa / len(eventos)
        
        for index, evento in enumerate(eventos):
            # Calcular porcentaje para este evento
            porcentaje_inicio = config['porcentajeInicio'] + (index * porcentaje_por_evento)
            porcentaje_fin = porcentaje_inicio + porcentaje_por_evento
            
            # Convertir porcentaje a fecha (usar escala 0-100 como base de tiempo)
            fecha_inicio = fecha_base + timedelta(days=porcentaje_inicio)
            fecha_fin = fecha_base + timedelta(days=porcentaje_fin)
            
            # Determinar si es evento puntual o período
            titulo = evento.get('titulo', '')
            es_punto = (etapa_key == 'origen' or 
                       'Explosión' in titulo or 
                       'Caída' in titulo or 
                       'Aparición' in titulo)
            
            items.append({
                'id': evento['id'],
                'content': titulo[:30] + '...' if len(titulo) > 30 else titulo,
                'start': fecha_inicio.isoformat(),
                'end': None if es_punto else fecha_fin.isoformat(),
                'group': etapa_key,
                'title': f"{titulo}\n\n{evento.get('descripcion', '')}\n\nProgreso: {porcentaje_inicio:.1f}% - {porcentaje_fin:.1f}%",
                'className': f'timeline-event-{etapa_key}',
                'type': 'point' if es_punto else 'range',
                'style': f'background-color: {config["color"]}; border-color: {config["color"]}; color: #fff;'
            })
    
    # Estructura de datos para vis-timeline
    timeline_visual_data = {
        'items': items,
        'groups': groups,
        'etapas_config': etapas_config,
        'fecha_base': fecha_base.isoformat()
    }
    
    # Guardar datos preprocesados
    output_dir = Path('data/processed')
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / 'timeline_visual_data.json', 'w', encoding='utf-8') as f:
        json.dump(timeline_visual_data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✓ Timeline preprocesado: {len(items)} items, {len(groups)} grupos")

if __name__ == '__main__':
    procesar_timeline()
