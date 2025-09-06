import re
import os
from datetime import datetime
from collections import defaultdict
from base_datos import base_datos

def buscar_archivos_temporada():
    """Busca archivos de temporada en el directorio actual"""
    archivos = []
    for archivo in os.listdir('.'):
        if (archivo.startswith('temporada_completa_') or archivo.startswith('temporada_jugadores_')) and archivo.endswith('.txt'):
            archivos.append(archivo)
    
    if not archivos:
        return None
    
    # Ordenar por fecha (más reciente primero)
    archivos.sort(reverse=True)
    return archivos

def extraer_datos_temporada(archivo):
    """Extrae datos de rendimiento de equipos y jugadores del archivo"""
    datos = {
        'ligas': {},
        'champions': {},
        'europa': {},
        'conference': {},
        'campeones': {},
        'jugadores': {}
    }
    
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Extraer tablas de liga
    ligas_nombres = ["Premier League", "La Liga", "Serie A", "Bundesliga", 
                     "Ligue 1", "Primeira Liga", "Eredivisie"]
    
    for liga in ligas_nombres:
        patron_tabla = rf"TABLA FINAL - {liga.upper()}\n=+\n.*?\n-+\n(.*?)(?=\n\nCLASIFICACIONES:|\n\n[A-Z]|\Z)"
        match = re.search(patron_tabla, contenido, re.DOTALL)
        
        if match:
            tabla_texto = match.group(1)
            equipos_liga = []
            
            for linea in tabla_texto.strip().split('\n'):
                if linea.strip() and not linea.startswith('=') and not linea.startswith('-'):
                    partes = linea.split()
                    if len(partes) >= 7:
                        try:
                            pos = int(partes[0])
                            equipo = partes[1].lower()
                            puntos = int(partes[2])
                            gf = int(partes[4])
                            gc = int(partes[5])
                            gd = int(partes[6])
                            
                            equipos_liga.append({
                                'equipo': equipo,
                                'posicion': pos,
                                'puntos': puntos,
                                'gf': gf,
                                'gc': gc,
                                'gd': gd
                            })
                        except (ValueError, IndexError):
                            continue
            
            datos['ligas'][liga] = equipos_liga
    
    # Extraer estadísticas de jugadores si existen
    patron_goleadores = r"TOP 10 GOLEADORES\n-+\n.*?\n-+\n(.*?)(?=\n\n🎯|\n\n[A-Z])"
    match_goleadores = re.search(patron_goleadores, contenido, re.DOTALL)
    
    if match_goleadores:
        goleadores_texto = match_goleadores.group(1)
        for linea in goleadores_texto.strip().split('\n'):
            if linea.strip():
                # Formato esperado: "1   Haaland        MC       23     38"
                partes = linea.split()
                if len(partes) >= 5:
                    try:
                        nombre = partes[1]
                        equipo = partes[2].lower()
                        goles = int(partes[3])
                        datos['jugadores'][f"{equipo}_{nombre}"] = {'goles': goles, 'asistencias': 0}
                    except (ValueError, IndexError):
                        continue
    
    # Extraer campeones europeos
    patron_campeon = r"🏆 CAMPEÓN (\w+(?:\s+\w+)*): (\w+)"
    campeones_europeos = re.findall(patron_campeon, contenido)
    
    for competicion, campeon in campeones_europeos:
        datos['campeones'][competicion.lower().replace(' ', '_')] = campeon.lower()
    
    return datos

