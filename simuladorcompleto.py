import random as rm
from collections import defaultdict
from datetime import datetime

# Equipos por liga con sus niveles
ligas = {
    "Premier League": {
        "mc": 85, "liv": 75, "ars": 60, "che": 74, "mu": 50, "tot": 65,
        "new": 55, "avl": 50, "wes": 45, "bha": 40, "wol": 45, "cry": 40,
        "ful": 40, "eve": 35, "bur": 30, "not": 25, "bou": 35, "shf": 25,
        "lut": 20, "lei": 45,
    },
    "La Liga": {
        "rmd": 82, "bar": 75, "atl": 75, "sev": 50, "bet": 40, "rsoc": 70,
        "vil": 45, "val": 55, "ath": 50, "osa": 45, "get": 40, "ray": 35,
        "cel": 25, "cad": 30, "gra": 25, "las": 35, "alm": 30, "mal": 40,
        "alv": 20, "gir": 30,
    },
    "Serie A": {
        "juv": 79, "int": 75, "mil": 65, "nap": 45, "rom": 50, "laz": 60,
        "ata": 80, "fio": 55, "tor": 45, "udi": 35, "gen": 35, "emp": 30,
        "lec": 25, "ver": 40, "cal": 30, "fro": 25, "sas": 35, "sam": 30,
        "mon": 40, "bol": 20,
    },
    "Bundesliga": {
        "bay": 84, "bvb": 65, "rbz": 70, "lev": 45, "fra": 35, "fre": 35,
        "wol_de": 40, "bmg": 55, "uni": 50, "stu": 20, "may": 35, "hof": 30,
        "aug": 25, "her": 30, "boc": 25, "col": 30, "bre": 30, "dar": 20,
    },
    "Ligue 1": {
        "psg": 70, "mar": 30, "oly": 60, "asm": 40, "ren": 35, "lil": 40,
        "nic": 45, "len": 35, "str": 30, "nan": 25, "rei": 30, "mtp": 25,
        "tou": 30, "lor": 20, "brest": 25, "cle": 20, "metz": 25, "hav": 15,
    },
    "Primeira Liga": {
        "ben": 70, "por": 65, "spo": 45, "bra": 40, "vit": 35, "gui": 30,
        "avo": 25, "mor": 25, "ton": 20, "rio": 25, "csmf": 30, "bel": 20,
        "port": 25, "san": 20, "far": 15, "aro": 20, "viz": 15, "est": 25,
    },
    "Eredivisie": {
        "aja": 25, "psv": 45, "fey": 30, "az": 35, "twn": 30, "vit_nl": 25,
        "uti": 20, "gro": 20, "her_nl": 25, "wil": 15, "hee": 20, "pec": 15,
        "for": 20, "spa_nl": 15, "goe": 10, "cam": 15, "nec": 20, "almc": 25,
    }
}

# Diccionario completo de equipos con sus niveles
todos_equipos = {}
for liga_equipos in ligas.values():
    todos_equipos.update(liga_equipos)

def simular_partido(equipo1, nivel1, equipo2, nivel2):
    """Simula un partido entre dos equipos"""
    gol1, gol2 = 0, 0
    sumalevel = nivel1 + nivel2
    
    for _ in range(90):
        prob = rm.randint(1, 200)
        if prob > 195:
            prob2 = rm.randint(0, sumalevel)        
            if prob2 <= nivel1:
                gol1 += 1
            else:
                gol2 += 1
    
    return gol1, gol2

def simular_liga(nombre_liga, equipos):
    """Simula una liga completa con todos contra todos (ida y vuelta)"""
    equipos_lista = list(equipos.keys())
    tabla = defaultdict(lambda: {'puntos': 0, 'gf': 0, 'gc': 0, 'partidos': 0, 'gd': 0})
    
    for i in range(len(equipos_lista)):
        for j in range(len(equipos_lista)):
            if i != j:
                equipo1 = equipos_lista[i]
                equipo2 = equipos_lista[j]
                nivel1 = equipos[equipo1]
                nivel2 = equipos[equipo2]
                
                gol1, gol2 = simular_partido(equipo1, nivel1, equipo2, nivel2)
                
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
    
    for equipo in tabla:
        tabla[equipo]['gd'] = tabla[equipo]['gf'] - tabla[equipo]['gc']
    
    tabla_ordenada = sorted(tabla.items(), 
                           key=lambda x: (x[1]['puntos'], x[1]['gd'], x[1]['gf']), 
                           reverse=True)
    
    return tabla_ordenada

