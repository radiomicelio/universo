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
    eventos_por_id = {}  # Para buscar eventos por ID cuando hay simultaneidad
    for evento in timeline_data:
        etapa = evento.get('etapa', 'futuro')
        if etapa not in eventos_por_etapa:
            eventos_por_etapa[etapa] = []
        eventos_por_etapa[etapa].append(evento)
        eventos_por_id[evento['id']] = evento
    
    # Crear items con porcentajes
    fecha_base = datetime(2020, 1, 1)
    porcentajes_asignados = {}  # Para almacenar porcentajes ya asignados
    
    # Primera pasada: asignar porcentajes normales a eventos sin simultaneidad
    for etapa_key, config in etapas_config.items():
        eventos = eventos_por_etapa.get(etapa_key, [])
        
        if len(eventos) == 0:
            continue
        
        # Filtrar eventos que no tienen simultaneidad o que ya tienen porcentaje asignado
        eventos_sin_simultaneidad = [
            e for e in eventos 
            if not e.get('simultaneo_con') and e['id'] not in porcentajes_asignados
        ]
        
        if len(eventos_sin_simultaneidad) == 0:
            continue
        
        # Calcular rango de porcentajes para esta etapa
        rango_etapa = config['porcentajeFin'] - config['porcentajeInicio']
        porcentaje_por_evento = rango_etapa / len(eventos_sin_simultaneidad)
        
        for index, evento in enumerate(eventos_sin_simultaneidad):
            # Calcular porcentaje para este evento
            porcentaje_inicio = config['porcentajeInicio'] + (index * porcentaje_por_evento)
            porcentaje_fin = porcentaje_inicio + porcentaje_por_evento
            
            porcentajes_asignados[evento['id']] = {
                'inicio': porcentaje_inicio,
                'fin': porcentaje_fin,
                'etapa': etapa_key
            }
    
    # Segunda pasada: asignar porcentajes a eventos simultáneos basándose en sus referencias
    for etapa_key, config in etapas_config.items():
        eventos = eventos_por_etapa.get(etapa_key, [])
        
        for evento in eventos:
            evento_id = evento['id']
            
            # Si ya tiene porcentaje asignado, continuar
            if evento_id in porcentajes_asignados:
                continue
            
            # Si tiene simultaneo_con, usar el porcentaje del primer evento referenciado disponible
            simultaneo_con = evento.get('simultaneo_con', [])
            if simultaneo_con:
                porcentaje_encontrado = None
                for ref_id in simultaneo_con:
                    if ref_id in porcentajes_asignados:
                        porcentaje_encontrado = porcentajes_asignados[ref_id]
                        break
                
                if porcentaje_encontrado:
                    porcentajes_asignados[evento_id] = {
                        'inicio': porcentaje_encontrado['inicio'],
                        'fin': porcentaje_encontrado['fin'],
                        'etapa': etapa_key
                    }
                else:
                    # Si no se encuentra referencia, asignar normalmente
                    eventos_sin_asignar = [e for e in eventos if e['id'] not in porcentajes_asignados]
                    if eventos_sin_asignar:
                        index = eventos_sin_asignar.index(evento)
                        rango_etapa = config['porcentajeFin'] - config['porcentajeInicio']
                        porcentaje_por_evento = rango_etapa / len(eventos_sin_asignar)
                        porcentaje_inicio = config['porcentajeInicio'] + (index * porcentaje_por_evento)
                        porcentaje_fin = porcentaje_inicio + porcentaje_por_evento
                        porcentajes_asignados[evento_id] = {
                            'inicio': porcentaje_inicio,
                            'fin': porcentaje_fin,
                            'etapa': etapa_key
                        }
            else:
                # Evento sin simultaneidad que no se asignó antes, asignarlo ahora
                eventos_sin_asignar = [e for e in eventos if e['id'] not in porcentajes_asignados]
                if eventos_sin_asignar:
                    index = eventos_sin_asignar.index(evento)
                    rango_etapa = config['porcentajeFin'] - config['porcentajeInicio']
                    porcentaje_por_evento = rango_etapa / len(eventos_sin_asignar)
                    porcentaje_inicio = config['porcentajeInicio'] + (index * porcentaje_por_evento)
                    porcentaje_fin = porcentaje_inicio + porcentaje_por_evento
                    porcentajes_asignados[evento_id] = {
                        'inicio': porcentaje_inicio,
                        'fin': porcentaje_fin,
                        'etapa': etapa_key
                    }
    
    # Tercera pasada: crear items con los porcentajes asignados
    for evento in timeline_data:
        evento_id = evento['id']
        etapa_key = evento.get('etapa', 'futuro')
        config = etapas_config.get(etapa_key, etapas_config['futuro'])
        
        if evento_id not in porcentajes_asignados:
            # Fallback: asignar al final de la etapa
            porcentaje_inicio = config['porcentajeFin'] - 1
            porcentaje_fin = config['porcentajeFin']
        else:
            porcentaje_info = porcentajes_asignados[evento_id]
            porcentaje_inicio = porcentaje_info['inicio']
            porcentaje_fin = porcentaje_info['fin']
        
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
            'id': evento_id,
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