def calcular_cambios_jugadores(datos):
    """Calcula cambios en los niveles de jugadores basado en rendimiento"""
    cambios_jugadores = {}
    
    # Cambios por rendimiento individual
    for jugador_key, stats in datos.get('jugadores', {}).items():
        if '_' in jugador_key:
            equipo, nombre = jugador_key.split('_', 1)
            jugador_obj = None
            
            # Buscar el jugador en la base de datos
            equipo_obj = base_datos.obtener_equipo(equipo)
            if equipo_obj:
                for j in equipo_obj.jugadores:
                    if j.nombre.lower() == nombre.lower():
                        jugador_obj = j
                        break
            
            if jugador_obj:
                cambio = 0
                razones = []
                
                # Cambios por goles
                goles = stats.get('goles', 0)
                if goles >= 30:  # Temporada excepcional
                    cambio += 3
                    razones.append(f"Temporada excepcional: {goles} goles (+3)")
                elif goles >= 20:  # Muy buena temporada
                    cambio += 2
                    razones.append(f"Muy buena temporada: {goles} goles (+2)")
                elif goles >= 10:  # Buena temporada
                    cambio += 1
                    razones.append(f"Buena temporada: {goles} goles (+1)")
                
                # Cambios por asistencias
                asistencias = stats.get('asistencias', 0)
                if asistencias >= 20:
                    cambio += 2
                    razones.append(f"Excelente en asistencias: {asistencias} (+2)")
                elif asistencias >= 10:
                    cambio += 1
                    razones.append(f"Buenas asistencias: {asistencias} (+1)")
                
                # Bonus por combinación goles+asistencias
                total_contribucion = goles + asistencias
                if total_contribucion >= 40:
                    cambio += 2
                    razones.append(f"Contribución total excepcional: {total_contribucion} G+A (+2)")
                elif total_contribucion >= 25:
                    cambio += 1
                    razones.append(f"Excelente contribución: {total_contribucion} G+A (+1)")
                
                if cambio > 0:
                    cambios_jugadores[jugador_key] = {
                        'jugador': jugador_obj,
                        'nivel_actual': jugador_obj.nivel,
                        'cambio': min(cambio, 5),  # Máximo +5
                        'nuevo_nivel': min(99, jugador_obj.nivel + min(cambio, 5)),
                        'razones': razones
                    }
    
    return cambios_jugadores

def calcular_cambios_equipos(datos):
    """Calcula cambios de nivel para equipos basado en rendimiento de liga y competiciones"""
    cambios_equipos = {}
    
    # Obtener todos los equipos de la base de datos
    todos_equipos = base_datos.obtener_todos_los_equipos()
    
    for codigo, equipo in todos_equipos.items():
        nivel_actual = equipo.calcular_nivel_equipo()
        cambio_total = 0
        razones = []
        
        # 1. Rendimiento en liga doméstica
        for liga, equipos_liga in datos['ligas'].items():
            equipo_encontrado = None
            for eq_datos in equipos_liga:
                if eq_datos['equipo'] == codigo:
                    equipo_encontrado = eq_datos
                    break
            
            if equipo_encontrado:
                pos = equipo_encontrado['posicion']
                puntos = equipo_encontrado['puntos']
                gd = equipo_encontrado['gd']
                
                # Cambios por posición en liga
                if pos == 1:  # Campeón
                    cambio_pos = +3
                    razones.append(f"Campeón de {liga} (+3)")
                elif pos <= 4:  # Top 4
                    cambio_pos = +2
                    razones.append(f"Top 4 en {liga} (+2)")
                elif pos <= 7:  # Top 7
                    cambio_pos = +1
                    razones.append(f"Top 7 en {liga} (+1)")
                elif pos <= 10:  # Media tabla
                    cambio_pos = 0
                elif pos <= 15:  # Parte baja
                    cambio_pos = -1
                    razones.append(f"Posición {pos} en {liga} (-1)")
                else:  # Zona de descenso
                    cambio_pos = -2
                    razones.append(f"Zona baja/descenso en {liga} (-2)")
                
                cambio_total += cambio_pos
                
                # Bonus por rendimiento excepcional
                total_equipos = len(equipos_liga)
                if puntos > (total_equipos * 2.2):  # Muy buenos puntos
                    cambio_total += 1
                    razones.append("Excelente puntuaje (+1)")
                
                if gd > 25:  # Muy buena diferencia de goles
                    cambio_total += 1
                    razones.append("Excelente diferencia de goles (+1)")
                elif gd < -20:  # Muy mala diferencia
                    cambio_total -= 1
                    razones.append("Diferencia de goles muy negativa (-1)")
                
                break
        
        # 2. Campeonatos europeos
        for comp, campeon in datos['campeones'].items():
            if campeon == codigo:
                if 'champions' in comp:
                    cambio_total += 5
                    razones.append("CAMPEÓN CHAMPIONS LEAGUE (+5)")
                elif 'europa' in comp:
                    cambio_total += 3
                    razones.append("CAMPEÓN EUROPA LEAGUE (+3)")
                elif 'conference' in comp:
                    cambio_total += 2
                    razones.append("CAMPEÓN CONFERENCE LEAGUE (+2)")
        
        # Aplicar límites realistas
        cambio_total = max(-5, min(8, cambio_total))
        
        # Solo registrar cambios significativos
        if cambio_total != 0 or razones:
            cambios_equipos[codigo] = {
                'equipo': equipo,
                'nivel_actual': nivel_actual,
                'cambio': cambio_total,
                'nuevo_nivel': max(40, min(95, nivel_actual + cambio_total)),
                'razones': razones
            }
    
    return cambios_equipos