def obtener_clasificados(resultados_ligas):
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
    
    # Asegurar que tengamos exactamente el número correcto de equipos
    # Champions: necesitamos 32 equipos
    while len(champions) < 32:
        # Agregar mejores equipos de Europa que no estén en Champions
        equipos_restantes = [eq for eq in europa if eq not in champions]
        if equipos_restantes:
            # Ordenar por nivel y tomar el mejor
            mejor_equipo = max(equipos_restantes, key=lambda x: todos_equipos[x])
            champions.append(mejor_equipo)
            europa.remove(mejor_equipo)
        else:
            break
    
    # Europa League: necesitamos 32 equipos  
    while len(europa) < 32:
        # Agregar equipos de Conference que no estén en Europa o Champions
        equipos_restantes = [eq for eq in conference if eq not in europa and eq not in champions]
        if equipos_restantes:
            mejor_equipo = max(equipos_restantes, key=lambda x: todos_equipos[x])
            europa.append(mejor_equipo)
            conference.remove(mejor_equipo)
        else:
            break
    
    # Recortar si hay demasiados equipos
    champions = champions[:32]
    europa = europa[:32]
    conference = conference[:24]  # Para Conference League usamos 24
    
    return champions, europa, conference

def crear_grupos_competicion(equipos, num_grupos):
    """Crea grupos para competiciones europeas"""
    equipos_lista = list(equipos)
    rm.shuffle(equipos_lista)
    
    grupos = {}
    equipos_por_grupo = len(equipos_lista) // num_grupos
    
    # Asegurar que cada grupo tenga al menos 3 equipos
    if equipos_por_grupo < 3:
        equipos_por_grupo = 4
        num_grupos = len(equipos_lista) // 4
    
    for i in range(num_grupos):
        grupo_letra = chr(ord('A') + i)
        inicio = i * equipos_por_grupo
        fin = inicio + equipos_por_grupo
        
        # Para el último grupo, incluir todos los equipos restantes
        if i == num_grupos - 1:
            grupos[grupo_letra] = equipos_lista[inicio:]
        else:
            grupos[grupo_letra] = equipos_lista[inicio:fin]
    
    return grupos

def simular_grupo_europeo(equipos_grupo, todos_equipos):
    """Simula la fase de grupos de competición europea"""
    tabla = defaultdict(lambda: {'puntos': 0, 'gf': 0, 'gc': 0, 'gd': 0, 'partidos': 0})
    
    for i in range(len(equipos_grupo)):
        for j in range(i+1, len(equipos_grupo)):
            equipo1 = equipos_grupo[i]
            equipo2 = equipos_grupo[j]
            nivel1 = todos_equipos[equipo1]
            nivel2 = todos_equipos[equipo2]
            
            # Ida y vuelta
            gol1_ida, gol2_ida = simular_partido(equipo1, nivel1, equipo2, nivel2)
            gol2_vuelta, gol1_vuelta = simular_partido(equipo2, nivel2, equipo1, nivel1)
            
            # Actualizar estadísticas
            tabla[equipo1]['gf'] += gol1_ida + gol1_vuelta
            tabla[equipo1]['gc'] += gol2_ida + gol2_vuelta
            tabla[equipo2]['gf'] += gol2_ida + gol2_vuelta
            tabla[equipo2]['gc'] += gol1_ida + gol1_vuelta
            tabla[equipo1]['partidos'] += 2
            tabla[equipo2]['partidos'] += 2
            
            # Puntos ida
            if gol1_ida > gol2_ida:
                tabla[equipo1]['puntos'] += 3
            elif gol1_ida < gol2_ida:
                tabla[equipo2]['puntos'] += 3
            else:
                tabla[equipo1]['puntos'] += 1
                tabla[equipo2]['puntos'] += 1
                
            # Puntos vuelta
            if gol1_vuelta > gol2_vuelta:
                tabla[equipo1]['puntos'] += 3
            elif gol1_vuelta < gol2_vuelta:
                tabla[equipo2]['puntos'] += 3
            else:
                tabla[equipo1]['puntos'] += 1
                tabla[equipo2]['puntos'] += 1
    
    for equipo in tabla:
        tabla[equipo]['gd'] = tabla[equipo]['gf'] - tabla[equipo]['gc']
    
    tabla_ordenada = sorted(tabla.items(), 
                           key=lambda x: (x[1]['puntos'], x[1]['gd'], x[1]['gf']), 
                           reverse=True)
    
    return tabla_ordenada

