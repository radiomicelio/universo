#!/usr/bin/env python3
"""
Script para generar una imagen estática de alta calidad del grafo de relaciones.
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import networkx as nx
from pathlib import Path
import numpy as np

def generar_grafo_imagen():
    """Genera una imagen del grafo de relaciones"""
    data_dir = Path('data')
    output_dir = Path('data/processed')
    output_dir.mkdir(exist_ok=True)
    
    # Cargar personajes
    with open(data_dir / 'personajes.json', 'r', encoding='utf-8') as f:
        personajes = json.load(f)
    
    # Crear grafo dirigido
    G = nx.DiGraph()
    
    # Mapeo de IDs a nombres y colores
    node_colors = {}
    node_labels = {}
    node_sizes = {}
    
    # Definir colores según tipo
    color_map = {
        'protagonista': '#27ae60',  # Verde
        'antagonista': '#e74c3c',    # Rojo
        'cosmico': '#9b59b6',        # Morado
        'default': '#79c0ff'         # Azul
    }
    
    # Agregar nodos
    for p in personajes:
        node_id = p['id']
        node_labels[node_id] = p['nombre']
        
        # Determinar color según etiquetas
        color = color_map['default']
        if 'etiquetas' in p and p['etiquetas']:
            if 'protagonista' in p['etiquetas']:
                color = color_map['protagonista']
            elif 'antagonista' in p['etiquetas']:
                color = color_map['antagonista']
            elif 'cosmico' in p['etiquetas']:
                color = color_map['cosmico']
        
        node_colors[node_id] = color
        
        # Tamaño según importancia (principales más grandes)
        principales = ['vaquero-atomico', 'sismico', 'amethystos', 'tamen']
        if node_id in principales:
            node_sizes[node_id] = 2000
        else:
            node_sizes[node_id] = 1200
        
        G.add_node(node_id)
    
    # Agregar aristas (relaciones)
    edge_labels = {}
    for p in personajes:
        if 'relaciones' in p and isinstance(p['relaciones'], list):
            for rel in p['relaciones']:
                if 'con' in rel and rel['con'] in node_labels:
                    G.add_edge(p['id'], rel['con'])
                    edge_labels[(p['id'], rel['con'])] = rel.get('tipo', '')
    
    # Crear figura con fondo oscuro y alta resolución
    fig = plt.figure(figsize=(24, 16), facecolor='#1a1a1a', dpi=100)
    ax = fig.add_subplot(111, facecolor='#1a1a1a')
    
    # Calcular layout mejorado (usar diferentes algoritmos según el tamaño)
    if len(G.nodes()) <= 10:
        pos = nx.spring_layout(G, k=4, iterations=200, seed=42)
    else:
        # Para grafos más grandes, usar kamada_kawai para mejor distribución
        try:
            pos = nx.kamada_kawai_layout(G)
        except:
            pos = nx.spring_layout(G, k=3, iterations=150, seed=42)
    
    # Dibujar aristas
    edges = G.edges()
    edge_colors = ['#666' for _ in edges]
    nx.draw_networkx_edges(
        G, pos,
        edgelist=edges,
        edge_color=edge_colors,
        width=2,
        alpha=0.6,
        arrows=True,
        arrowsize=20,
        arrowstyle='->',
        connectionstyle='arc3,rad=0.1',
        ax=ax
    )
    
    # Dibujar etiquetas de aristas (solo las más importantes para no saturar)
    edge_labels_filtered = {k: v for k, v in edge_labels.items() if len(v) > 0 and len(v) < 30}
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels_filtered,
        font_size=8,
        font_color='#aaa',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#2a2a2a', edgecolor='none', alpha=0.7),
        ax=ax
    )
    
    # Dibujar nodos con colores y tamaños
    node_list = list(G.nodes())
    node_color_list = [node_colors[node] for node in node_list]
    node_size_list = [node_sizes.get(node, 1200) for node in node_list]
    
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=node_list,
        node_color=node_color_list,
        node_size=node_size_list,
        alpha=0.9,
        edgecolors='white',
        linewidths=2,
        ax=ax
    )
    
    # Dibujar etiquetas de nodos
    nx.draw_networkx_labels(
        G, pos,
        labels=node_labels,
        font_size=10,
        font_weight='bold',
        font_color='white',
        font_family='sans-serif',
        ax=ax
    )
    
    # Título
    ax.set_title('Red de Relaciones - Radio Micelio', 
                 fontsize=24, color='white', fontweight='bold', pad=20)
    
    # Leyenda
    legend_elements = [
        mpatches.Patch(color='#27ae60', label='Protagonistas'),
        mpatches.Patch(color='#79c0ff', label='Personajes'),
        mpatches.Patch(color='#e74c3c', label='Antagonistas'),
        mpatches.Patch(color='#9b59b6', label='Cósmicos')
    ]
    ax.legend(handles=legend_elements, loc='upper left', 
              facecolor='#2a2a2a', edgecolor='#444', 
              labelcolor='white', fontsize=12)
    
    ax.axis('off')
    plt.tight_layout()
    
    # Guardar con alta calidad (300 DPI para impresión)
    output_path = output_dir / 'network_graph.png'
    plt.savefig(output_path, dpi=300, facecolor='#1a1a1a', 
                bbox_inches='tight', format='png', 
                edgecolor='none', pad_inches=0.2)
    print(f"✓ Grafo generado: {output_path} (300 DPI)")
    
    plt.close()
    
    # También generar versión web optimizada (menor tamaño)
    fig_web = plt.figure(figsize=(20, 14), facecolor='#1a1a1a', dpi=100)
    ax_web = fig_web.add_subplot(111, facecolor='#1a1a1a')
    
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colors,
                           width=2, alpha=0.6, arrows=True, arrowsize=20,
                           arrowstyle='->', connectionstyle='arc3,rad=0.1', ax=ax_web)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_filtered,
                                 font_size=8, font_color='#aaa',
                                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#2a2a2a',
                                          edgecolor='none', alpha=0.7), ax=ax_web)
    nx.draw_networkx_nodes(G, pos, nodelist=node_list, node_color=node_color_list,
                          node_size=node_size_list, alpha=0.9, edgecolors='white',
                          linewidths=2, ax=ax_web)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10,
                           font_weight='bold', font_color='white',
                           font_family='sans-serif', ax=ax_web)
    ax_web.set_title('Red de Relaciones - Radio Micelio', 
                    fontsize=24, color='white', fontweight='bold', pad=20)
    ax_web.legend(handles=legend_elements, loc='upper left',
                 facecolor='#2a2a2a', edgecolor='#444',
                 labelcolor='white', fontsize=12)
    ax_web.axis('off')
    plt.tight_layout()
    
    output_path_web = output_dir / 'network_graph_web.png'
    plt.savefig(output_path_web, dpi=150, facecolor='#1a1a1a',
               bbox_inches='tight', format='png', edgecolor='none', pad_inches=0.2)
    print(f"✓ Grafo web generado: {output_path_web} (150 DPI)")
    plt.close()

if __name__ == '__main__':
    generar_grafo_imagen()
