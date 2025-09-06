import random as rm
from collections import defaultdict
from datetime import datetime
from typing import List, Tuple, Dict
from base_datos import base_datos, Jugador, Equipo

def simular_partido_con_jugadores(equipo1: str, equipo2: str) -> Tuple[int, int, List[Dict]]:
    """
    Simula un partido entre dos equipos registrando estadísticas individuales
    Retorna: (goles_equipo1, goles_equipo2, eventos_del_partido)
    """
    team1 = base_datos.obtener_equipo(equipo1)
    team2 = base_datos.obtener_equipo(equipo2)
    
    if not team1 or not team2:
        return 0, 0, []
    
    nivel1 = team1.calcular_nivel_equipo()
    nivel2 = team2.calcular_nivel_equipo()
    
    gol1, gol2 = 0, 0
    eventos = []
    sumalevel = nivel1 + nivel2
    
    # Actualizar partidos jugados
    for jugador in team1.jugadores:
        jugador.partidos_jugados += 1
        jugador.minutos_jugados += 90
        
    for jugador in team2.jugadores:
        jugador.partidos_jugados += 1
        jugador.minutos_jugados += 90
    
    # Simulación de 90 minutos
    for minuto in range(1, 91):
        prob = rm.randint(1, 200)
        if prob > 195:  # Oportunidad de gol
            prob2 = rm.randint(0, sumalevel)
            
            if prob2 <= nivel1:  # Gol del equipo 1
                goleador, asistente = seleccionar_goleador_y_asistente(team1)
                if goleador:
                    goleador.goles += 1
                    gol1 += 1
                    evento = {
                        'minuto': minuto,
                        'tipo': 'gol',
                        'equipo': equipo1,
                        'goleador': goleador.nombre,
                        'asistente': asistente.nombre if asistente else None
                    }
                    eventos.append(evento)
                    
                    if asistente:
                        asistente.asistencias += 1
            else:  # Gol del equipo 2
                goleador, asistente = seleccionar_goleador_y_asistente(team2)
                if goleador:
                    goleador.goles += 1
                    gol2 += 1
                    evento = {
                        'minuto': minuto,
                        'tipo': 'gol',
                        'equipo': equipo2,
                        'goleador': goleador.nombre,
                        'asistente': asistente.nombre if asistente else None
                    }
                    eventos.append(evento)
                    
                    if asistente:
                        asistente.asistencias += 1
        
        # Simular tarjetas (muy ocasionalmente)
        if prob == 1:  # Tarjeta amarilla
            equipo_tarjeta = team1 if rm.randint(0, sumalevel) <= nivel1 else team2
            jugador_tarjeta = rm.choice(equipo_tarjeta.jugadores)
            jugador_tarjeta.tarjetas_amarillas += 1
            eventos.append({
                'minuto': minuto,
                'tipo': 'tarjeta_amarilla',
                'equipo': equipo1 if equipo_tarjeta == team1 else equipo2,
                'jugador': jugador_tarjeta.nombre
            })
        elif prob == 2:  # Tarjeta roja (muy rara)
            equipo_tarjeta = team1 if rm.randint(0, sumalevel) <= nivel1 else team2
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
    Selecciona quién marca el gol y quién da la asistencia basado en posiciones y niveles
    """
    # Probabilidades por posición para marcar gol
    prob_gol = {"DEL": 0.6, "MED": 0.3, "DEF": 0.08, "POR": 0.02}
    # Probabilidades por posición para dar asistencia
    prob_asist = {"MED": 0.5, "DEL": 0.35, "DEF": 0.13, "POR": 0.02}
    
    # Seleccionar goleador
    goleador = None
    intentos_goleador = 0
    while not goleador and intentos_goleador < 20:
        jugador_candidato = rm.choice(equipo.jugadores)
        prob_posicion = prob_gol.get(jugador_candidato.posicion, 0.1)
        prob_nivel = jugador_candidato.nivel / 100.0
        prob_final = prob_posicion * prob_nivel * 2
        
        if rm.random() < prob_final:
            goleador = jugador_candidato
        intentos_goleador += 1
    
    if not goleador:  # Fallback: cualquier jugador puede marcar
        goleador = rm.choice(equipo.jugadores)
    
    # Seleccionar asistente (diferente al goleador)
    asistente = None
    intentos_asistente = 0
    jugadores_disponibles = [j for j in equipo.jugadores if j != goleador]
    
    while not asistente and intentos_asistente < 15 and jugadores_disponibles:
        jugador_candidato = rm.choice(jugadores_disponibles)
        prob_posicion = prob_asist.get(jugador_candidato.posicion, 0.1)
        prob_nivel = jugador_candidato.nivel / 100.0
        prob_final = prob_posicion * prob_nivel * 1.5
        
        if rm.random() < prob_final:
            asistente = jugador_candidato
        intentos_asistente += 1
    
    # 40% de posibilidad de que no haya asistencia registrada
    if rm.random() < 0.4:
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
                if partidos_simulados % 50 == 0:
                    progreso = (partidos_simulados / partidos_total) * 100
                    print(f"    Progreso: {progreso:.1f}% ({partidos_simulados}/{partidos_total})")
    
    # Calcular diferencia de goles
    for equipo in tabla:
        tabla[equipo]['gd'] = tabla[equipo]['gf'] - tabla[equipo]['gc']
    
    # Ordenar tabla
    tabla_ordenada = sorted(tabla.items(), 
                           key=lambda x: (x[1]['puntos'], x[1]['gd'], x[1]['gf']), 
                           reverse=True)
    
    return tabla_ordenada

def simular_eliminatoria_con_jugadores(equipo1: str, equipo2: str) -> Tuple[str, str]:
    """Simula una eliminatoria a doble partido registrando estadísticas"""
    nivel1 = base_datos.obtener_nivel_equipo(equipo1)
    nivel2 = base_datos.obtener_nivel_equipo(equipo2)
    
    # Ida
    gol1_ida, gol2_ida, eventos_ida = simular_partido_con_jugadores(equipo1, equipo2)
    # Vuelta
    gol2_vuelta, gol1_vuelta, eventos_vuelta = simular_partido_con_jugadores(equipo2, equipo1)
    
    total1 = gol1_ida + gol1_vuelta
    total2 = gol2_ida + gol2_vuelta
    
    resultado = f"{equipo1.upper()} {gol1_ida}-{gol2_ida} {equipo2.upper()} (IDA) | {equipo2.upper()} {gol2_vuelta}-{gol1_vuelta} {equipo1.upper()} (VUELTA) | AGG: {total1}-{total2}"
    
    if total1 > total2:
        return equipo1, resultado
    elif total2 > total1:
        return equipo2, resultado
    else:
        # Goles de visitante o penales
        if gol2_ida > gol1_vuelta:
            return equipo2, resultado + f" - {equipo2.upper()} por goles de visitante"
        elif gol1_vuelta > gol2_ida:
            return equipo1, resultado + f" - {equipo1.upper()} por goles de visitante"
        else:
            # Penales (basado en nivel)
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
    """Obtiene los equipos clasificados para cada competición europea"""
    champions = []
    europa = []
    conference = []
    
    for liga, tabla in resultados_ligas.items():
        if liga in ["Premier League", "La Liga", "Serie A", "Bundesliga"]:
            champions.extend([tabla[0][0], tabla[1][0], tabla[2][0], tabla[3][0]])
            europa.extend([tabla[4][0], tabla[5][0]])
            conference.append(tabla[6][0])
        elif liga == "Ligue 1":
            champions.extend([tabla[0][0], tabla[1][0], tabla[2][0]])
            europa.append(tabla[3][0])
            conference.append(tabla[4][0])
        elif liga == "Primeira Liga":
            champions.extend([tabla[0][0], tabla[1][0]])
            europa.extend([tabla[2][0], tabla[3][0]])
            conference.append(tabla[4][0])
        elif liga == "Eredivisie":
            champions.append(tabla[0][0])
            europa.extend([tabla[1][0], tabla[2][0]])
            conference.append(tabla[3][0])
    
    # Completar con mejores equipos si faltan
    todos_los_equipos = base_datos.obtener_todos_los_equipos()
    
    while len(champions) < 32:
        equipos_restantes = [eq for eq in europa if eq not in champions]
        if equipos_restantes:
            mejor_equipo = max(equipos_restantes, 
                             key=lambda x: todos_los_equipos[x].calcular_nivel_equipo())
            champions.append(mejor_equipo)
            europa.remove(mejor_equipo)
        else:
            break
    
    while len(europa) < 32:
        equipos_restantes = [eq for eq in conference if eq not in europa and eq not in champions]
        if equipos_restantes:
            mejor_equipo = max(equipos_restantes, 
                             key=lambda x: todos_los_equipos[x].calcular_nivel_equipo())
            europa.append(mejor_equipo)
            conference.remove(mejor_equipo)
        else:
            break
    
    return champions[:32], europa[:32], conference[:24]

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
        archivo.write(f"📉 Descenso: {', '.join([tabla[i][0].upper() for i in [-3, -2, -1]])}\n")
    # ... (continuar con otras ligas)

def main():
    print("🏆 SIMULADOR COMPLETO CON JUGADORES 🏆")
    print("=" * 60)
    print("Inicializando base de datos de jugadores...")
    
    # Reset estadísticas para nueva temporada
    base_datos.reset_estadisticas_temporada()
    
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"temporada_jugadores_{fecha_actual}.txt"
    
    # Obtener estructura de ligas
    ligas = base_datos.obtener_ligas()
    
    print(f"Simulando temporada con {len(base_datos.jugadores)} jugadores en {len(base_datos.equipos)} equipos...")
    
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write("🏆 SIMULACIÓN TEMPORADA EUROPEA CON JUGADORES 🏆\n")
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
        print("\n🌍 Clasificando equipos para competiciones europeas...")
        champions, europa, conference = obtener_clasificados_europeos(resultados_ligas)
        
        # Simular competiciones europeas (simplificado para el ejemplo)
        print("🏆 Simulando Champions League...")
        # (Aquí iría la simulación completa de Champions League)
        
        print("🏅 Simulando Europa League...")
        # (Aquí iría la simulación completa de Europa League)
        
        print("🎯 Simulando Conference League...")
        # (Aquí iría la simulación completa de Conference League)
        
        # Escribir estadísticas individuales
        print("📊 Generando estadísticas individuales...")
        escribir_estadisticas_individuales(archivo)
        
        # Resumen final
        archivo.write(f"\n{'='*80}\n")
        archivo.write("RESUMEN FINAL DE LA TEMPORADA\n")
        archivo.write(f"{'='*80}\n")
        
        archivo.write("CAMPEONES DE LIGA:\n")
        for nombre_liga, tabla in resultados_ligas.items():
            nivel_campeon = base_datos.obtener_nivel_equipo(tabla[0][0])
            archivo.write(f"🏆 {nombre_liga}: {tabla[0][0].upper()} (Nivel: {nivel_campeon})\n")
    
    print(f"\n✅ Simulación completa guardada en: {nombre_archivo}")
    
    # Mostrar estadísticas rápidas en consola
    print("\n📊 ESTADÍSTICAS DESTACADAS:")
    top_goleadores = base_datos.obtener_top_goleadores(3)
    print("\n🥇 TOP 3 GOLEADORES:")
    for i, jugador in enumerate(top_goleadores, 1):
        print(f"  {i}. {jugador.nombre} ({jugador.equipo.upper()}) - {jugador.goles} goles")
    
    candidatos_balon = base_datos.obtener_candidatos_balon_oro(3)
    print("\n🏆 TOP 3 BALÓN DE ORO:")
    for i, (jugador, puntos) in enumerate(candidatos_balon, 1):
        medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        print(f"  {medalla} {jugador.nombre} ({jugador.equipo.upper()}) - {puntos:.2f} puntos")

if __name__ == "__main__":
    main()