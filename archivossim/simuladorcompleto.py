import random as rm
from collections import defaultdict
from datetime import datetime
from typing import List, Tuple, Dict
from base_datos import base_datos, Jugador, Equipo

def simular_partido_con_jugadores(equipo1: str, equipo2: str) -> Tuple[int, int, List[Dict]]:
    """
    Simula un partido entre dos equipos con estadísticas REALISTAS
    """
    team1 = base_datos.obtener_equipo(equipo1)
    team2 = base_datos.obtener_equipo(equipo2)
    
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
    oportunidades_equipo1 = 0
    oportunidades_equipo2 = 0
    
    for minuto in range(1, 91):
        prob = rm.randint(1, 200)
        
        # OPORTUNIDADES DE GOL REALISTAS (2.5% por minuto = ~2.25 por partido)
        if prob > 195:  # 2.5% de probabilidad
            prob2 = rm.randint(0, int(sumalevel))
            
            equipo_atacante = team1 if prob2 <= nivel1_ajustado else team2
            goleador, asistente = seleccionar_goleador_y_asistente(equipo_atacante)
            
            if goleador:
                # Registrar la oportunidad (para estadísticas)
                if equipo_atacante == team1:
                    oportunidades_equipo1 += 1
                else:
                    oportunidades_equipo2 += 1
                
                # PROBABILIDAD DE CONVERSIÓN REALISTA
                # Mejores delanteros: 25-35% de efectividad
                efectividad_base = 0.25
                bonus_nivel = (goleador.nivel - 80) / 100  # +0.15 para jugadores de nivel 95
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
    Selecciona quién marca el gol y quién da la asistencia - versión más realista
    """
    # Probabilidades por posición y nivel
    prob_gol = {
        "DEL": 0.7,  # Delanteros más probables
        "MED": 0.25, # Mediocampistas
        "DEF": 0.04, # Defensores
        "POR": 0.01  # Porteros (muy raro)
    }
    
    prob_asist = {
        "MED": 0.6,  # Mediocampistas más asistentes
        "DEL": 0.3,  # Delanteros
        "DEF": 0.08, # Defensores
        "POR": 0.02  # Porteros
    }
    
    # Ordenar jugadores por nivel (mejores jugadores más probables)
    jugadores_ordenados = sorted(equipo.jugadores, key=lambda x: x.nivel, reverse=True)
    
    # Seleccionar goleador - los mejores jugadores tienen más probabilidad
    goleador = None
    for jugador in jugadores_ordenados:
        prob_posicion = prob_gol.get(jugador.posicion, 0.1)
        prob_nivel = jugador.nivel / 100.0
        prob_final = prob_posicion * prob_nivel * 1.8  # Más realista
        
        if rm.random() < prob_final:
            goleador = jugador
            break
    
    if not goleador:  # Fallback: mejor jugador del equipo
        goleador = jugadores_ordenados[0]
    
    # Seleccionar asistente (diferente al goleador)
    asistente = None
    jugadores_sin_goleador = [j for j in jugadores_ordenados if j != goleador]
    
    for jugador in jugadores_sin_goleador:
        prob_posicion = prob_asist.get(jugador.posicion, 0.1)
        prob_nivel = jugador.nivel / 100.0
        prob_final = prob_posicion * prob_nivel * 1.5
        
        if rm.random() < prob_final:
            asistente = jugador
            break
    
    # 30% de posibilidad de que no haya asistencia registrada (más realista)
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
    """Simula una eliminatoria a doble partido registrando estadísticas"""
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
            # Penales (basado en nivel)
            nivel1 = base_datos.obtener_nivel_equipo(equipo1)
            nivel2 = base_datos.obtener_nivel_equipo(equipo2)
            prob_pen = rm.randint(0, nivel1 + nivel2)
            ganador = equipo1 if prob_pen <= nivel1 else equipo2
            return ganador, resultado + f" - {ganador.upper()} por penales"

def simular_final_con_jugadores(equipo1: str, equipo2: str) -> Tuple[str, str]:
    """Simula una final registrando estadísticas"""
    nivel1 = base_datos.obtener_nivel_equipo(equipo1)
    nivel2 = base_datos.obtener_nivel_equipo(equipo2)
    
    goles1, goles2, eventos = simular_partido_con_jugadores(equipo1, equipo2)
    resultado = f"{equipo1.upper()} {goles1}-{goles2} {equipo2.upper()}"
    
    if goles1 > goles2:
        return equipo1, resultado
    elif goles2 > goles1:
        return equipo2, resultado
    else:
        # Penales en final
        prob_pen = rm.randint(0, nivel1 + nivel2)
        ganador = equipo1 if prob_pen <= nivel1 else equipo2
        return ganador, resultado + f" - {ganador.upper()} por penales"

def obtener_clasificados_europeos(resultados_ligas: Dict) -> Tuple[List[str], List[str], List[str]]:
    """Obtiene los equipos clasificados para cada competición europea y completa con los mejores"""
    champions = []
    europa = []
    conference = []
    
    for liga, tabla in resultados_ligas.items():
        if liga in ["Premier League", "La Liga", "Serie A", "Bundesliga"]:
            champions.extend([tabla[0][0], tabla[1][0], tabla[2][0], tabla[3][0]])
            europa.extend([tabla[4][0], tabla[5][0]])
            if len(tabla) > 6:
                conference.append(tabla[6][0])
        elif liga == "Ligue 1":
            champions.extend([tabla[0][0], tabla[1][0], tabla[2][0]])
            europa.append(tabla[3][0])
            if len(tabla) > 4:
                conference.append(tabla[4][0])
        elif liga == "Primeira Liga":
            champions.extend([tabla[0][0], tabla[1][0]])
            europa.extend([tabla[2][0], tabla[3][0]])
            if len(tabla) > 4:
                conference.append(tabla[4][0])
        elif liga == "Eredivisie":
            champions.append(tabla[0][0])
            europa.extend([tabla[1][0], tabla[2][0]])
            if len(tabla) > 3:
                conference.append(tabla[3][0])
    
    # Completar con los mejores equipos de cada liga hasta tener 32
    def completar_32(competicion_actual, todas_ligas):
        faltantes = 32 - len(competicion_actual)
        if faltantes <= 0:
            return competicion_actual
        
        # Crear lista de todos los equipos no clasificados, ordenados por posición
        equipos_no_clasificados = []
        for liga, tabla in todas_ligas.items():
            for pos, (equipo, stats) in enumerate(tabla, 1):
                if equipo not in champions and equipo not in europa and equipo not in conference:
                    # Ponderar por calidad de liga y posición
                    peso_liga = 1.0
                    if liga in ["Premier League", "La Liga", "Serie A", "Bundesliga"]:
                        peso_liga = 1.2
                    elif liga == "Ligue 1":
                        peso_liga = 1.1
                    
                    puntuacion = (33 - pos) * peso_liga  # Mejor posición = mayor puntuación
                    equipos_no_clasificados.append((equipo, puntuacion, liga, pos))
        
        # Ordenar por puntuación y tomar los mejores
        equipos_no_clasificados.sort(key=lambda x: x[1], reverse=True)
        equipos_completar = [eq[0] for eq in equipos_no_clasificados[:faltantes]]
        
        return competicion_actual + equipos_completar
    
    # Completar cada competición a 32 equipos
    champions = completar_32(champions, resultados_ligas)[:32]
    europa = completar_32(europa, resultados_ligas)[:32]
    conference = completar_32(conference, resultados_ligas)[:32]
    
    return champions, europa, conference

def simular_fase_grupos(equipos_grupo: List[str], archivo) -> List[str]:
    """Simula una fase de grupos y retorna los 2 mejores equipos"""
    tabla = defaultdict(lambda: {'puntos': 0, 'gf': 0, 'gc': 0, 'gd': 0})
    
    # Todos contra todos (ida y vuelta)
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
    
    # Calcular diferencia de goles
    for equipo in tabla:
        tabla[equipo]['gd'] = tabla[equipo]['gf'] - tabla[equipo]['gc']
    
    # Ordenar tabla
    tabla_ordenada = sorted(tabla.items(), 
                           key=lambda x: (x[1]['puntos'], x[1]['gd'], x[1]['gf']), 
                           reverse=True)
    
    # Mostrar tabla del grupo
    archivo.write(f"{'Pos':<3} {'Equipo':<12} {'Pts':<4} {'GF':<4} {'GC':<4} {'GD':<4}\n")
    for i, (equipo, stats) in enumerate(tabla_ordenada, 1):
        archivo.write(f"{i:<3} {equipo.upper():<12} {stats['puntos']:<4} {stats['gf']:<4} {stats['gc']:<4} {stats['gd']:<+4}\n")
    
    # Retornar los 2 primeros
    return [tabla_ordenada[0][0], tabla_ordenada[1][0]]

def simular_champions_league(equipos: List[str], archivo) -> str:
    """Simula la Champions League completa con exactamente 32 equipos"""
    archivo.write(f"\n{'='*80}\n")
    archivo.write("🏆 CHAMPIONS LEAGUE 2024/25 (32 equipos)\n")
    archivo.write(f"{'='*80}\n")
    
    # Asegurar exactamente 32 equipos
    equipos_copia = equipos[:32].copy()
    rm.shuffle(equipos_copia)
    
    archivo.write(f"\n📊 EQUIPOS PARTICIPANTES (32):\n")
    archivo.write("-" * 40 + "\n")
    for i, equipo in enumerate(equipos_copia, 1):
        nivel = base_datos.obtener_nivel_equipo(equipo)
        archivo.write(f"{i:2}. {equipo.upper()} (Nivel: {nivel})\n")
    
    # Fase de grupos (8 grupos de 4)
    archivo.write(f"\n🎯 FASE DE GRUPOS:\n")
    archivo.write("-" * 40 + "\n")
    octavos = []
    
    for grupo in range(8):
        archivo.write(f"\nGrupo {chr(65 + grupo)}:\n")
        equipos_grupo = equipos_copia[grupo*4:(grupo+1)*4]
        clasificados_grupo = simular_fase_grupos(equipos_grupo, archivo)
        octavos.extend(clasificados_grupo)
    
    # Continuar con octavos, cuartos, etc. (el resto del código igual)
    # ... [el resto del código de simular_champions_league permanece igual]
    
    # Octavos de final
    archivo.write(f"\n🎯 OCTAVOS DE FINAL\n")
    archivo.write("-" * 40 + "\n")
    octavos = equipos_copia[:16]
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
    """Simula la Europa League completa con exactamente 32 equipos"""
    archivo.write(f"\n{'='*80}\n")
    archivo.write("🏅 EUROPA LEAGUE 2024/25 (32 equipos)\n")
    archivo.write(f"{'='*80}\n")
    
    # Asegurar exactamente 32 equipos
    equipos_copia = equipos[:32].copy()
    rm.shuffle(equipos_copia)
    
    archivo.write(f"\n📊 EQUIPOS PARTICIPANTES (32):\n")
    archivo.write("-" * 40 + "\n")
    for i, equipo in enumerate(equipos_copia, 1):
        nivel = base_datos.obtener_nivel_equipo(equipo)
        archivo.write(f"{i:2}. {equipo.upper()} (Nivel: {nivel})\n")
    
    # Fase de grupos (8 grupos de 4)
    archivo.write(f"\n🎯 FASE DE GRUPOS:\n")
    archivo.write("-" * 40 + "\n")
    dieciseisavos = []
    
    for grupo in range(8):
        archivo.write(f"\nGrupo {chr(65 + grupo)}:\n")
        equipos_grupo = equipos_copia[grupo*4:(grupo+1)*4]
        clasificados_grupo = simular_fase_grupos(equipos_grupo, archivo)
        dieciseisavos.extend(clasificados_grupo)
    
    # CORRECCIÓN: dieciseisavos tiene 16 equipos (8 grupos × 2 clasificados)
    num_equipos_dieciseisavos = len(dieciseisavos)
    archivo.write(f"\n🎯 DIECISEISAVOS DE FINAL ({num_equipos_dieciseisavos} equipos)\n")
    archivo.write("-" * 40 + "\n")
    octavos = []
    
    # CORRECCIÓN: Usar la longitud real de dieciseisavos
    for i in range(0, num_equipos_dieciseisavos, 2):
        if i + 1 < num_equipos_dieciseisavos:  # Verificar que existe el siguiente equipo
            equipo1, equipo2 = dieciseisavos[i], dieciseisavos[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            octavos.append(ganador)
            archivo.write(f"{resultado}\n")
            archivo.write(f"✅ Pasa: {ganador.upper()}\n\n")
        else:
            # Si queda un equipo sin pareja, pasa automáticamente
            octavos.append(dieciseisavos[i])
            archivo.write(f"{dieciseisavos[i].upper()} pasa automáticamente (sin oponente)\n")
    
    # El resto del código permanece igual...
    # Octavos de final (deberían ser 8 equipos)
    num_octavos = len(octavos)
    archivo.write(f"\n🔥 OCTAVOS DE FINAL ({num_octavos} equipos)\n")
    archivo.write("-" * 40 + "\n")
    cuartos = []
    
    for i in range(0, num_octavos, 2):
        if i + 1 < num_octavos:
            equipo1, equipo2 = octavos[i], octavos[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            cuartos.append(ganador)
            archivo.write(f"{resultado}\n")
            archivo.write(f"✅ Pasa: {ganador.upper()}\n\n")
        else:
            cuartos.append(octavos[i])
            archivo.write(f"{octavos[i].upper()} pasa automáticamente (sin oponente)\n")
    
    # Continuar con cuartos, semis y final...
    # Cuartos de final
    num_cuartos = len(cuartos)
    archivo.write(f"⚡ CUARTOS DE FINAL ({num_cuartos} equipos)\n")
    archivo.write("-" * 40 + "\n")
    semis = []
    
    for i in range(0, num_cuartos, 2):
        if i + 1 < num_cuartos:
            equipo1, equipo2 = cuartos[i], cuartos[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            semis.append(ganador)
            archivo.write(f"{resultado}\n")
            archivo.write(f"✅ Pasa: {ganador.upper()}\n\n")
        else:
            semis.append(cuartos[i])
            archivo.write(f"{cuartos[i].upper()} pasa automáticamente (sin oponente)\n")
    
    # Semifinales
    num_semis = len(semis)
    archivo.write(f"💫 SEMIFINALES ({num_semis} equipos)\n")
    archivo.write("-" * 40 + "\n")
    finalistas = []
    
    for i in range(0, num_semis, 2):
        if i + 1 < num_semis:
            equipo1, equipo2 = semis[i], semis[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            finalistas.append(ganador)
            archivo.write(f"{resultado}\n")
            archivo.write(f"✅ FINALISTA: {ganador.upper()}\n\n")
        else:
            finalistas.append(semis[i])
            archivo.write(f"{semis[i].upper()} pasa automáticamente a la final (sin oponente)\n")
    
    # Final
    if len(finalistas) == 2:
        archivo.write(f"👑 FINAL EUROPA LEAGUE\n")
        archivo.write("=" * 40 + "\n")
        campeon, resultado_final = simular_final_con_jugadores(finalistas[0], finalistas[1])
        archivo.write(f"{resultado_final}\n")
        archivo.write(f"🏅 CAMPEÓN EUROPA LEAGUE: {campeon.upper()}\n")
    elif len(finalistas) == 1:
        archivo.write(f"👑 FINAL EUROPA LEAGUE\n")
        archivo.write("=" * 40 + "\n")
        archivo.write(f"🏅 CAMPEÓN EUROPA LEAGUE: {finalistas[0].upper()} (ganador por walkover)\n")
        campeon = finalistas[0]
    else:
        archivo.write("❌ No hay suficientes finalistas\n")
        campeon = ""
    
    base_datos.registrar_campeon('europa', campeon)
    return campeon


def simular_conference_league(equipos: List[str], archivo) -> str:
    """Simula la Conference League completa con exactamente 32 equipos"""
    archivo.write(f"\n{'='*80}\n")
    archivo.write("🎯 CONFERENCE LEAGUE 2024/25 (32 equipos)\n")
    archivo.write(f"{'='*80}\n")
    
    # Asegurar exactamente 32 equipos
    equipos_copia = equipos[:32].copy()
    rm.shuffle(equipos_copia)
    
    archivo.write(f"\n📊 EQUIPOS PARTICIPANTES (32):\n")
    archivo.write("-" * 40 + "\n")
    for i, equipo in enumerate(equipos_copia, 1):
        nivel = base_datos.obtener_nivel_equipo(equipo)
        archivo.write(f"{i:2}. {equipo.upper()} (Nivel: {nivel})\n")
    
    # Fase de grupos (8 grupos de 4)
    archivo.write(f"\n🎯 FASE DE GRUPOS:\n")
    archivo.write("-" * 40 + "\n")
    dieciseisavos = []
    
    for grupo in range(8):
        archivo.write(f"\nGrupo {chr(65 + grupo)}:\n")
        equipos_grupo = equipos_copia[grupo*4:(grupo+1)*4]
        clasificados_grupo = simular_fase_grupos(equipos_grupo, archivo)
        dieciseisavos.extend(clasificados_grupo)
    
    # Dieciseisavos de final (16 equipos - 8 grupos × 2 clasificados)
    num_dieciseisavos = len(dieciseisavos)
    archivo.write(f"\n🎯 DIECISEISAVOS DE FINAL ({num_dieciseisavos} equipos)\n")
    archivo.write("-" * 40 + "\n")
    octavos = []
    
    for i in range(0, num_dieciseisavos, 2):
        if i + 1 < num_dieciseisavos:
            equipo1, equipo2 = dieciseisavos[i], dieciseisavos[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            octavos.append(ganador)
            archivo.write(f"{resultado}\n")
            archivo.write(f"✅ Pasa: {ganador.upper()}\n\n")
        else:
            octavos.append(dieciseisavos[i])
            archivo.write(f"{dieciseisavos[i].upper()} pasa automáticamente (sin oponente)\n")
    
    # Octavos de final (8 equipos)
    num_octavos = len(octavos)
    archivo.write(f"\n🔥 OCTAVOS DE FINAL ({num_octavos} equipos)\n")
    archivo.write("-" * 40 + "\n")
    cuartos = []
    
    for i in range(0, num_octavos, 2):
        if i + 1 < num_octavos:
            equipo1, equipo2 = octavos[i], octavos[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            cuartos.append(ganador)
            archivo.write(f"{resultado}\n")
            archivo.write(f"✅ Pasa: {ganador.upper()}\n\n")
        else:
            cuartos.append(octavos[i])
            archivo.write(f"{octavos[i].upper()} pasa automáticamente (sin oponente)\n")
    
    # Cuartos de final (4 equipos)
    num_cuartos = len(cuartos)
    archivo.write(f"⚡ CUARTOS DE FINAL ({num_cuartos} equipos)\n")
    archivo.write("-" * 40 + "\n")
    semis = []
    
    for i in range(0, num_cuartos, 2):
        if i + 1 < num_cuartos:
            equipo1, equipo2 = cuartos[i], cuartos[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            semis.append(ganador)
            archivo.write(f"{resultado}\n")
            archivo.write(f"✅ Pasa: {ganador.upper()}\n\n")
        else:
            semis.append(cuartos[i])
            archivo.write(f"{cuartos[i].upper()} pasa automáticamente (sin oponente)\n")
    
    # Semifinales (2 equipos)
    num_semis = len(semis)
    archivo.write(f"💫 SEMIFINALES ({num_semis} equipos)\n")
    archivo.write("-" * 40 + "\n")
    finalistas = []
    
    for i in range(0, num_semis, 2):
        if i + 1 < num_semis:
            equipo1, equipo2 = semis[i], semis[i+1]
            ganador, resultado = simular_eliminatoria_con_jugadores(equipo1, equipo2)
            finalistas.append(ganador)
            archivo.write(f"{resultado}\n")
            archivo.write(f"✅ FINALISTA: {ganador.upper()}\n\n")
        else:
            finalistas.append(semis[i])
            archivo.write(f"{semis[i].upper()} pasa automáticamente a la final (sin oponente)\n")
    
    # Final
    if len(finalistas) == 2:
        archivo.write(f"👑 FINAL CONFERENCE LEAGUE\n")
        archivo.write("=" * 40 + "\n")
        campeon, resultado_final = simular_final_con_jugadores(finalistas[0], finalistas[1])
        archivo.write(f"{resultado_final}\n")
        archivo.write(f"🎯 CAMPEÓN CONFERENCE LEAGUE: {campeon.upper()}\n")
    elif len(finalistas) == 1:
        archivo.write(f"👑 FINAL CONFERENCE LEAGUE\n")
        archivo.write("=" * 40 + "\n")
        archivo.write(f"🎯 CAMPEÓN CONFERENCE LEAGUE: {finalistas[0].upper()} (ganador por walkover)\n")
        campeon = finalistas[0]
    else:
        archivo.write("❌ No hay suficientes finalistas\n")
        campeon = ""
    
    base_datos.registrar_campeon('conference', campeon)
    return campeon

def escribir_estadisticas_individuales(archivo):
    """Escribe las estadísticas individuales de jugadores"""
    archivo.write(f"\n{'='*80}\n")
    archivo.write("ESTADÍSTICAS INDIVIDUALES DE LA TEMPORADA\n")
    archivo.write(f"{'='*80}\n")
    
    # Top 10 Goleadores
    top_goleadores = base_datos.obtener_top_goleadores(10)
    archivo.write("\n🥇 TOP 10 GOLEADORES\n")
    archivo.write("-" * 50 + "\n")
    archivo.write(f"{'Pos':<3} {'Jugador':<15} {'Equipo':<8} {'Goles':<6} {'Partidos':<8}\n")
    archivo.write("-" * 50 + "\n")
    
    for i, jugador in enumerate(top_goleadores, 1):
        promedio = jugador.goles / max(1, jugador.partidos_jugados)
        archivo.write(f"{i:<3} {jugador.nombre:<15} {jugador.equipo.upper():<8} "
                     f"{jugador.goles:<6} {jugador.partidos_jugados:<8} ({promedio:.2f} por partido)\n")
    
    # Top 10 Asistentes
    top_asistentes = base_datos.obtener_top_asistentes(10)
    archivo.write(f"\n🎯 TOP 10 ASISTENTES\n")
    archivo.write("-" * 50 + "\n")
    archivo.write(f"{'Pos':<3} {'Jugador':<15} {'Equipo':<8} {'Asist':<6} {'Partidos':<8}\n")
    archivo.write("-" * 50 + "\n")
    
    for i, jugador in enumerate(top_asistentes, 1):
        promedio = jugador.asistencias / max(1, jugador.partidos_jugados)
        archivo.write(f"{i:<3} {jugador.nombre:<15} {jugador.equipo.upper():<8} "
                     f"{jugador.asistencias:<6} {jugador.partidos_jugados:<8} ({promedio:.2f} por partido)\n")
    
    # Top 20 Balón de Oro
    candidatos_balon = base_datos.obtener_candidatos_balon_oro(20)
    archivo.write(f"\n🏆 TOP 20 CANDIDATOS BALÓN DE ORO\n")
    archivo.write("-" * 60 + "\n")
    archivo.write(f"{'Pos':<3} {'Jugador':<15} {'Equipo':<8} {'Goles':<6} {'Asist':<6} {'Puntos':<8}\n")
    archivo.write("-" * 60 + "\n")
    
    for i, (jugador, puntos) in enumerate(candidatos_balon, 1):
        medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i:<3}"
        archivo.write(f"{medalla} {jugador.nombre:<15} {jugador.equipo.upper():<8} "
                     f"{jugador.goles:<6} {jugador.asistencias:<6} {puntos:<8.2f}\n")

def escribir_tabla_liga_mejorada(archivo, nombre_liga: str, tabla: List[Tuple]):
    """Escribe la tabla de una liga con más detalles"""
    archivo.write(f"\n{'='*70}\n")
    archivo.write(f"TABLA FINAL - {nombre_liga.upper()}\n")
    archivo.write(f"{'='*70}\n")
    archivo.write(f"{'Pos':<3} {'Equipo':<12} {'Pts':<4} {'PJ':<3} {'GF':<3} {'GC':<3} {'DG':<4} {'Nivel':<5}\n")
    archivo.write("-" * 70 + "\n")
    
    for i, (equipo, stats) in enumerate(tabla, 1):
        nivel_equipo = base_datos.obtener_nivel_equipo(equipo)
        archivo.write(f"{i:<3} {equipo.upper():<12} {stats['puntos']:<4} {stats['partidos']:<3} "
                     f"{stats['gf']:<3} {stats['gc']:<3} {stats['gd']:+4} {nivel_equipo:<5}\n")
    
    # Mostrar clasificaciones
    archivo.write(f"\nCLASIFICACIONES:\n")
    if nombre_liga in ["Premier League", "La Liga", "Serie A", "Bundesliga"]:
        archivo.write(f"🏆 Champions League: {', '.join([tabla[i][0].upper() for i in range(4)])}\n")
        archivo.write(f"🏅 Europa League: {tabla[4][0].upper()}, {tabla[5][0].upper()}\n")
        archivo.write(f"🎯 Conference League: {tabla[6][0].upper()}\n")
        archivo.write(f"📉 Descenso: {', '.join([tabla[i][0].upper() for i in [-3, -2, -1]])}\n")
    elif nombre_liga == "Ligue 1":
        archivo.write(f"🏆 Champions League: {', '.join([tabla[i][0].upper() for i in range(3)])}\n")
        archivo.write(f"🏅 Europa League: {tabla[3][0].upper()}\n")
        archivo.write(f"🎯 Conference League: {tabla[4][0].upper()}\n")
    elif nombre_liga == "Primeira Liga":
        archivo.write(f"🏆 Champions League: {tabla[0][0].upper()}, {tabla[1][0].upper()}\n")
        archivo.write(f"🏅 Europa League: {tabla[2][0].upper()}, {tabla[3][0].upper()}\n")
        archivo.write(f"🎯 Conference League: {tabla[4][0].upper()}\n")
    elif nombre_liga == "Eredivisie":
        archivo.write(f"🏆 Champions League: {tabla[0][0].upper()}\n")
        archivo.write(f"🏅 Europa League: {tabla[1][0].upper()}, {tabla[2][0].upper()}\n")
        archivo.write(f"🎯 Conference League: {tabla[3][0].upper()}\n")

def main():
    print("🏆 SIMULADOR COMPLETO CON JUGADORES Y COMPETICIONES EUROPEAS 🏆")
    print("=" * 70)
    print("Inicializando base de datos de jugadores...")
    
    # Reset estadísticas para nueva temporada
    base_datos.reset_estadisticas_temporada()
    
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"temporada_completa_{fecha_actual}.txt"
    
    # Obtener estructura de ligas
    ligas = base_datos.obtener_ligas()
    
    print(f"Simulando temporada con {len(base_datos.jugadores)} jugadores en {len(base_datos.equipos)} equipos...")
    
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write("🏆 SIMULACIÓN TEMPORADA EUROPEA COMPLETA CON JUGADORES 🏆\n")
        archivo.write(f"Fecha de simulación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        archivo.write(f"Jugadores simulados: {len(base_datos.jugadores)}\n")
        archivo.write(f"Equipos participantes: {len(base_datos.equipos)}\n")
        archivo.write("=" * 80 + "\n")
        
        # Simular todas las ligas
        print("\n📊 Simulando ligas domésticas...")
        resultados_ligas = {}
        
        for nombre_liga, equipos_dict in ligas.items():
            print(f"🏟️  {nombre_liga}...")
            tabla = simular_liga_con_jugadores(nombre_liga, equipos_dict)
            resultados_ligas[nombre_liga] = tabla
            escribir_tabla_liga_mejorada(archivo, nombre_liga, tabla)
        
        # Obtener clasificados para competiciones europeas
        print("\n🌍 Obteniendo clasificados europeos...")
        champions, europa, conference = obtener_clasificados_europeos(resultados_ligas)
        
        print(f"📊 Clasificados - Champions: {len(champions)}, Europa: {len(europa)}, Conference: {len(conference)}")
        
        # Simular competiciones europeas
        print("\n🏆 Simulando Champions League...")
        campeon_champions = simular_champions_league(champions, archivo)
        
        print("🏅 Simulando Europa League...")
        campeon_europa = simular_europa_league(europa, archivo)
        
        print("🎯 Simulando Conference League...")
        campeon_conference = simular_conference_league(conference, archivo)
        
        # Escribir estadísticas individuales
        print("📊 Generando estadísticas individuales...")
        escribir_estadisticas_individuales(archivo)
        
        # Resumen final
        archivo.write(f"\n{'='*80}\n")
        archivo.write("🏆 RESUMEN FINAL DE LA TEMPORADA 2024/25 🏆\n")
        archivo.write(f"{'='*80}\n")
        
        archivo.write("\n📊 CAMPEONES DE LIGA:\n")
        archivo.write("-" * 50 + "\n")
        for nombre_liga, tabla in resultados_ligas.items():
            nivel_campeon = base_datos.obtener_nivel_equipo(tabla[0][0])
            archivo.write(f"🏆 {nombre_liga:<20}: {tabla[0][0].upper():<15} (Nivel: {nivel_campeon})\n")
        
        archivo.write(f"\n🌍 CAMPEONES EUROPEOS:\n")
        archivo.write("-" * 50 + "\n")
        archivo.write(f"🏆 CAMPEÓN CHAMPIONS LEAGUE: {campeon_champions.upper()}\n")
        archivo.write(f"🏅 CAMPEÓN EUROPA LEAGUE: {campeon_europa.upper()}\n")
        archivo.write(f"🎯 CAMPEÓN CONFERENCE LEAGUE: {campeon_conference.upper()}\n")
        
        # Top 5 goleadores resumido
        top_goleadores = base_datos.obtener_top_goleadores(5)
        archivo.write(f"\n⚽ TOP 5 GOLEADORES DE LA TEMPORADA:\n")
        archivo.write("-" * 50 + "\n")
        for i, jugador in enumerate(top_goleadores, 1):
            medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            archivo.write(f"{medalla} {jugador.nombre} ({jugador.equipo.upper()}) - {jugador.goles} goles\n")
        
        # Ganador Balón de Oro
        candidatos_balon = base_datos.obtener_candidatos_balon_oro(1)
        if candidatos_balon:
            ganador_balon, puntos = candidatos_balon[0]
            archivo.write(f"\n🥇 BALÓN DE ORO 2025: {ganador_balon.nombre.upper()} ({ganador_balon.equipo.upper()})\n")
            archivo.write(f"   Estadísticas: {ganador_balon.goles} goles, {ganador_balon.asistencias} asistencias - {puntos:.2f} puntos\n")
        
        # Estadísticas generales de la temporada
        total_goles = sum(j.goles for j in base_datos.jugadores.values())
        total_partidos = sum(j.partidos_jugados for j in base_datos.jugadores.values())
        
        archivo.write(f"\n📈 ESTADÍSTICAS GENERALES:\n")
        archivo.write("-" * 50 + "\n")
        archivo.write(f"⚽ Total de goles marcados: {total_goles}\n")
        archivo.write(f"🏟️  Total de partidos jugados: {total_partidos // 22} (aprox.)\n")  # Dividir por jugadores promedio por partido
        archivo.write(f"📊 Promedio de goles por partido: {total_goles / (total_partidos // 22):.2f}\n")
    
    print(f"\n✅ Simulación completa guardada en: {nombre_archivo}")
    
    # Mostrar estadísticas destacadas en consola
    print("\n📊 ESTADÍSTICAS DESTACADAS:")
    
    print(f"\n🏆 CAMPEONES EUROPEOS:")
    print(f"   Champions League: {campeon_champions.upper()}")
    print(f"   Europa League: {campeon_europa.upper()}")
    print(f"   Conference League: {campeon_conference.upper()}")
    
    top_goleadores = base_datos.obtener_top_goleadores(3)
    print("\n🥇 TOP 3 GOLEADORES:")
    for i, jugador in enumerate(top_goleadores, 1):
        medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        print(f"  {medalla} {jugador.nombre} ({jugador.equipo.upper()}) - {jugador.goles} goles")
    
    candidatos_balon = base_datos.obtener_candidatos_balon_oro(3)
    print("\n🏆 TOP 3 BALÓN DE ORO:")
    for i, (jugador, puntos) in enumerate(candidatos_balon, 1):
        medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        print(f"  {medalla} {jugador.nombre} ({jugador.equipo.upper()}) - {puntos:.2f} puntos")
    
    print(f"\n🎉 ¡Simulación de la temporada 2024/25 completada!")
    print(f"📁 Revisa el archivo '{nombre_archivo}' para ver todos los detalles.")

if __name__ == "__main__":
    main()