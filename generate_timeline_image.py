#!/usr/bin/env python3
"""
Script para generar una imagen estática de alta calidad del timeline.
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import textwrap

def generar_timeline_imagen():
    """Genera una imagen del timeline visual"""
    data_dir = Path('data')
    output_dir = Path('data/processed')
    output_dir.mkdir(exist_ok=True)
    
    # Cargar timeline
    with open(data_dir / 'timeline.json', 'r', encoding='utf-8') as f:
        timeline_data = json.load(f)
    
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
    
    # Organizar eventos por etapa
    eventos_por_etapa = {}
    for evento in timeline_data:
        etapa = evento.get('etapa', 'futuro')
        if etapa not in eventos_por_etapa:
            eventos_por_etapa[etapa] = []
        eventos_por_etapa[etapa].append(evento)
    
    # Crear figura con alta resolución
    fig = plt.figure(figsize=(28, 14), facecolor='#1a1a1a', dpi=100)
    ax = fig.add_subplot(111, facecolor='#1a1a1a')
    
    # Altura de cada etapa
    etapa_height = 0.12
    etapa_spacing = 0.02
    
    # Dibujar etapas y eventos
    y_positions = {}
    current_y = 0.85
    
    for etapa_key in sorted(etapas_config.keys(), key=lambda k: etapas_config[k]['orden']):
        config = etapas_config[etapa_key]
        eventos = eventos_por_etapa.get(etapa_key, [])
        
        if len(eventos) == 0:
            continue
        
        y_positions[etapa_key] = current_y
        
        # Dibujar barra de etapa
        etapa_width = config['porcentajeFin'] - config['porcentajeInicio']
        rect = Rectangle(
            (config['porcentajeInicio'], current_y - etapa_height/2),
            etapa_width,
            etapa_height,
            facecolor=config['color'],
            edgecolor='white',
            linewidth=2,
            alpha=0.3,
            zorder=1
        )
        ax.add_patch(rect)
        
        # Etiqueta de etapa
        ax.text(
            (config['porcentajeInicio'] + config['porcentajeFin']) / 2,
            current_y,
            config['nombre'],
            ha='center',
            va='center',
            fontsize=14,
            fontweight='bold',
            color='white',
            zorder=3
        )
        
        # Dibujar eventos
        rango_etapa = config['porcentajeFin'] - config['porcentajeInicio']
        porcentaje_por_evento = rango_etapa / len(eventos)
        
        # Primero calcular todas las posiciones de etiquetas para evitar solapamientos
        label_positions = []
        min_label_spacing = 3.0  # Espaciado mínimo entre etiquetas en porcentaje
        
        for index, evento in enumerate(eventos):
            porcentaje_inicio = config['porcentajeInicio'] + (index * porcentaje_por_evento)
            porcentaje_fin = porcentaje_inicio + porcentaje_por_evento
            label_x = porcentaje_inicio + porcentaje_por_evento/2
            titulo = evento.get('titulo', '')
            label_text = titulo  # Mostrar texto completo sin truncar
            
            # Determinar posición Y inicial (arriba o abajo)
            # Alternar entre arriba y abajo para evitar solapamientos
            use_top = (index % 2 == 0)
            
            # Verificar colisiones con etiquetas anteriores
            label_y_offset = 0.0
            if use_top:
                base_y = current_y + etapa_height/2 + 0.02
            else:
                base_y = current_y - etapa_height/2 - 0.02
            
            # Detectar colisiones y ajustar posición
            for prev_x, prev_y, prev_width in label_positions:
                # Calcular distancia horizontal entre centros
                dist_x = abs(label_x - prev_x)
                # Si están muy cerca horizontalmente, ajustar verticalmente
                if dist_x < min_label_spacing:
                    if use_top:
                        # Si ambas están arriba, mover esta más arriba
                        if prev_y > current_y:
                            label_y_offset += 0.03
                    else:
                        # Si ambas están abajo, mover esta más abajo
                        if prev_y < current_y:
                            label_y_offset -= 0.03
            
            final_y = base_y + label_y_offset
            label_positions.append((label_x, final_y, porcentaje_por_evento))
            
            # Determinar si es evento puntual
            es_punto = (etapa_key == 'origen' or 
                       'Explosión' in titulo or 
                       'Caída' in titulo or 
                       'Aparición' in titulo)
            
            if es_punto:
                # Evento puntual: círculo
                circle = plt.Circle(
                    (porcentaje_inicio + porcentaje_por_evento/2, current_y),
                    0.015,
                    facecolor=config['color'],
                    edgecolor='white',
                    linewidth=2,
                    zorder=2
                )
                ax.add_patch(circle)
            else:
                # Evento de duración: rectángulo
                event_rect = Rectangle(
                    (porcentaje_inicio, current_y - etapa_height/3),
                    porcentaje_por_evento,
                    etapa_height/1.5,
                    facecolor=config['color'],
                    edgecolor='white',
                    linewidth=1.5,
                    alpha=0.8,
                    zorder=2
                )
                ax.add_patch(event_rect)
            
            # Dibujar línea conectora si la etiqueta está lejos
            if abs(final_y - current_y) > etapa_height/2 + 0.01:
                ax.plot([label_x, label_x], [current_y, final_y], 
                       color=config['color'], linewidth=1, alpha=0.5, zorder=2, linestyle='--')
            
            # Etiqueta del evento - dividir texto largo en múltiples líneas
            va_align = 'bottom' if final_y > current_y else 'top'
            
            # Dividir texto largo en múltiples líneas (máximo 35 caracteres por línea)
            max_chars_per_line = 35
            if len(label_text) > max_chars_per_line:
                wrapped_text = '\n'.join(textwrap.wrap(label_text, width=max_chars_per_line))
            else:
                wrapped_text = label_text
            
            ax.text(
                label_x,
                final_y,
                wrapped_text,
                ha='center',
                va=va_align,
                fontsize=7,
                color='white',
                rotation=0,
                zorder=3,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#2a2a2a', 
                         edgecolor=config['color'], alpha=0.9, linewidth=1)
            )
        
        current_y -= (etapa_height + etapa_spacing)
    
    # Configurar ejes
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1)
    ax.set_xlabel('Progreso de la Historia (%)', fontsize=16, color='white', fontweight='bold')
    ax.set_title('Timeline - Radio Micelio', fontsize=24, color='white', 
                 fontweight='bold', pad=20)
    
    # Eje X con porcentajes
    ax.set_xticks(range(0, 101, 10))
    ax.set_xticklabels([f'{i}%' for i in range(0, 101, 10)], 
                       color='#aaa', fontsize=10)
    ax.tick_params(colors='#aaa')
    
    # Ocultar eje Y
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#444')
    
    # Fondo
    ax.set_facecolor('#1a1a1a')
    
    plt.tight_layout()
    
    # Guardar con alta calidad (300 DPI para impresión)
    output_path = output_dir / 'timeline_graph.png'
    plt.savefig(output_path, dpi=300, facecolor='#1a1a1a', 
                bbox_inches='tight', format='png',
                edgecolor='none', pad_inches=0.2)
    print(f"✓ Timeline generado: {output_path} (300 DPI)")
    
    plt.close()
    
    # También generar versión web optimizada
    fig_web = plt.figure(figsize=(24, 12), facecolor='#1a1a1a', dpi=100)
    ax_web = fig_web.add_subplot(111, facecolor='#1a1a1a')
    
    current_y_web = 0.85
    for etapa_key in sorted(etapas_config.keys(), key=lambda k: etapas_config[k]['orden']):
        config = etapas_config[etapa_key]
        eventos = eventos_por_etapa.get(etapa_key, [])
        if len(eventos) == 0:
            continue
        
        rect = Rectangle((config['porcentajeInicio'], current_y_web - etapa_height/2),
                        config['porcentajeFin'] - config['porcentajeInicio'],
                        etapa_height, facecolor=config['color'], edgecolor='white',
                        linewidth=2, alpha=0.3, zorder=1)
        ax_web.add_patch(rect)
        
        ax_web.text((config['porcentajeInicio'] + config['porcentajeFin']) / 2,
                   current_y_web, config['nombre'], ha='center', va='center',
                   fontsize=14, fontweight='bold', color='white', zorder=3)
        
        rango_etapa = config['porcentajeFin'] - config['porcentajeInicio']
        porcentaje_por_evento = rango_etapa / len(eventos)
        
        # Calcular posiciones de etiquetas para evitar solapamientos (versión web)
        label_positions_web = []
        min_label_spacing = 3.0
        
        for index, evento in enumerate(eventos):
            porcentaje_inicio = config['porcentajeInicio'] + (index * porcentaje_por_evento)
            porcentaje_fin = porcentaje_inicio + porcentaje_por_evento
            label_x = porcentaje_inicio + porcentaje_por_evento/2
            titulo = evento.get('titulo', '')
            label_text = titulo  # Mostrar texto completo sin truncar
            
            use_top = (index % 2 == 0)
            label_y_offset = 0.0
            if use_top:
                base_y = current_y_web + etapa_height/2 + 0.02
            else:
                base_y = current_y_web - etapa_height/2 - 0.02
            
            for prev_x, prev_y, prev_width in label_positions_web:
                dist_x = abs(label_x - prev_x)
                if dist_x < min_label_spacing:
                    if use_top:
                        if prev_y > current_y_web:
                            label_y_offset += 0.03
                    else:
                        if prev_y < current_y_web:
                            label_y_offset -= 0.03
            
            final_y = base_y + label_y_offset
            label_positions_web.append((label_x, final_y, porcentaje_por_evento))
            
            es_punto = (etapa_key == 'origen' or 'Explosión' in titulo or 
                       'Caída' in titulo or 'Aparición' in titulo)
            
            if es_punto:
                circle = plt.Circle((porcentaje_inicio + porcentaje_por_evento/2, current_y_web),
                                  0.015, facecolor=config['color'], edgecolor='white',
                                  linewidth=2, zorder=2)
                ax_web.add_patch(circle)
            else:
                event_rect = Rectangle((porcentaje_inicio, current_y_web - etapa_height/3),
                                       porcentaje_por_evento, etapa_height/1.5,
                                       facecolor=config['color'], edgecolor='white',
                                       linewidth=1.5, alpha=0.8, zorder=2)
                ax_web.add_patch(event_rect)
            
            # Línea conectora si es necesario
            if abs(final_y - current_y_web) > etapa_height/2 + 0.01:
                ax_web.plot([label_x, label_x], [current_y_web, final_y], 
                           color=config['color'], linewidth=1, alpha=0.5, zorder=2, linestyle='--')
            
            va_align = 'bottom' if final_y > current_y_web else 'top'
            
            # Dividir texto largo en múltiples líneas (máximo 35 caracteres por línea)
            max_chars_per_line = 35
            if len(label_text) > max_chars_per_line:
                wrapped_text = '\n'.join(textwrap.wrap(label_text, width=max_chars_per_line))
            else:
                wrapped_text = label_text
            
            ax_web.text(label_x, final_y, wrapped_text, ha='center', va=va_align,
                       fontsize=7, color='white', rotation=0, zorder=3,
                       bbox=dict(boxstyle='round,pad=0.4', facecolor='#2a2a2a',
                                edgecolor=config['color'], alpha=0.9, linewidth=1))
        
        current_y_web -= (etapa_height + etapa_spacing)
    
    ax_web.set_xlim(0, 100)
    ax_web.set_ylim(0, 1)
    ax_web.set_xlabel('Progreso de la Historia (%)', fontsize=16, color='white', fontweight='bold')
    ax_web.set_title('Timeline - Radio Micelio', fontsize=24, color='white',
                    fontweight='bold', pad=20)
    ax_web.set_xticks(range(0, 101, 10))
    ax_web.set_xticklabels([f'{i}%' for i in range(0, 101, 10)], color='#aaa', fontsize=10)
    ax_web.tick_params(colors='#aaa')
    ax_web.set_yticks([])
    ax_web.spines['top'].set_visible(False)
    ax_web.spines['right'].set_visible(False)
    ax_web.spines['left'].set_visible(False)
    ax_web.spines['bottom'].set_color('#444')
    ax_web.set_facecolor('#1a1a1a')
    plt.tight_layout()
    
    output_path_web = output_dir / 'timeline_graph_web.png'
    plt.savefig(output_path_web, dpi=150, facecolor='#1a1a1a',
               bbox_inches='tight', format='png', edgecolor='none', pad_inches=0.2)
    print(f"✓ Timeline web generado: {output_path_web} (150 DPI)")
    plt.close()

if __name__ == '__main__':
    generar_timeline_imagen()
