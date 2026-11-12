#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador Completo de Fútbol - Versión Corregida
Simula ligas europeas, sudamericanas y competiciones internacionales
"""

import random as rm
from collections import defaultdict
from datetime import datetime
from typing import List, Tuple, Dict
import sys
import os

# Añadir el directorio actual al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from base_datos import base_datos, Jugador, Equipo
    from conmebol import simular_copa_latina, seleccionar_mejor_jugador_america
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    print("Asegúrate de que base_datos.py y conmebol.py están en el mismo directorio")
    sys.exit(1)

def simular_partido_con_jugadores(
    equipo1: str, equipo2: str, base_datos_instancia=None
) -> Tuple[int, int, List[Dict]]:
    """
    Simula un partido entre dos equipos con estadísticas REALISTAS
    """
    datos = base_datos if base_datos_instancia is None else base_datos_instancia
    team1 = datos.obtener_equipo(equipo1)
    team2 = datos.obtener_equipo(equipo2)
    
    if not team1 or not team2:
        return 0, 0, []
    
    nivel1 = team1.calcular_nivel_equipo()
    nivel2 = team2.calcular_nivel_equipo()
    
    # Factor de ventaja por diferencia de nivel
    diferencia_nivel = abs(nivel1 - nivel2)
    factor_ventaja = 1 + (diferencia_nivel / 40)
    
    if nivel1 > nivel2:
        nivel1_ajustado = nivel1 * factor_ventaja
        nivel2_ajustado = nivel2 / factor_ventaja
    else:
        nivel1_ajustado = nivel1 / factor_ventaja
        nivel2_ajustado = nivel2 * factor_ventaja
    
    gol1, gol2 = 0, 0
    eventos = []
    sumalevel = nivel1_ajustado + nivel2_ajustado
    
    # Actualizar partidos jugados y minutos
    for jugador in team1.jugadores:
        jugador.partidos_jugados += 1
        jugador.minutos_jugados += 90
        
    for jugador in team2.jugadores:
        jugador.partidos_jugados += 1
        jugador.minutos_jugados += 90
    
    # SIMULACIÓN CON ESTADÍSTICAS REALISTAS
    for minuto in range(1, 91):
        prob = rm.randint(1, 200)
        
        # OPORTUNIDADES DE GOL REALISTAS (2.5% por minuto)
        if prob > 195:
            prob2 = rm.randint(0, int(sumalevel))
            
            equipo_atacante = team1 if prob2 <= nivel1_ajustado else team2
            goleador, asistente = seleccionar_goleador_y_asistente(equipo_atacante)
            
            if goleador:
                # PROBABILIDAD DE CONVERSIÓN REALISTA
                efectividad_base = 0.25
                bonus_nivel = (goleador.nivel - 80) / 100
                probabilidad_gol = min(0.40, max(0.15, efectividad_base + bonus_nivel))
                
                if rm.random() < probabilidad_gol:
                    goleador.goles += 1
                    if equipo_atacante == team1:
                        gol1 += 1
                    else:
                        gol2 += 1
                    
                    evento = {
                        'minuto': minuto,
                        'tipo': 'gol',
                        'equipo': equipo1 if equipo_atacante == team1 else equipo2,
                        'goleador': goleador.nombre,
                        'asistente': asistente.nombre if asistente else None
                    }
                    eventos.append(evento)
                    
                    if asistente:
                        asistente.asistencias += 1
        
        # Tarjetas (proporcionales)
        if prob < 8:  # 4% para amarilla
            equipo_tarjeta = team1 if rm.randint(0, int(sumalevel)) <= nivel1_ajustado else team2
            jugador_tarjeta = rm.choice([j for j in equipo_tarjeta.jugadores if j.posicion in ["DEF", "MED"]])
            jugador_tarjeta.tarjetas_amarillas += 1
            eventos.append({
                'minuto': minuto,
                'tipo': 'tarjeta_amarilla',
                'equipo': equipo1 if equipo_tarjeta == team1 else equipo2,
                'jugador': jugador_tarjeta.nombre
            })
        elif prob == 1:  # 0.5% para roja
            equipo_tarjeta = team1 if rm.randint(0, int(sumalevel)) <= nivel1_ajustado else team2
            jugador_tarjeta = rm.choice(equipo_tarjeta.jugadores)
            jugador_tarjeta.tarjetas_rojas += 1
            eventos.append({
                'minuto': minuto,
                'tipo': 'tarjeta_roja',
                'equipo': equipo1 if equipo_tarjeta == team1 else equipo2,
                'jugador': jugador_tarjeta.nombre
            })
    
    return gol1, gol2, eventos

def seleccionar_goleador_y_asistente(equipo: Equipo) -> Tuple[Jugador, Jugador]:
    """
    Selecciona quién marca el gol y quién da la asistencia
    """
    prob_gol = {
        "DEL": 0.7,
        "MED": 0.25,
        "DEF": 0.04,
        "POR": 0.01
    }
    
    prob_asist = {
        "MED": 0.6,
        "DEL": 0.3,
        "DEF": 0.08,
        "POR": 0.02
    }
    
    jugadores_ordenados = sorted(equipo.jugadores, key=lambda x: x.nivel, reverse=True)
    
    # Seleccionar goleador
    goleador = None
    for jugador in jugadores_ordenados:
        prob_posicion = prob_gol.get(jugador.posicion, 0.1)
        prob_nivel = jugador.nivel / 100.0
        prob_final = prob_posicion * prob_nivel * 1.8
        
        if rm.random() < prob_final:
            goleador = jugador
            break
    
    if not goleador:
        goleador = jugadores_ordenados[0]
    
    # Seleccionar asistente
    asistente = None
    jugadores_sin_goleador = [j for j in jugadores_ordenados if j != goleador]
    
    for jugador in jugadores_sin_goleador:
        prob_posicion = prob_asist.get(jugador.posicion, 0.1)
        prob_nivel = jugador.nivel / 100.0
        prob_final = prob_posicion * prob_nivel * 1.5
        
        if rm.random() < prob_final:
            asistente = jugador
            break
    
    if rm.random() < 0.3:
        asistente = None
    
    return goleador, asistente

def simular_liga_con_jugadores(nombre_liga: str, equipos_dict: Dict[str, int]) -> List[Tuple[str, Dict]]:
    """Simula una liga completa registrando estadísticas de jugadores"""
    equipos_lista = list(equipos_dict.keys())
    tabla = defaultdict(lambda: {'puntos': 0, 'gf': 0, 'gc': 0, 'partidos': 0, 'gd': 0})
    
    print(f"  Simulando partidos de {nombre_liga}...")
    partidos_total = len(equipos_lista) * (len(equipos_lista) - 1)
    partidos_simulados = 0
    
    # Todos contra todos (ida y vuelta)
    for i in range(len(equipos_lista)):
        for j in range(len(equipos_lista)):
            if i != j:
                equipo1 = equipos_lista[i]
                equipo2 = equipos_lista[j]
                
                gol1, gol2, eventos = simular_partido_con_jugadores(equipo1, equipo2)
                
                # Actualizar tabla
                tabla[equipo1]['gf'] += gol1
                tabla[equipo1]['gc'] += gol2
                tabla[equipo1]['partidos'] += 1
                tabla[equipo2]['gf'] += gol2
                tabla[equipo2]['gc'] += gol1
                tabla[equipo2]['partidos'] += 1
                
                if gol1 > gol2:
                    tabla[equipo1]['puntos'] += 3
                elif gol1 < gol2:
                    tabla[equipo2]['puntos'] += 3
                else:
                    tabla[equipo1]['puntos'] += 1
                    tabla[equipo2]['puntos'] += 1
                
                partidos_simulados += 1
                if partidos_simulados % 100 == 0:
                    progreso = (partidos_simulados / partidos_total) * 100
                    print(f"    Progreso: {progreso:.1f}% ({partidos_simulados}/{partidos_total})")
    
    # Calcular diferencia de goles
    for equipo in tabla:
        tabla[equipo]['gd'] = tabla[equipo]['gf'] - tabla[equipo]['gc']
    
    # Ordenar tabla
    tabla_ordenada = sorted(tabla.items(), 
                           key=lambda x: (x[1]['puntos'], x[1]['gd'], x[1]['gf']), 
                           reverse=True)
    
    # Registrar campeón de liga
    if tabla_ordenada:
        campeon_liga = tabla_ordenada[0][0]
        base_datos.registrar_campeon(nombre_liga, campeon_liga)
    
    return tabla_ordenada

def simular_eliminatoria_con_jugadores(equipo1: str, equipo2: str) -> Tuple[str, str]:
    """Simula una eliminatoria a doble partido"""
    # Ida
    gol1_ida, gol2_ida, eventos_ida = simular_partido_con_jugadores(equipo1, equipo2)
    # Vuelta
    gol2_vuelta, gol1_vuelta, eventos_vuelta = simular_partido_con_jugadores(equipo2, equipo1)
    
    total1 = gol1_ida + gol1_vuelta
    total2 = gol2_ida + gol2_vuelta
    
    resultado = f"{equipo1.upper()} {gol1_ida}-{gol2_ida} {equipo2.upper()} | {equipo2.upper()} {gol2_vuelta}-{gol1_vuelta} {equipo1.upper()} | AGG: {total1}-{total2}"
    
    if total1 > total2:
        return equipo1, resultado
    elif total2 > total1:
        return equipo2, resultado
    else:
        # Goles de visitante
        if gol2_ida > gol1_vuelta:
            return equipo2, resultado + f" - {equipo2.upper()} por goles visitante"
        elif gol1_vuelta > gol2_ida:
            return equipo1, resultado + f" - {equipo1.upper()} por goles visitante"
        else:
            # Penales
            nivel1 = base_datos.obtener_nivel_equipo(equipo1)
            nivel2 = base_datos.obtener_nivel_equipo(equipo2)
            prob_pen = rm.randint(0, nivel1 + nivel2)
            ganador = equipo1 if prob_pen <= nivel1 else equipo2
            return ganador, resultado + f" - {ganador.upper()} por penales"

def simular_final_con_jugadores(equipo1: str, equipo2: str) -> Tuple[str, str]:
    """Simula una final"""
    nivel1 = base_datos.obtener_nivel_equipo(equipo1)
    nivel2 = base_datos.obtener_nivel_equipo(equipo2)
    
    goles1, goles2, eventos = simular_partido_con_jugadores(equipo1, equipo2)
    resultado = f"{equipo1.upper()} {goles1}-{goles2} {equipo2.upper()}"
    
    if goles1 > goles2:
        return equipo1, resultado
    elif goles2 > goles1:
        return equipo2, resultado
    else:
        # Penales
        prob_pen = rm.randint(0, nivel1 + nivel2)
        ganador = equipo1 if prob_pen <= nivel1 else equipo2
        return ganador, resultado + f" - {ganador.upper()} por penales"

def es_equipo_europeo(codigo_equipo: str) -> bool:
    """Verifica si un equipo es europeo basándose en su liga"""
    equipo = base_datos.obtener_equipo(codigo_equipo)
    if not equipo:
        return False
    
    LIGAS_EUROPEAS = ["Premier League", "La Liga", "Serie A", "Bundesliga", 
                      "Ligue 1", "Primeira Liga", "Eredivisie"]
    
    return equipo.liga in LIGAS_EUROPEAS

def obtener_clasificados_europeos(resultados_ligas: Dict) -> Tuple[List[str], List[str], List[str]]:
    """Obtiene los equipos clasificados para cada competición europea - SOLO EQUIPOS EUROPEOS"""
    champions = []
    europa = []
    conference = []
    
    # LIGAS EUROPEAS ÚNICAMENTE
    LIGAS_EUROPEAS = ["Premier League", "La Liga", "Serie A", "Bundesliga", 
                      "Ligue 1", "Primeira Liga", "Eredivisie"]
    
    print("\n🌍 Clasificando equipos SOLO EUROPEOS para competiciones UEFA...")
    
    for liga, tabla in resultados_ligas.items():
        # FILTRO ESTRICTO: Solo ligas europeas
        if liga not in LIGAS_EUROPEAS:
            print(f"   ❌ Saltando {liga} (NO es europea)")
            continue
        
        print(f"   ✅ Procesando {liga} (liga europea)")
            
        if liga in ["Premier League", "La Liga", "Serie A", "Bundesliga"]:
            # Verificar que cada equipo sea europeo
            for i in range(min(4, len(tabla))):
                equipo = tabla[i][0]
                if es_equipo_europeo(equipo):
                    champions.append(equipo)
                else:
                    print(f"      ⚠️  ADVERTENCIA: {equipo} NO es europeo, omitiendo")
            
            for i in range(4, min(6, len(tabla))):
                equipo = tabla[i][0]
                if es_equipo_europeo(equipo):
                    europa.append(equipo)
                    
            if len(tabla) > 6:
                equipo = tabla[6][0]
                if es_equipo_europeo(equipo):
                    conference.append(equipo)
                    
        elif liga == "Ligue 1":
            for i in range(min(3, len(tabla))):
                equipo = tabla[i][0]
                if es_equipo_europeo(equipo):
                    champions.append(equipo)
                    
            if len(tabla) > 3:
                equipo = tabla[3][0]
                if es_equipo_europeo(equipo):
                    europa.append(equipo)
                    
            if len(tabla) > 4:
                equipo = tabla[4][0]
                if es_equipo_europeo(equipo):
                    conference.append(equipo)
                    
        elif liga == "Primeira Liga":
            for i in range(min(2, len(tabla))):
                equipo = tabla[i][0]
                if es_equipo_europeo(equipo):
                    champions.append(equipo)
                    
            for i in range(2, min(4, len(tabla))):
                equipo = tabla[i][0]
                if es_equipo_europeo(equipo):
                    europa.append(equipo)
                    
            if len(tabla) > 4:
                equipo = tabla[4][0]
                if es_equipo_europeo(equipo):
                    conference.append(equipo)
                    
        elif liga == "Eredivisie":
            if len(tabla) > 0:
                equipo = tabla[0][0]
                if es_equipo_europeo(equipo):
                    champions.append(equipo)
                    
            for i in range(1, min(3, len(tabla))):
                equipo = tabla[i][0]
                if es_equipo_europeo(equipo):
                    europa.append(equipo)
                    
            if len(tabla) > 3:
                equipo = tabla[3][0]
                if es_equipo_europeo(equipo):
                    conference.append(equipo)
    
    print(f"\n📊 Equipos clasificados antes de completar:")
    print(f"   Champions: {len(champions)}")
    print(f"   Europa League: {len(europa)}")
    print(f"   Conference: {len(conference)}")
    
    # Completar hasta 32 equipos - SOLO CON EQUIPOS EUROPEOS
    def completar_32(competicion_actual, todas_ligas, nombre_comp):
        faltantes = 32 - len(competicion_actual)
        if faltantes <= 0:
            return competicion_actual[:32]
        
        print(f"\n   Completando {nombre_comp}: necesitamos {faltantes} equipos más")
        
        equipos_no_clasificados = []
        for liga, tabla in todas_ligas.items():
            # FILTRO ESTRICTO: Solo ligas europeas
            if liga not in LIGAS_EUROPEAS:
                continue
                
            for pos, (equipo, stats) in enumerate(tabla, 1):
                # VERIFICACIÓN DOBLE: el equipo debe ser europeo Y no estar clasificado
                if (es_equipo_europeo(equipo) and 
                    equipo not in champions and 
                    equipo not in europa and 
                    equipo not in conference):
                    
                    peso_liga = 1.0
                    if liga in ["Premier League", "La Liga", "Serie A", "Bundesliga"]:
                        peso_liga = 1.2
                    elif liga == "Ligue 1":
                        peso_liga = 1.1
                    
                    puntuacion = (33 - pos) * peso_liga
                    equipos_no_clasificados.append((equipo, puntuacion, liga, pos))
        
        equipos_no_clasificados.sort(key=lambda x: x[1], reverse=True)
        equipos_completar = []
        
        for equipo, punt, liga, pos in equipos_no_clasificados[:faltantes]:
            if es_equipo_europeo(equipo):
                equipos_completar.append(equipo)
                print(f"      ✅ Añadiendo {equipo} de {liga} (pos {pos})")
            else:
                print(f"      ❌ Rechazando {equipo} (NO es europeo)")
        
        return competicion_actual + equipos_completar
    
    champions = completar_32(champions, resultados_ligas, "Champions League")[:32]
    europa = completar_32(europa, resultados_ligas, "Europa League")[:32]
    conference = completar_32(conference, resultados_ligas, "Conference League")[:32]
    
    # VERIFICACIÓN FINAL: Asegurar que TODOS los equipos son europeos
    print(f"\n🔍 VERIFICACIÓN FINAL:")
    
    def verificar_equipos(lista_equipos, nombre_comp):
        no_europeos = [eq for eq in lista_equipos if not es_equipo_europeo(eq)]
        if no_europeos:
            print(f"   ⚠️  {nombre_comp} tiene equipos NO europeos: {no_europeos}")
            # Filtrar equipos no europeos
            lista_filtrada = [eq for eq in lista_equipos if es_equipo_europeo(eq)]
            print(f"   ✅ Filtrados, quedan {len(lista_filtrada)} equipos europeos")
            return lista_filtrada
        else:
            print(f"   ✅ {nombre_comp}: Todos los {len(lista_equipos)} equipos son europeos")
            return lista_equipos
    
    champions = verificar_equipos(champions, "Champions League")
    europa = verificar_equipos(europa, "Europa League")
    conference = verificar_equipos(conference, "Conference League")
    
    return champions, europa, conference

def simular_fase_grupos(equipos_grupo: List[str], archivo) -> List[str]:
    """Simula una fase de grupos y retorna los 2 mejores equipos"""
    tabla = defaultdict(lambda: {'puntos': 0, 'gf': 0, 'gc': 0, 'gd': 0})
    
    for i in range(len(equipos_grupo)):
        for j in range(len(equipos_grupo)):
            if i != j:
                equipo1 = equipos_grupo[i]
                equipo2 = equipos_grupo[j]
                
                gol1, gol2, _ = simular_partido_con_jugadores(equipo1, equipo2)
                
                tabla[equipo1]['gf'] += gol1
                tabla[equipo1]['gc'] += gol2
                tabla[equipo2]['gf'] += gol2
                tabla[equipo2]['gc'] += gol1
                
                if gol1 > gol2:
                    tabla[equipo1]['puntos'] += 3
                elif gol1 < gol2:
                    tabla[equipo2]['puntos'] += 3
                else:
                    tabla[equipo1]['puntos'] += 1
                    tabla[equipo2]['puntos'] += 1
    
    for equipo in tabla:
        tabla[equipo]['gd'] = tabla[equipo]['gf'] - tabla[equipo]['gc']
    
    tabla_ordenada = sorted(tabla.items(), 
                           key=lambda x: (x[1]['puntos'], x[1]['gd'], x[1]['gf']), 
                           reverse=True)
    
    archivo.write(f"{'Pos':<3} {'Equipo':<12} {'Pts':<4} {'GF':<4} {'GC':<4} {'GD':<4}\n")
    for i, (equipo, stats) in enumerate(tabla_ordenada, 1):
        archivo.write(f"{i:<3} {equipo.upper():<12} {stats['puntos']:<4} {stats['gf']:<4} {stats['gc']:<4} {stats['gd']:+4}\n")
    
    return [tabla_ordenada[0][0], tabla_ordenada[1][0]]

def simular_champions_league(equipos: List[str], archivo) -> str:
    """Simula la Champions League completa"""
    archivo.write(f"\n{'='*80}\n")
    archivo.write("🏆 CHAMPIONS LEAGUE 2024/25\n")
    archivo.write(f"{'='*80}\n")
    
    equipos_copia = equipos[:32].copy()
    rm.shuffle(equipos_copia)
    
    # Fase de grupos
    archivo.write(f"\n🎯 FASE DE GRUPOS:\n")
    archivo.write("-" * 40 + "\n")
    octavos = []
    
    for grupo in range(8):
        archivo.write(f"\nGrupo {chr(65 + grupo)}:\n")
        equipos_grupo = equipos_copia[grupo*4:(grupo+1)*4]
        clasificados_grupo = simular_fase_grupos(equipos_grupo, archivo)
        octavos.extend(clasificados_grupo)
    
    # Octavos de final
    archivo.write(f"\n🎯 OCTAVOS DE FINAL\n")
    archivo.write("-" * 40 + "\n")
    cuartos = []
    
    for i in range(0, 16, 2):
        equipo1, equipo2 = octavos[i], octavos[i+1]
        ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
        cuartos.append(ganador)
        archivo.write(f"{resultado}\n")
        archivo.write(f"✅ Pasa: {ganador.upper()}\n\n")
    
    # Cuartos de final
    archivo.write(f"🔥 CUARTOS DE FINAL\n")
    archivo.write("-" * 40 + "\n")
    semis = []
    
    for i in range(0, 8, 2):
        equipo1, equipo2 = cuartos[i], cuartos[i+1]
        ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
        semis.append(ganador)
        archivo.write(f"{resultado}\n")
        archivo.write(f"✅ Pasa: {ganador.upper()}\n\n")
    
    # Semifinales
    archivo.write(f"⚡ SEMIFINALES\n")
    archivo.write("-" * 40 + "\n")
    finalistas = []
    
    for i in range(0, 4, 2):
        equipo1, equipo2 = semis[i], semis[i+1]
        ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
        finalistas.append(ganador)
        archivo.write(f"{resultado}\n")
        archivo.write(f"✅ FINALISTA: {ganador.upper()}\n\n")
    
    # Final
    archivo.write(f"👑 FINAL CHAMPIONS LEAGUE\n")
    archivo.write("=" * 40 + "\n")
    campeon, resultado_final = simular_final_con_jugadores(finalistas[0], finalistas[1])
    archivo.write(f"{resultado_final}\n")
    archivo.write(f"🏆 CAMPEÓN CHAMPIONS LEAGUE: {campeon.upper()}\n")
    
    base_datos.registrar_campeon('champions', campeon)
    return campeon

def simular_europa_league(equipos: List[str], archivo) -> str:
    """Simula la Europa League completa con formato mejorado"""
    archivo.write(f"\n{'='*80}\n")
    archivo.write("🥈 EUROPA LEAGUE 2024/25 (32 equipos)\n")
    archivo.write(f"{'='*80}\n")
    
    equipos_copia = equipos[:32].copy()
    rm.shuffle(equipos_copia)
    
    archivo.write(f"\n📊 EQUIPOS PARTICIPANTES (32):\n")
    archivo.write("-" * 40 + "\n")
    for i, equipo in enumerate(equipos_copia, 1):
        nivel = base_datos.obtener_nivel_equipo(equipo)
        archivo.write(f"{i:2}. {equipo.upper()} (Nivel: {nivel})\n")
    
    # Fase de grupos
    archivo.write(f"\n{'='*80}\n")
    archivo.write("🎯 FASE DE GRUPOS\n")
    archivo.write(f"{'='*80}\n")
    dieciseisavos = []
    
    for grupo in range(8):
        archivo.write(f"\n{'─'*40}\n")
        archivo.write(f"GRUPO {chr(65 + grupo)}\n")
        archivo.write(f"{'─'*40}\n")
        equipos_grupo = equipos_copia[grupo*4:(grupo+1)*4]
        clasificados_grupo = simular_fase_grupos(equipos_grupo, archivo)
        dieciseisavos.extend(clasificados_grupo)
        archivo.write(f"✅ CLASIFICAN: {clasificados_grupo[0].upper()} y {clasificados_grupo[1].upper()}\n")
    
    # Dieciseisavos
    archivo.write(f"\n{'='*80}\n")
    archivo.write("⚔️  DIECISEISAVOS DE FINAL\n")
    archivo.write(f"{'='*80}\n")
    octavos = []
    
    for i in range(0, len(dieciseisavos), 2):
        if i + 1 < len(dieciseisavos):
            equipo1, equipo2 = dieciseisavos[i], dieciseisavos[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            octavos.append(ganador)
            archivo.write(f"\n{resultado}\n")
            archivo.write(f"✅ Clasifica: {ganador.upper()}\n")
    
    # Octavos
    archivo.write(f"\n{'='*80}\n")
    archivo.write("🔥 OCTAVOS DE FINAL\n")
    archivo.write(f"{'='*80}\n")
    cuartos = []
    
    for i in range(0, len(octavos), 2):
        if i + 1 < len(octavos):
            equipo1, equipo2 = octavos[i], octavos[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            cuartos.append(ganador)
            archivo.write(f"\n{resultado}\n")
            archivo.write(f"✅ Clasifica: {ganador.upper()}\n")
    
    # Cuartos
    archivo.write(f"\n{'='*80}\n")
    archivo.write("⚡ CUARTOS DE FINAL\n")
    archivo.write(f"{'='*80}\n")
    semis = []
    
    for i in range(0, len(cuartos), 2):
        if i + 1 < len(cuartos):
            equipo1, equipo2 = cuartos[i], cuartos[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            semis.append(ganador)
            archivo.write(f"\n{resultado}\n")
            archivo.write(f"✅ Clasifica: {ganador.upper()}\n")
    
    # Semifinales
    archivo.write(f"\n{'='*80}\n")
    archivo.write("💫 SEMIFINALES\n")
    archivo.write(f"{'='*80}\n")
    finalistas = []
    
    for i in range(0, len(semis), 2):
        if i + 1 < len(semis):
            equipo1, equipo2 = semis[i], semis[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            finalistas.append(ganador)
            archivo.write(f"\n{resultado}\n")
            archivo.write(f"✅ FINALISTA: {ganador.upper()}\n")
    
    # Final
    archivo.write(f"\n{'='*80}\n")
    if len(finalistas) >= 2:
        archivo.write("👑 FINAL EUROPA LEAGUE\n")
        archivo.write(f"{'='*80}\n")
        campeon, resultado_final = simular_final_con_jugadores(finalistas[0], finalistas[1])
        archivo.write(f"\n{resultado_final}\n\n")
        archivo.write(f"{'🏆'*20}\n")
        archivo.write(f"🥈 CAMPEÓN EUROPA LEAGUE: {campeon.upper()}\n")
        archivo.write(f"{'🏆'*20}\n")
    else:
        campeon = finalistas[0] if finalistas else equipos_copia[0]
        archivo.write(f"🥈 CAMPEÓN EUROPA LEAGUE: {campeon.upper()} (por defecto)\n")
    
    base_datos.registrar_campeon('europa', campeon)
    return campeon

def simular_conference_league(equipos: List[str], archivo) -> str:
    """Simula la Conference League completa con formato mejorado"""
    archivo.write(f"\n{'='*80}\n")
    archivo.write("🎯 CONFERENCE LEAGUE 2024/25 (32 equipos)\n")
    archivo.write(f"{'='*80}\n")
    
    equipos_copia = equipos[:32].copy()
    rm.shuffle(equipos_copia)
    
    archivo.write(f"\n📊 EQUIPOS PARTICIPANTES (32):\n")
    archivo.write("-" * 40 + "\n")
    for i, equipo in enumerate(equipos_copia, 1):
        nivel = base_datos.obtener_nivel_equipo(equipo)
        archivo.write(f"{i:2}. {equipo.upper()} (Nivel: {nivel})\n")
    
    # Fase de grupos
    archivo.write(f"\n{'='*80}\n")
    archivo.write("🎯 FASE DE GRUPOS\n")
    archivo.write(f"{'='*80}\n")
    dieciseisavos = []
    
    for grupo in range(8):
        archivo.write(f"\n{'─'*40}\n")
        archivo.write(f"GRUPO {chr(65 + grupo)}\n")
        archivo.write(f"{'─'*40}\n")
        equipos_grupo = equipos_copia[grupo*4:(grupo+1)*4]
        clasificados_grupo = simular_fase_grupos(equipos_grupo, archivo)
        dieciseisavos.extend(clasificados_grupo)
        archivo.write(f"✅ CLASIFICAN: {clasificados_grupo[0].upper()} y {clasificados_grupo[1].upper()}\n")
    
    # Dieciseisavos
    archivo.write(f"\n{'='*80}\n")
    archivo.write("⚔️  DIECISEISAVOS DE FINAL\n")
    archivo.write(f"{'='*80}\n")
    octavos = []
    
    for i in range(0, len(dieciseisavos), 2):
        if i + 1 < len(dieciseisavos):
            equipo1, equipo2 = dieciseisavos[i], dieciseisavos[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            octavos.append(ganador)
            archivo.write(f"\n{resultado}\n")
            archivo.write(f"✅ Clasifica: {ganador.upper()}\n")
    
    # Octavos
    archivo.write(f"\n{'='*80}\n")
    archivo.write("🔥 OCTAVOS DE FINAL\n")
    archivo.write(f"{'='*80}\n")
    cuartos = []
    
    for i in range(0, len(octavos), 2):
        if i + 1 < len(octavos):
            equipo1, equipo2 = octavos[i], octavos[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            cuartos.append(ganador)
            archivo.write(f"\n{resultado}\n")
            archivo.write(f"✅ Clasifica: {ganador.upper()}\n")
    
    # Cuartos
    archivo.write(f"\n{'='*80}\n")
    archivo.write("⚡ CUARTOS DE FINAL\n")
    archivo.write(f"{'='*80}\n")
    semis = []
    
    for i in range(0, len(cuartos), 2):
        if i + 1 < len(cuartos):
            equipo1, equipo2 = cuartos[i], cuartos[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            semis.append(ganador)
            archivo.write(f"\n{resultado}\n")
            archivo.write(f"✅ Clasifica: {ganador.upper()}\n")
    
    # Semifinales
    archivo.write(f"\n{'='*80}\n")
    archivo.write("💫 SEMIFINALES\n")
    archivo.write(f"{'='*80}\n")
    finalistas = []
    
    for i in range(0, len(semis), 2):
        if i + 1 < len(semis):
            equipo1, equipo2 = semis[i], semis[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            finalistas.append(ganador)
            archivo.write(f"\n{resultado}\n")
            archivo.write(f"✅ FINALISTA: {ganador.upper()}\n")
    
    # Final
    archivo.write(f"\n{'='*80}\n")
    if len(finalistas) >= 2:
        archivo.write("👑 FINAL CONFERENCE LEAGUE\n")
        archivo.write(f"{'='*80}\n")
        campeon, resultado_final = simular_final_con_jugadores(finalistas[0], finalistas[1])
        archivo.write(f"\n{resultado_final}\n\n")
        archivo.write(f"{'🏆'*20}\n")
        archivo.write(f"🎯 CAMPEÓN CONFERENCE LEAGUE: {campeon.upper()}\n")
        archivo.write(f"{'🏆'*20}\n")
    else:
        campeon = finalistas[0] if finalistas else equipos_copia[0]
        archivo.write(f"🎯 CAMPEÓN CONFERENCE LEAGUE: {campeon.upper()}\n")
    
    base_datos.registrar_campeon('conference', campeon)
    return campeon

def escribir_estadisticas_individuales(archivo):
    """Escribe las estadísticas individuales de jugadores"""
    archivo.write(f"\n{'='*80}\n")
    archivo.write("ESTADÍSTICAS INDIVIDUALES DE LA TEMPORADA\n")
    archivo.write(f"{'='*80}\n")
    
    # Top Goleadores
    top_goleadores = base_datos.obtener_top_goleadores(10)
    archivo.write("\n🥇 TOP 10 GOLEADORES\n")
    archivo.write("-" * 60 + "\n")
    archivo.write(f"{'Pos':<3} {'Jugador':<15} {'Equipo':<10} {'Goles':<6}\n")
    archivo.write("-" * 60 + "\n")
    
    for i, jugador in enumerate(top_goleadores, 1):
        archivo.write(f"{i:<3} {jugador.nombre:<15} {jugador.equipo.upper():<10} {jugador.goles:<6}\n")
    
    # Top Asistentes
    top_asistentes = base_datos.obtener_top_asistentes(10)
    archivo.write(f"\n🎯 TOP 10 ASISTENTES\n")
    archivo.write("-" * 60 + "\n")
    archivo.write(f"{'Pos':<3} {'Jugador':<15} {'Equipo':<10} {'Asist':<6}\n")
    archivo.write("-" * 60 + "\n")
    
    for i, jugador in enumerate(top_asistentes, 1):
        archivo.write(f"{i:<3} {jugador.nombre:<15} {jugador.equipo.upper():<10} {jugador.asistencias:<6}\n")
    
    # Balón de Oro
    candidatos_balon = base_datos.obtener_candidatos_balon_oro(20)
    archivo.write(f"\n🏆 TOP 20 CANDIDATOS BALÓN DE ORO\n")
    archivo.write("-" * 80 + "\n")
    archivo.write(f"{'Pos':<3} {'Jugador':<15} {'Equipo':<10} {'Goles':<6} {'Asist':<6} {'Puntos':<8}\n")
    archivo.write("-" * 80 + "\n")
    
    for i, (jugador, puntos) in enumerate(candidatos_balon, 1):
        medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i:<3}"
        archivo.write(f"{medalla} {jugador.nombre:<15} {jugador.equipo.upper():<10} "
                     f"{jugador.goles:<6} {jugador.asistencias:<6} {puntos:<8.2f}\n")

def escribir_tabla_liga_mejorada(archivo, nombre_liga: str, tabla: List[Tuple]):
    """Escribe la tabla de una liga"""
    archivo.write(f"\n{'='*70}\n")
    archivo.write(f"TABLA FINAL - {nombre_liga.upper()}\n")
    archivo.write(f"{'='*70}\n")
    archivo.write(f"{'Pos':<3} {'Equipo':<12} {'Pts':<4} {'PJ':<3} {'GF':<3} {'GC':<3} {'DG':<4}\n")
    archivo.write("-" * 70 + "\n")
    
    for i, (equipo, stats) in enumerate(tabla, 1):
        archivo.write(f"{i:<3} {equipo.upper():<12} {stats['puntos']:<4} {stats['partidos']:<3} "
                     f"{stats['gf']:<3} {stats['gc']:<3} {stats['gd']:+4}\n")
    
    # Clasificaciones
    archivo.write(f"\nCLASIFICACIONES:\n")
    if nombre_liga in ["Premier League", "La Liga", "Serie A", "Bundesliga"]:
        archivo.write(f"🏆 Champions League: {', '.join([tabla[i][0].upper() for i in range(min(4, len(tabla)))])}\n")
        if len(tabla) > 5:
            archivo.write(f"🥈 Europa League: {tabla[4][0].upper()}, {tabla[5][0].upper()}\n")
        if len(tabla) > 6:
            archivo.write(f"🎯 Conference League: {tabla[6][0].upper()}\n")

def main():
    """Función principal del simulador"""
    print("🏆 SIMULADOR COMPLETO DE FÚTBOL 🏆")
    print("=" * 70)
    print("Inicializando...")
    
    try:
        # Reset estadísticas
        base_datos.reset_estadisticas_temporada()
        
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"temporada_completa_{fecha_actual}.txt"
        
        # Obtener ligas
        ligas = base_datos.obtener_ligas()
        
        print(f"Simulando temporada con {len(base_datos.jugadores)} jugadores...")
        
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write("🏆 SIMULACIÓN TEMPORADA COMPLETA 🏆\n")
            archivo.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            archivo.write(f"Jugadores: {len(base_datos.jugadores)}\n")
            archivo.write(f"Equipos: {len(base_datos.equipos)}\n")
            archivo.write("=" * 80 + "\n")
            
            # Simular ligas
            print("\n📊 Simulando ligas domésticas...")
            resultados_ligas = {}
            
            for nombre_liga, equipos_dict in ligas.items():
                print(f"🏟️  {nombre_liga}...")
                tabla = simular_liga_con_jugadores(nombre_liga, equipos_dict)
                resultados_ligas[nombre_liga] = tabla
                escribir_tabla_liga_mejorada(archivo, nombre_liga, tabla)
            
            # Clasificados europeos
            print("\n🌍 Obteniendo clasificados europeos...")
            champions, europa, conference = obtener_clasificados_europeos(resultados_ligas)
            
            # Champions League
            print("\n🏆 Simulando Champions League...")
            campeon_champions = simular_champions_league(champions, archivo)
            
            # Europa League
            print("🥈 Simulando Europa League...")
            campeon_europa = simular_europa_league(europa, archivo)
            
            # Conference League
            print("🎯 Simulando Conference League...")
            campeon_conference = simular_conference_league(conference, archivo)
            
            # Competiciones sudamericanas
            print("\n🌎 Simulando competiciones sudamericanas...")
            try:
                campeon_libertadores, _ = simular_copa_latina("Copa Libertadores", archivo)
                campeon_sudamericana, _ = simular_copa_latina("Copa Sudamericana", archivo)
                
                # Intercontinental
                print("🌍 Simulando Torneo Intercontinental...")
                archivo.write(f"\n🌍 TORNEO INTERCONTINENTAL\n")
                archivo.write("=" * 40 + "\n")
                campeon_intercontinental, resultado = simular_final_con_jugadores(
                    campeon_champions, campeon_libertadores
                )
                archivo.write(f"{resultado}\n")
                archivo.write(f"🏆 CAMPEÓN INTERCONTINENTAL: {campeon_intercontinental.upper()}\n")
            except Exception as e:
                print(f"⚠️  Error en competiciones sudamericanas: {e}")
                campeon_libertadores = "N/A"
                campeon_sudamericana = "N/A"
                campeon_intercontinental = campeon_champions
            
            # Estadísticas individuales
            print("📊 Generando estadísticas individuales...")
            escribir_estadisticas_individuales(archivo)
            
            # Resumen final
            archivo.write(f"\n{'='*80}\n")
            archivo.write("🏆 RESUMEN FINAL DE LA TEMPORADA 🏆\n")
            archivo.write(f"{'='*80}\n")
            
            archivo.write("\n📊 CAMPEONES DE LIGA:\n")
            archivo.write("-" * 50 + "\n")
            for nombre_liga, tabla in resultados_ligas.items():
                if tabla:
                    archivo.write(f"🏆 {nombre_liga:<20}: {tabla[0][0].upper()}\n")
            
            archivo.write(f"\n🌍 CAMPEONES EUROPEOS:\n")
            archivo.write("-" * 50 + "\n")
            archivo.write(f"🏆 Champions League: {campeon_champions.upper()}\n")
            archivo.write(f"🥈 Europa League: {campeon_europa.upper()}\n")
            archivo.write(f"🎯 Conference League: {campeon_conference.upper()}\n")
            
            if campeon_libertadores != "N/A":
                archivo.write(f"\n🌎 CAMPEONES SUDAMERICANOS:\n")
                archivo.write("-" * 50 + "\n")
                archivo.write(f"🏆 Libertadores: {campeon_libertadores.upper()}\n")
                archivo.write(f"🥈 Sudamericana: {campeon_sudamericana.upper()}\n")
                archivo.write(f"\n🌍 CAMPEÓN INTERCONTINENTAL: {campeon_intercontinental.upper()}\n")
            
            # Top goleadores resumido
            top_goleadores = base_datos.obtener_top_goleadores(5)
            archivo.write(f"\n⚽ TOP 5 GOLEADORES:\n")
            archivo.write("-" * 50 + "\n")
            for i, jugador in enumerate(top_goleadores, 1):
                medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                archivo.write(f"{medalla} {jugador.nombre} ({jugador.equipo.upper()}) - {jugador.goles} goles\n")
            
            # Balón de Oro
            candidatos_balon = base_datos.obtener_candidatos_balon_oro(1)
            if candidatos_balon:
                ganador, puntos = candidatos_balon[0]
                archivo.write(f"\n🥇 BALÓN DE ORO: {ganador.nombre.upper()} ({ganador.equipo.upper()})\n")
                archivo.write(f"   {ganador.goles} goles, {ganador.asistencias} asistencias - {puntos:.2f} pts\n")
            
            # Rey de América
            try:
                rey_america = seleccionar_mejor_jugador_america()
                if rey_america:
                    archivo.write(f"\n👑 REY DE AMÉRICA: {rey_america.nombre.upper()} ({rey_america.equipo.upper()})\n")
                    archivo.write(f"   {rey_america.goles} goles, {rey_america.asistencias} asistencias\n")
            except:
                pass
        
        print(f"\n✅ Simulación completada!")
        print(f"📄 Archivo generado: {nombre_archivo}")
        
        # Resumen en consola
        print("\n🏆 RESUMEN:")
        print(f"   Champions League: {campeon_champions.upper()}")
        print(f"   Europa League: {campeon_europa.upper()}")
        print(f"   Conference League: {campeon_conference.upper()}")
        
        if campeon_libertadores != "N/A":
            print(f"   Libertadores: {campeon_libertadores.upper()}")
            print(f"   Intercontinental: {campeon_intercontinental.upper()}")
        
        top_3 = base_datos.obtener_top_goleadores(3)
        print("\n⚽ TOP 3 GOLEADORES:")
        for i, j in enumerate(top_3, 1):
            print(f"   {i}. {j.nombre} ({j.equipo.upper()}) - {j.goles} goles")
        
        print("\n🎉 ¡Simulación completada exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante la simulación: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
