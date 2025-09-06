import re
import os
from datetime import datetime
from collections import defaultdict

# Niveles originales de equipos (base de datos)
equipos_originales = {
    # Premier League
    "mc": 85, "liv": 75, "ars": 60, "che": 74, "mu": 50, "tot": 65,
    "new": 55, "avl": 50, "wes": 45, "bha": 40, "wol": 45, "cry": 40,
    "ful": 40, "eve": 35, "bur": 30, "not": 25, "bou": 35, "shf": 25,
    "lut": 20, "lei": 45,
    
    # La Liga
    "rmd": 82, "bar": 75, "atl": 75, "sev": 50, "bet": 40, "rsoc": 70,
    "vil": 45, "val": 55, "ath": 50, "osa": 45, "get": 40, "ray": 35,
    "cel": 25, "cad": 30, "gra": 25, "las": 35, "alm": 30, "mal": 40,
    "alv": 20, "gir": 30,
    
    # Serie A
    "juv": 79, "int": 75, "mil": 65, "nap": 45, "rom": 50, "laz": 60,
    "ata": 80, "fio": 55, "tor": 45, "udi": 35, "gen": 35, "emp": 30,
    "lec": 25, "ver": 40, "cal": 30, "fro": 25, "sas": 35, "sam": 30,
    "mon": 40, "bol": 20,
    
    # Bundesliga
    "bay": 84, "bvb": 65, "rbz": 70, "lev": 45, "fra": 35, "fre": 35,
    "wol_de": 40, "bmg": 55, "uni": 50, "stu": 20, "may": 35, "hof": 30,
    "aug": 25, "her": 30, "boc": 25, "col": 30, "bre": 30, "dar": 20,
    
    # Ligue 1
    "psg": 70, "mar": 30, "oly": 60, "asm": 40, "ren": 35, "lil": 40,
    "nic": 45, "len": 35, "str": 30, "nan": 25, "rei": 30, "mtp": 25,
    "tou": 30, "lor": 20, "brest": 25, "cle": 20, "metz": 25, "hav": 15,
    
    # Primeira Liga
    "ben": 70, "por": 65, "spo": 45, "bra": 40, "vit": 35, "gui": 30,
    "avo": 25, "mor": 25, "ton": 20, "rio": 25, "csmf": 30, "bel": 20,
    "port": 25, "san": 20, "far": 15, "aro": 20, "viz": 15, "est": 25,
    
    # Eredivisie
    "aja": 25, "psv": 45, "fey": 30, "az": 35, "twn": 30, "vit_nl": 25,
    "uti": 20, "gro": 20, "her_nl": 25, "wil": 15, "hee": 20, "pec": 15,
    "for": 20, "spa_nl": 15, "goe": 10, "cam": 15, "nec": 20, "almc": 25,
}

def buscar_archivos_temporada():
    """Busca archivos de temporada en el directorio actual"""
    archivos = []
    for archivo in os.listdir('.'):
        if archivo.startswith('temporada_completa_') and archivo.endswith('.txt'):
            archivos.append(archivo)
    
    if not archivos:
        return None
    
    # Ordenar por fecha (más reciente primero)
    archivos.sort(reverse=True)
    return archivos

def extraer_datos_temporada(archivo):
    """Extrae todos los datos relevantes del archivo de temporada"""
    datos = {
        'ligas': {},
        'champions': {},
        'europa': {},
        'conference': {},
        'campeones': {}
    }
    
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Extraer campeones de liga
    ligas_nombres = ["Premier League", "La Liga", "Serie A", "Bundesliga", 
                     "Ligue 1", "Primeira Liga", "Eredivisie"]
    
    for liga in ligas_nombres:
        # Buscar tabla de cada liga
        patron_tabla = rf"TABLA FINAL - {liga.upper()}\n=+\nPos.*?\n-+\n(.*?)(?=\n\nCLASIFICACIONES:)"
        match = re.search(patron_tabla, contenido, re.DOTALL)
        
        if match:
            tabla_texto = match.group(1)
            equipos_liga = []
            
            for linea in tabla_texto.strip().split('\n'):
                if linea.strip():
                    partes = linea.split()
                    if len(partes) >= 7:
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
            
            datos['ligas'][liga] = equipos_liga
    
    # Extraer campeones europeos
    patron_campeon = r"🏆 CAMPEÓN (\w+(?:\s+\w+)*): (\w+)"
    campeones_europeos = re.findall(patron_campeon, contenido)
    
    for competicion, campeon in campeones_europeos:
        datos['campeones'][competicion.lower().replace(' ', '_')] = campeon.lower()
    
    # Extraer rendimiento en competiciones europeas
    # Buscar menciones de equipos en fases europeas
    for competicion in ['CHAMPIONS LEAGUE', 'EUROPA LEAGUE', 'CONFERENCE LEAGUE']:
        patron_comp = rf"{competicion}.*?(?=\n={'='*80}|\Z)"
        match = re.search(patron_comp, contenido, re.DOTALL)
        
        if match:
            comp_texto = match.group(0)
            # Buscar equipos que llegaron a diferentes fases
            datos[competicion.lower().replace(' ', '_')] = analizar_rendimiento_europeo(comp_texto)
    
    return datos

