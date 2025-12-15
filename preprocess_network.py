#!/usr/bin/env python3
"""
Script para preprocesar datos del grafo de relaciones.
Genera nodos y aristas ya procesados para la visualización de red.
"""

import json
from pathlib import Path

def procesar_grafo():
    """Procesa personajes y genera datos del grafo preprocesados"""
    data_dir = Path('data')
    
    # Cargar personajes
    with open(data_dir / 'personajes.json', 'r', encoding='utf-8') as f:
        personajes = json.load(f)
    
    nodes = []
    edges = []
    node_map = {}
    
    # Crear nodos
    for p in personajes:
        node_id = p['id']
        node_map[node_id] = p
        
        # Determinar color según rol/etiquetas
        color = '#79c0ff'  # Azul por defecto
        if 'etiquetas' in p and p['etiquetas']:
            if 'protagonista' in p['etiquetas']:
                color = '#27ae60'  # Verde
            elif 'antagonista' in p['etiquetas']:
                color = '#e74c3c'  # Rojo
            elif 'cosmico' in p['etiquetas']:
                color = '#9b59b6'  # Morado
        
        nodes.append({
            'id': node_id,
            'label': p['nombre'],
            'title': f"{p['nombre']}\n{p.get('rol', '')}",
            'color': {
                'background': color,
                'border': '#fff',
                'highlight': {
                    'background': color,
                    'border': '#fff'
                }
            },
            'font': {'color': '#fff', 'size': 14},
            'shape': 'dot',
            'size': 20
        })
        
        # Crear aristas desde relaciones
        if 'relaciones' in p and isinstance(p['relaciones'], list):
            for rel in p['relaciones']:
                if 'con' in rel and rel['con'] in node_map:
                    edges.append({
                        'from': node_id,
                        'to': rel['con'],
                        'label': rel.get('tipo', ''),
                        'title': rel.get('tipo', ''),
                        'color': {'color': '#666', 'highlight': '#79c0ff'},
                        'arrows': 'to',
                        'font': {'color': '#aaa', 'size': 10, 'align': 'middle'},
                        'smooth': {'type': 'curvedCW', 'roundness': 0.2}
                    })
    
    # Estructura de datos para vis-network
    network_data = {
        'nodes': nodes,
        'edges': edges,
        'node_map': {k: {'nombre': v['nombre'], 'rol': v.get('rol', '')} 
                     for k, v in node_map.items()}
    }
    
    # Guardar datos preprocesados
    output_dir = Path('data/processed')
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / 'network_data.json', 'w', encoding='utf-8') as f:
        json.dump(network_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Grafo preprocesado: {len(nodes)} nodos, {len(edges)} aristas")

if __name__ == '__main__':
    procesar_grafo()