def simular_eliminatoria(equipo1, nivel1, equipo2, nivel2):
    """Simula una eliminatoria a doble partido"""
    # Ida y vuelta
    gol1_ida, gol2_ida = simular_partido(equipo1, nivel1, equipo2, nivel2)
    gol2_vuelta, gol1_vuelta = simular_partido(equipo2, nivel2, equipo1, nivel1)
    
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
            # Penales
            prob_pen = rm.randint(0, nivel1 + nivel2)
            ganador = equipo1 if prob_pen <= nivel1 else equipo2
            return ganador, resultado + f" - {ganador.upper()} por penales"

def simular_final(equipo1, nivel1, equipo2, nivel2):
    """Simula una final a un solo partido"""
    goles1, goles2 = simular_partido(equipo1, nivel1, equipo2, nivel2)
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

def simular_competicion_europea(nombre, equipos_participantes, todos_equipos, archivo):
    """Simula una competición europea completa"""
    archivo.write(f"\n{'='*80}\n")
    archivo.write(f"{nombre.upper()} - SIMULACIÓN COMPLETA\n")
    archivo.write(f"{'='*80}\n\n")
    
    # Determinar formato según competición
    if nombre == "Champions League":
        num_grupos = 8
        clasificados_por_grupo = 2
    elif nombre == "Europa League":
        num_grupos = 8  
        clasificados_por_grupo = 2
    else:  # Conference League
        num_grupos = 6
        clasificados_por_grupo = 2
    
    # Fase de grupos
    grupos = crear_grupos_competicion(equipos_participantes, num_grupos)
    archivo.write("FASE DE GRUPOS\n")
    archivo.write("-" * 50 + "\n")
    
    clasificados = []
    
    for letra, equipos_grupo in grupos.items():
        archivo.write(f"\nGRUPO {letra}: {', '.join([eq.upper() for eq in equipos_grupo])}\n")
        tabla = simular_grupo_europeo(equipos_grupo, todos_equipos)
        
        archivo.write(f"{'Pos':<3} {'Equipo':<10} {'Pts':<4} {'PJ':<3} {'GF':<3} {'GC':<3} {'DG':<4}\n")
        archivo.write("-" * 45 + "\n")
        
        for i, (equipo, stats) in enumerate(tabla, 1):
            status = "✓" if i <= clasificados_por_grupo else " "
            archivo.write(f"{status} {i:<2} {equipo.upper():<10} {stats['puntos']:<4} {stats['partidos']:<3} "
                         f"{stats['gf']:<3} {stats['gc']:<3} {stats['gd']:+4}\n")
        
        # Clasificar los primeros equipos de cada grupo
        clasificados_grupo = min(clasificados_por_grupo, len(tabla))
        for i in range(clasificados_grupo):
            clasificados.append(tabla[i][0])
    
    archivo.write(f"\nCLASIFICADOS PARA ELIMINATORIAS: {len(clasificados)} equipos\n")
    archivo.write(", ".join([eq.upper() for eq in clasificados]) + "\n")
    
    # Asegurar que tengamos un número par de equipos para eliminatorias
    if len(clasificados) % 2 != 0:
        clasificados = clasificados[:-1]  # Quitar uno si es impar
    
    # Preparar equipos para eliminatorias
    equipos_actuales = clasificados[:]
    
    # Fases eliminatorias según número de equipos
    num_equipos = len(equipos_actuales)
    if num_equipos >= 16:
        fases = ["OCTAVOS DE FINAL", "CUARTOS DE FINAL", "SEMIFINALES", "FINAL"]
    elif num_equipos >= 8:
        fases = ["CUARTOS DE FINAL", "SEMIFINALES", "FINAL"]
    elif num_equipos >= 4:
        fases = ["SEMIFINALES", "FINAL"]
    else:
        fases = ["FINAL"]
    
    for fase in fases:
        archivo.write(f"\n{fase}\n")
        archivo.write("-" * 50 + "\n")
        
        # Verificar que tengamos suficientes equipos
        if len(equipos_actuales) < 2:
            archivo.write("No hay suficientes equipos para continuar la competición.\n")
            if len(equipos_actuales) == 1:
                archivo.write(f"\n🏆 CAMPEÓN {nombre.upper()}: {equipos_actuales[0].upper()} (Nivel: {todos_equipos[equipos_actuales[0]]})\n")
                return equipos_actuales[0]
            else:
                archivo.write("No hay equipos restantes.\n")
                return None
        
        if fase == "FINAL":
            # Verificar que tengamos exactamente 2 equipos para la final
            if len(equipos_actuales) < 2:
                archivo.write(f"Error: Solo hay {len(equipos_actuales)} equipo(s) para la final.\n")
                if len(equipos_actuales) == 1:
                    archivo.write(f"\n🏆 CAMPEÓN {nombre.upper()}: {equipos_actuales[0].upper()} (Nivel: {todos_equipos[equipos_actuales[0]]})\n")
                    return equipos_actuales[0]
                return None
                
            # Final a un partido
            equipo1, equipo2 = equipos_actuales[0], equipos_actuales[1]
            nivel1, nivel2 = todos_equipos[equipo1], todos_equipos[equipo2]
            campeon, resultado = simular_final(equipo1, nivel1, equipo2, nivel2)
            
            archivo.write(f"FINAL: {resultado}\n")
            archivo.write(f"\n🏆 CAMPEÓN {nombre.upper()}: {campeon.upper()} (Nivel: {todos_equipos[campeon]})\n")
            
            return campeon
        else:
            # Eliminatorias a doble partido
            if len(equipos_actuales) % 2 != 0:
                # Si hay número impar, el último pasa automáticamente
                archivo.write(f"⚠️  {equipos_actuales[-1].upper()} pasa automáticamente a la siguiente ronda (número impar de equipos)\n\n")
                pasa_automatico = equipos_actuales.pop()
            else:
                pasa_automatico = None
            
            rm.shuffle(equipos_actuales)
            siguiente_ronda = []
            
            for i in range(0, len(equipos_actuales), 2):
                if i + 1 < len(equipos_actuales):  # Verificar que haya pareja
                    equipo1 = equipos_actuales[i]
                    equipo2 = equipos_actuales[i+1]
                    nivel1 = todos_equipos[equipo1]
                    nivel2 = todos_equipos[equipo2]
                    
                    ganador, resultado = simular_eliminatoria(equipo1, nivel1, equipo2, nivel2)
                    siguiente_ronda.append(ganador)
                    archivo.write(f"{resultado}\n")
                    archivo.write(f"Clasifica: {ganador.upper()}\n\n")
                else:
                    # Si queda un equipo sin pareja, pasa automáticamente
                    siguiente_ronda.append(equipos_actuales[i])
                    archivo.write(f"⚠️  {equipos_actuales[i].upper()} pasa automáticamente (sin rival)\n\n")
            
            # Agregar el que pasó automáticamente al inicio si existe
            if pasa_automatico:
                siguiente_ronda.append(pasa_automatico)
            
            equipos_actuales = siguiente_ronda