def analizar_rendimiento_europeo(texto_competicion):
    """Analiza qué tan lejos llegó cada equipo en competiciones europeas"""
    rendimiento = {}
    
    # Buscar menciones de equipos en diferentes fases
    fases = {
        'FINAL': 10,
        'SEMIFINAL': 8,
        'CUARTOS DE FINAL': 6,
        'OCTAVOS DE FINAL': 4,
        'GRUPOS': 2
    }
    
    # Extraer todos los equipos mencionados
    equipos_mencionados = re.findall(r'\b([a-z]{2,6})\b', texto_competicion.lower())
    
    for equipo in set(equipos_mencionados):
        if equipo in equipos_originales:
            # Determinar la fase más alta alcanzada
            mejor_fase = 0
            for fase, puntos in fases.items():
                if fase in texto_competicion and equipo.upper() in texto_competicion:
                    # Verificar contexto más específico
                    if re.search(rf'{equipo.upper()}.*?{fase}|{fase}.*?{equipo.upper()}', texto_competicion, re.IGNORECASE):
                        mejor_fase = max(mejor_fase, puntos)
            
            if mejor_fase > 0:
                rendimiento[equipo] = mejor_fase
    
    return rendimiento

def calcular_cambios_nivel(datos):
    """Calcula los cambios de nivel basados en el rendimiento"""
    cambios = {}
    
    for equipo in equipos_originales:
        nivel_original = equipos_originales[equipo]
        cambio_total = 0
        razones = []
        
        # 1. Rendimiento en liga doméstica
        for liga, equipos_liga in datos['ligas'].items():
            equipo_encontrado = None
            for eq_datos in equipos_liga:
                if eq_datos['equipo'] == equipo:
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
                if puntos > (total_equipos * 2):  # Muy buenos puntos
                    cambio_total += 1
                    razones.append("Excelente puntuaje (+1)")
                
                if gd > 20:  # Muy buena diferencia de goles
                    cambio_total += 1
                    razones.append("Excelente diferencia de goles (+1)")
                elif gd < -15:  # Muy mala diferencia
                    cambio_total -= 1
                    razones.append("Diferencia de goles negativa (-1)")
                
                break
        
        # 2. Rendimiento en competiciones europeas
        comp_europeas = ['champions_league', 'europa_league', 'conference_league']
        for comp in comp_europeas:
            if comp in datos and equipo in datos[comp]:
                puntos_comp = datos[comp][equipo]
                
                if puntos_comp >= 10:  # Final
                    cambio_total += 3
                    razones.append(f"Finalista en {comp.replace('_', ' ').title()} (+3)")
                elif puntos_comp >= 8:  # Semifinales
                    cambio_total += 2
                    razones.append(f"Semifinales en {comp.replace('_', ' ').title()} (+2)")
                elif puntos_comp >= 6:  # Cuartos
                    cambio_total += 1
                    razones.append(f"Cuartos en {comp.replace('_', ' ').title()} (+1)")
                elif puntos_comp >= 4:  # Octavos
                    cambio_total += 1
                    razones.append(f"Octavos en {comp.replace('_', ' ').title()} (+1)")
        
        # 3. Bonus por campeonatos europeos
        for comp, campeon in datos['campeones'].items():
            if campeon == equipo:
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
        
        # Calcular nuevo nivel con límites
        nuevo_nivel = max(10, min(95, nivel_original + cambio_total))
        
        if cambio_total != 0 or razones:
            cambios[equipo] = {
                'nivel_original': nivel_original,
                'cambio': cambio_total,
                'nuevo_nivel': nuevo_nivel,
                'razones': razones
            }
    
    return cambios