def aplicar_cambios_jugadores(cambios_jugadores):
    """Aplica los cambios calculados a los jugadores"""
    for jugador_key, datos_cambio in cambios_jugadores.items():
        jugador = datos_cambio['jugador']
        jugador.nivel = datos_cambio['nuevo_nivel']

def aplicar_cambios_equipos_a_jugadores(cambios_equipos):
    """Aplica cambios generales a todos los jugadores de equipos que cambiaron"""
    for codigo_equipo, datos_cambio in cambios_equipos.items():
        if datos_cambio['cambio'] != 0:
            equipo = datos_cambio['equipo']
            cambio_general = max(-2, min(2, datos_cambio['cambio'] // 2))  # Cambio más moderado para jugadores
            
            for jugador in equipo.jugadores:
                # Aplicar cambio general pero con variación aleatoria
                import random
                variacion = random.randint(-1, 1)
                cambio_individual = cambio_general + variacion
                nuevo_nivel = max(45, min(95, jugador.nivel + cambio_individual))
                jugador.nivel = nuevo_nivel

def generar_reporte_cambios(cambios_jugadores, cambios_equipos, archivo_original):
    """Genera un reporte completo de los cambios realizados"""
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"reporte_cambios_{fecha_actual}.txt"
    
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write("📊 REPORTE DE CAMBIOS DE NIVELES\n")
        f.write(f"{'='*60}\n")
        f.write(f"Archivo analizado: {archivo_original}\n")
        f.write(f"Fecha de análisis: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"{'='*60}\n\n")
        
        # Cambios de jugadores
        if cambios_jugadores:
            f.write("🌟 CAMBIOS INDIVIDUALES DE JUGADORES\n")
            f.write("-" * 50 + "\n")
            
            # Agrupar por equipo
            jugadores_por_equipo = {}
            for jugador_key, datos in cambios_jugadores.items():
                equipo_codigo = datos['jugador'].equipo
                if equipo_codigo not in jugadores_por_equipo:
                    jugadores_por_equipo[equipo_codigo] = []
                jugadores_por_equipo[equipo_codigo].append((jugador_key, datos))
            
            for equipo_codigo in sorted(jugadores_por_equipo.keys()):
                equipo_obj = base_datos.obtener_equipo(equipo_codigo)
                f.write(f"\n🏟️ {equipo_obj.nombre.upper()} ({equipo_codigo.upper()}):\n")
                
                for jugador_key, datos in jugadores_por_equipo[equipo_codigo]:
                    jugador = datos['jugador']
                    f.write(f"  • {jugador.nombre} ({jugador.posicion}): {datos['nivel_actual']} → {datos['nuevo_nivel']} ({datos['cambio']:+d})\n")
                    for razon in datos['razones']:
                        f.write(f"    - {razon}\n")
                    f.write("\n")
        
        # Cambios de equipos
        if cambios_equipos:
            f.write("\n🏆 CAMBIOS DE NIVELES DE EQUIPOS\n")
            f.write("-" * 50 + "\n")
            
            # Separar por tipo de cambio
            mejoras = [(k, v) for k, v in cambios_equipos.items() if v['cambio'] > 0]
            descensos = [(k, v) for k, v in cambios_equipos.items() if v['cambio'] < 0]
            
            if mejoras:
                f.write("\n⬆️ EQUIPOS QUE MEJORAN:\n")
                for codigo, datos in sorted(mejoras, key=lambda x: x[1]['cambio'], reverse=True):
                    f.write(f"  🔥 {datos['equipo'].nombre.upper()} ({codigo.upper()}): "
                           f"{datos['nivel_actual']} → {datos['nuevo_nivel']} ({datos['cambio']:+d})\n")
                    for razon in datos['razones']:
                        f.write(f"     - {razon}\n")
                    f.write("\n")
            
            if descensos:
                f.write("\n⬇️ EQUIPOS QUE DECLINAN:\n")
                for codigo, datos in sorted(descensos, key=lambda x: x[1]['cambio']):
                    f.write(f"  📉 {datos['equipo'].nombre.upper()} ({codigo.upper()}): "
                           f"{datos['nivel_actual']} → {datos['nuevo_nivel']} ({datos['cambio']:+d})\n")
                    for razon in datos['razones']:
                        f.write(f"     - {razon}\n")
                    f.write("\n")
        
        # Estadísticas generales
        f.write(f"\n📈 RESUMEN ESTADÍSTICO\n")
        f.write("-" * 30 + "\n")
        f.write(f"Jugadores modificados: {len(cambios_jugadores)}\n")
        f.write(f"Equipos modificados: {len(cambios_equipos)}\n")
        
        if cambios_equipos:
            mejoras_count = len([v for v in cambios_equipos.values() if v['cambio'] > 0])
            descensos_count = len([v for v in cambios_equipos.values() if v['cambio'] < 0])
            f.write(f"Equipos que mejoran: {mejoras_count}\n")
            f.write(f"Equipos que declinan: {descensos_count}\n")
    
    return nombre_archivo

def generar_base_datos_actualizada():
    """Genera un nuevo archivo de base de datos con los niveles actualizados"""
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"base_datos_actualizada_{fecha_actual}.py"
    
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write("# Base de datos actualizada con cambios de temporada\n")
        f.write(f"# Generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        
        f.write("from dataclasses import dataclass\n")
        f.write("from typing import Dict, List\n")
        f.write("import random\n\n")
        
        # Copiar las clases de la base de datos original
        f.write("@dataclass\n")
        f.write("class Jugador:\n")
        f.write('    """Clase que representa a un jugador"""\n')
        f.write("    nombre: str\n")
        f.write("    posicion: str  # POR, DEF, MED, DEL\n")
        f.write("    nivel: int     # 1-99\n")
        f.write("    equipo: str\n")
        f.write("    goles: int = 0\n")
        f.write("    asistencias: int = 0\n")
        f.write("    partidos_jugados: int = 0\n")
        f.write("    minutos_jugados: int = 0\n")
        f.write("    tarjetas_amarillas: int = 0\n")
        f.write("    tarjetas_rojas: int = 0\n\n")
        
        f.write("    def calcular_puntos_balon_oro(self) -> float:\n")
        f.write('        """Calcula los puntos para el Balón de Oro"""\n')
        f.write("        puntos_base = (self.goles * 2.0) + (self.asistencias * 1.5)\n")
        f.write("        multiplicador_nivel = self.nivel / 85.0\n")
        f.write("        multiplicador_partidos = min(1.0, self.partidos_jugados / 30.0)\n")
        f.write("        return puntos_base * multiplicador_nivel * multiplicador_partidos\n\n")
        
        # Exportar todos los jugadores con sus niveles actualizados
        f.write("# Jugadores actualizados por equipo\n")
        f.write("JUGADORES_ACTUALIZADOS = {\n")
        
        for codigo_equipo, equipo in base_datos.equipos.items():
            f.write(f'    "{codigo_equipo}": [\n')
            for jugador in equipo.jugadores:
                f.write(f'        ("{jugador.nombre}", "{jugador.posicion}", {jugador.nivel}),\n')
            f.write("    ],\n")
        
        f.write("}\n\n")
        
        # Generar función para recrear la base de datos
        f.write("def crear_base_datos_actualizada():\n")
        f.write('    """Crea la base de datos con los niveles actualizados"""\n')
        f.write("    # Esta función debería recrear toda la estructura de BaseDatos\n")
        f.write("    # usando los niveles actualizados en JUGADORES_ACTUALIZADOS\n")
        f.write("    pass\n")
    
    return nombre_archivo

def mostrar_preview_cambios(cambios_jugadores, cambios_equipos):
    """Muestra un preview de los cambios que se van a aplicar"""
    print(f"\n📊 PREVIEW DE CAMBIOS")
    print("=" * 50)
    
    if cambios_jugadores:
        print(f"\n🌟 JUGADORES A MODIFICAR ({len(cambios_jugadores)}):")
        
        # Mostrar solo los 10 cambios más significativos
        cambios_ordenados = sorted(cambios_jugadores.items(), 
                                 key=lambda x: abs(x[1]['cambio']), reverse=True)[:10]
        
        for jugador_key, datos in cambios_ordenados:
            jugador = datos['jugador']
            cambio_str = f"{datos['cambio']:+d}"
            print(f"  • {jugador.nombre} ({jugador.equipo.upper()}): {datos['nivel_actual']} → {datos['nuevo_nivel']} ({cambio_str})")
        
        if len(cambios_jugadores) > 10:
            print(f"  ... y {len(cambios_jugadores) - 10} cambios más")
    
    if cambios_equipos:
        print(f"\n🏆 EQUIPOS A MODIFICAR ({len(cambios_equipos)}):")
        
        cambios_ordenados = sorted(cambios_equipos.items(), 
                                 key=lambda x: abs(x[1]['cambio']), reverse=True)
        
        for codigo, datos in cambios_ordenados[:10]:
            cambio_str = f"{datos['cambio']:+d}"
            print(f"  • {datos['equipo'].nombre} ({codigo.upper()}): {datos['nivel_actual']} → {datos['nuevo_nivel']} ({cambio_str})")

def main():
    print("🔄 ACTUALIZADOR DE NIVELES CON JUGADORES 🔄")
    print("=" * 60)
    
    # Buscar archivos de temporada
    archivos = buscar_archivos_temporada()
    
    if not archivos:
        print("❌ No se encontraron archivos de temporada.")
        print("   Busque archivos que empiecen con 'temporada_completa_' o 'temporada_jugadores_'")
        return
    
    # Mostrar archivos disponibles
    print("📁 Archivos de temporada encontrados:")
    for i, archivo in enumerate(archivos, 1):
        fecha_archivo = archivo.replace('temporada_completa_', '').replace('temporada_jugadores_', '').replace('.txt', '')
        print(f"   {i}. {archivo} ({fecha_archivo})")
    
    # Seleccionar archivo
    if len(archivos) == 1:
        archivo_seleccionado = archivos[0]
        print(f"\n✅ Usando automáticamente: {archivo_seleccionado}")
    else:
        try:
            opcion = int(input(f"\nSeleccione archivo (1-{len(archivos)}) o Enter para el más reciente: ") or "1")
            archivo_seleccionado = archivos[opcion-1]
        except (ValueError, IndexError):
            archivo_seleccionado = archivos[0]
            print(f"✅ Usando archivo más reciente: {archivo_seleccionado}")
    
    print(f"\n🔍 Analizando temporada: {archivo_seleccionado}")
    
    # Extraer datos
    try:
        datos = extraer_datos_temporada(archivo_seleccionado)
        print("✅ Datos extraídos correctamente")
    except Exception as e:
        print(f"❌ Error al extraer datos: {e}")
        return
    
    # Calcular cambios
    print("🧮 Calculando cambios de nivel...")
    cambios_jugadores = calcular_cambios_jugadores(datos)
    cambios_equipos = calcular_cambios_equipos(datos)
    
    if not cambios_jugadores and not cambios_equipos:
        print("ℹ️  No se detectaron cambios significativos")
        return
    
    # Mostrar preview
    mostrar_preview_cambios(cambios_jugadores, cambios_equipos)
    
    # Confirmar aplicación de cambios
    respuesta = input("\n❓ ¿Aplicar estos cambios? (s/N): ").strip().lower()
    if respuesta != 's':
        print("❌ Cambios cancelados")
        return
    
    # Aplicar cambios
    print("⚡ Aplicando cambios...")
    if cambios_jugadores:
        aplicar_cambios_jugadores(cambios_jugadores)
        print(f"✅ Actualizados {len(cambios_jugadores)} jugadores")
    
    if cambios_equipos:
        aplicar_cambios_equipos_a_jugadores(cambios_equipos)
        print(f"✅ Actualizados jugadores de {len(cambios_equipos)} equipos")
    
    # Generar reportes
    print("📝 Generando reportes...")
    archivo_reporte = generar_reporte_cambios(cambios_jugadores, cambios_equipos, archivo_seleccionado)
    archivo_bd_actualizada = generar_base_datos_actualizada()
    
    print(f"\n✅ Actualización completada!")
    print(f"📁 Reporte generado: {archivo_reporte}")
    print(f"📁 Base de datos actualizada: {archivo_bd_actualizada}")
    
    # Mostrar estadísticas finales
    total_jugadores_modificados = len(cambios_jugadores)
    total_equipos_modificados = len(cambios_equipos)
    
    if cambios_equipos:
        mejoras = len([v for v in cambios_equipos.values() if v['cambio'] > 0])
        descensos = len([v for v in cambios_equipos.values() if v['cambio'] < 0])
        
        print(f"📊 Resumen:")
        print(f"   🌟 Jugadores modificados: {total_jugadores_modificados}")
        print(f"   🏆 Equipos modificados: {total_equipos_modificados}")
        print(f"   ⬆️  Equipos que mejoran: {mejoras}")
        print(f"   ⬇️  Equipos que declinan: {descensos}")
    
    print(f"\n💡 Los cambios se han aplicado a la base de datos en memoria.")
    print(f"   Ejecute el simulador para usar los niveles actualizados.")

if __name__ == "__main__":
    main()