def escribir_tabla_liga(archivo, nombre_liga, tabla):
    """Escribe la tabla de una liga en el archivo"""
    archivo.write(f"\n{'='*60}\n")
    archivo.write(f"TABLA FINAL - {nombre_liga.upper()}\n")
    archivo.write(f"{'='*60}\n")
    archivo.write(f"{'Pos':<3} {'Equipo':<8} {'Pts':<4} {'PJ':<3} {'GF':<3} {'GC':<3} {'DG':<4}\n")
    archivo.write("-" * 60 + "\n")
    
    for i, (equipo, stats) in enumerate(tabla, 1):
        archivo.write(f"{i:<3} {equipo:<8} {stats['puntos']:<4} {stats['partidos']:<3} "
                     f"{stats['gf']:<3} {stats['gc']:<3} {stats['gd']:+4}\n")
    
    archivo.write(f"\nCLASIFICACIONES:\n")
    
    # Clasificaciones según liga
    if nombre_liga in ["Premier League", "La Liga", "Serie A", "Bundesliga"]:
        archivo.write(f"🏆 Champions League: {tabla[0][0]}, {tabla[1][0]}, {tabla[2][0]}, {tabla[3][0]}\n")
        archivo.write(f"🏅 Europa League: {tabla[4][0]}, {tabla[5][0]}\n")
        archivo.write(f"🎯 Conference League: {tabla[6][0]}\n")
        archivo.write(f"📉 Descenso: {tabla[-3][0]}, {tabla[-2][0]}, {tabla[-1][0]}\n")
    elif nombre_liga == "Ligue 1":
        archivo.write(f"🏆 Champions League: {tabla[0][0]}, {tabla[1][0]}, {tabla[2][0]}\n")
        archivo.write(f"🏅 Europa League: {tabla[3][0]}\n")
        archivo.write(f"🎯 Conference League: {tabla[4][0]}\n")
        archivo.write(f"📉 Descenso: {tabla[-3][0]}, {tabla[-2][0]}, {tabla[-1][0]}\n")
    elif nombre_liga == "Primeira Liga":
        archivo.write(f"🏆 Champions League: {tabla[0][0]}, {tabla[1][0]}\n")
        archivo.write(f"🏅 Europa League: {tabla[2][0]}, {tabla[3][0]}\n")
        archivo.write(f"🎯 Conference League: {tabla[4][0]}\n")
        archivo.write(f"📉 Descenso: {tabla[-2][0]}, {tabla[-1][0]}\n")
    elif nombre_liga == "Eredivisie":
        archivo.write(f"🏆 Champions League: {tabla[0][0]}\n")
        archivo.write(f"🏅 Europa League: {tabla[1][0]}, {tabla[2][0]}\n")
        archivo.write(f"🎯 Conference League: {tabla[3][0]}\n")
        archivo.write(f"📉 Descenso: {tabla[-1][0]}\n")