def generar_archivo_cambios(cambios, archivo_original):
    """Genera el archivo solo con el diccionario actualizado para copiar y pegar"""
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"niveles_actualizados_{fecha_actual}.txt"
    
    # Crear diccionario de nuevos niveles
    nuevos_niveles = equipos_originales.copy()
    for equipo, datos in cambios.items():
        nuevos_niveles[equipo] = datos['nuevo_nivel']
    
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        # Solo generar el código Python actualizado para copiar y pegar
        f.write("equipos_originales = {\n")
        
        # Agrupar por liga para mejor organización
        ligas_grupos = {
            "Premier League": ["mc", "liv", "ars", "che", "mu", "tot", "new", "avl", "wes", "bha", 
                              "wol", "cry", "ful", "eve", "bur", "not", "bou", "shf", "lut", "lei"],
            "La Liga": ["rmd", "bar", "atl", "sev", "bet", "rsoc", "vil", "val", "ath", "osa",
                       "get", "ray", "cel", "cad", "gra", "las", "alm", "mal", "alv", "gir"],
            "Serie A": ["juv", "int", "mil", "nap", "rom", "laz", "ata", "fio", "tor", "udi",
                       "gen", "emp", "lec", "ver", "cal", "fro", "sas", "sam", "mon", "bol"],
            "Bundesliga": ["bay", "bvb", "rbz", "lev", "fra", "fre", "wol_de", "bmg", "uni", "stu",
                          "may", "hof", "aug", "her", "boc", "col", "bre", "dar"],
            "Ligue 1": ["psg", "mar", "oly", "asm", "ren", "lil", "nic", "len", "str", "nan",
                       "rei", "mtp", "tou", "lor", "brest", "cle", "metz", "hav"],
            "Primeira Liga": ["ben", "por", "spo", "bra", "vit", "gui", "avo", "mor", "ton", "rio",
                             "csmf", "bel", "port", "san", "far", "aro", "viz", "est"],
            "Eredivisie": ["aja", "psv", "fey", "az", "twn", "vit_nl", "uti", "gro", "her_nl", "wil",
                          "hee", "pec", "for", "spa_nl", "goe", "cam", "nec", "almc"]
        }
        
        for liga, equipos_liga in ligas_grupos.items():
            f.write(f"    # {liga}\n")
            equipos_linea = []
            for equipo in equipos_liga:
                if equipo in nuevos_niveles:
                    nivel = nuevos_niveles[equipo]
                    equipos_linea.append(f'"{equipo}": {nivel}')
            
            # Escribir en líneas de máximo 4 equipos
            for i in range(0, len(equipos_linea), 4):
                linea = equipos_linea[i:i+4]
                f.write(f"    {', '.join(linea)},\n")
            f.write("\n")
        
        f.write("}")
    
    return nombre_archivo

def main():
    print("🔄 ACTUALIZADOR DE NIVELES DE EQUIPOS 🔄")
    print("=" * 60)
    
    # Buscar archivos de temporada
    archivos = buscar_archivos_temporada()
    
    if not archivos:
        print("❌ No se encontraron archivos de temporada.")
        print("   Asegúrate de que existan archivos que empiecen con 'temporada_completa_'")
        return
    
    # Mostrar archivos disponibles
    print("📁 Archivos de temporada encontrados:")
    for i, archivo in enumerate(archivos, 1):
        fecha_archivo = archivo.replace('temporada_completa_', '').replace('.txt', '')
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
    cambios = calcular_cambios_nivel(datos)
    
    if not cambios:
        print("ℹ️  No se detectaron cambios significativos en los niveles")
        return
    
    # Generar archivo
    print("📝 Generando archivo de cambios...")
    archivo_cambios = generar_archivo_cambios(cambios, archivo_seleccionado)
    
    print(f"\n✅ Análisis completado!")
    print(f"📁 Archivo generado: {archivo_cambios}")
    print(f"📊 Equipos modificados: {len(cambios)}")
    
    # Mostrar resumen rápido
    subidas = len([eq for eq, datos in cambios.items() if datos['cambio'] > 0])
    bajadas = len([eq for eq, datos in cambios.items() if datos['cambio'] < 0])
    
    print(f"⬆️  Equipos que suben: {subidas}")
    print(f"⬇️  Equipos que bajan: {bajadas}")
    
    print(f"\n💡 El archivo '{archivo_cambios}' contiene solo el diccionario actualizado")
    print("   Cópialo y pégalo directamente en tu código para actualizar los niveles.")

if __name__ == "__main__":
    main()