def main():
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"temporada_completa_{fecha_actual}.txt"
    
    print("🏆 SIMULANDO TEMPORADA EUROPEA COMPLETA 🏆")
    print("=" * 60)
    print("Simulando todas las ligas domésticas...")
    
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write("🏆 SIMULACIÓN TEMPORADA EUROPEA COMPLETA 🏆\n")
        archivo.write(f"Fecha de simulación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        archivo.write("=" * 80 + "\n")
        
        # Simular todas las ligas
        resultados_ligas = {}
        
        for nombre_liga, equipos in ligas.items():
            print(f"Simulando {nombre_liga}...")
            tabla = simular_liga(nombre_liga, equipos)
            resultados_ligas[nombre_liga] = tabla
            escribir_tabla_liga(archivo, nombre_liga, tabla)
        
        # Obtener clasificados para competiciones europeas
        champions, europa, conference = obtener_clasificados(resultados_ligas)
        
        # Preparar equipos para Conference League (máximo 24)
        conference_24 = conference[:24]
        
        print("Simulando Champions League...")
        # Simular Champions League (32 equipos)
        campeon_champions = simular_competicion_europea("Champions League", champions, todos_equipos, archivo)
        
        print("Simulando Europa League...")
        # Simular Europa League (32 equipos)
        campeon_europa = simular_competicion_europea("Europa League", europa, todos_equipos, archivo)
        
        print("Simulando Conference League...")
        # Simular Conference League (24 equipos)
        campeon_conference = simular_competicion_europea("Conference League", conference_24, todos_equipos, archivo)
        
        # Resumen final
        archivo.write(f"\n{'='*80}\n")
        archivo.write("RESUMEN FINAL DE LA TEMPORADA\n")
        archivo.write(f"{'='*80}\n")
        
        archivo.write("CAMPEONES DE LIGA:\n")
        for nombre_liga, tabla in resultados_ligas.items():
            archivo.write(f"🏆 {nombre_liga}: {tabla[0][0].upper()} ({todos_equipos[tabla[0][0]]} nivel)\n")
        
        archivo.write(f"\nCAMPEONES EUROPEOS:\n")
        if campeon_champions:
            archivo.write(f"🏆 Champions League: {campeon_champions.upper()} ({todos_equipos[campeon_champions]} nivel)\n")
        if campeon_europa:
            archivo.write(f"🏅 Europa League: {campeon_europa.upper()} ({todos_equipos[campeon_europa]} nivel)\n")
        if campeon_conference:
            archivo.write(f"🎯 Conference League: {campeon_conference.upper()} ({todos_equipos[campeon_conference]} nivel)\n")
    
    print(f"\n✅ Simulación completa guardada en: {nombre_archivo}")
    print("\nRESUMEN RÁPIDO:")
    if campeon_champions:
        print(f"🏆 Champions League: {campeon_champions.upper()}")
    if campeon_europa:
        print(f"🏅 Europa League: {campeon_europa.upper()}")
    if campeon_conference:
        print(f"🎯 Conference League: {campeon_conference.upper()}")

if __name__ == "__main__":
    main()