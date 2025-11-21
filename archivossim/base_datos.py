from dataclasses import dataclass
from typing import Dict, List
import random

@dataclass
class Jugador:
    """Clase que representa a un jugador"""
    nombre: str
    posicion: str
    nivel: int
    equipo: str
    goles: int = 0
    asistencias: int = 0
    partidos_jugados: int = 0
    minutos_jugados: int = 0
    tarjetas_amarillas: int = 0
    tarjetas_rojas: int = 0
    titulos_colectivos: int = 0  # Nuevo campo para títulos
    
    def calcular_puntos_balon_oro(self, equipo_campeon: bool = False) -> float:
        """Calcula los puntos para el Balón de Oro considerando títulos colectivos"""
        # Fórmula base: goles y asistencias
        puntos_base = (self.goles * 2.0) + (self.asistencias * 1.5)
        
        # Multiplicadores
        multiplicador_nivel = self.nivel / 85.0
        multiplicador_partidos = min(1.0, self.partidos_jugados / 30.0)
        
        # BONUS POR TÍTULOS COLECTIVOS (muy importante)
        bonus_titulos = 1.0
        if equipo_campeon:
            bonus_titulos = 1.5  # 50% más puntos si su equipo es campeón
        elif self.titulos_colectivos > 0:
            bonus_titulos = 1.2  # 20% más puntos si ganó algún título
        
        # BONUS POR RENDIMIENTO EN COMPETICIONES (Champions > Europa > Conference > Liga)
        bonus_competicion = 1.0
        # (Esto se calculará externamente basado en en qué competición destacó)
        
        return puntos_base * multiplicador_nivel * multiplicador_partidos * bonus_titulos * bonus_competicion

@dataclass
class Equipo:
    """Clase que representa a un equipo con sus jugadores"""
    nombre: str
    liga: str
    jugadores: List[Jugador]
    
    def calcular_nivel_equipo(self) -> int:
        """Calcula el nivel del equipo basado en sus jugadores"""
        if not self.jugadores:
            return 50
        
        # Ponderar por posición (delanteros y mediocampistas más importantes para el ataque)
        peso_posiciones = {"POR": 0.8, "DEF": 1.0, "MED": 1.2, "DEL": 1.3}
        
        nivel_total = 0
        peso_total = 0
        
        for jugador in self.jugadores:
            peso = peso_posiciones.get(jugador.posicion, 1.0)
            nivel_total += jugador.nivel * peso
            peso_total += peso
        
        return int(nivel_total / peso_total) if peso_total > 0 else 50
    
    def obtener_jugadores_por_posicion(self, posicion: str) -> List[Jugador]:
        """Obtiene jugadores de una posición específica"""
        return [j for j in self.jugadores if j.posicion == posicion]

# Base de datos completa de equipos y jugadores
class BaseDatos:
    def __init__(self):
        self.equipos: Dict[str, Equipo] = {}
        self.jugadores: Dict[str, Jugador] = {}
        self.campeones = {
            'champions': None,
            'europa': None,
            'conference': None,
            'ligas': {}
        }
        self._crear_base_datos()
    
    def _crear_equipo(self, codigo: str, nombre_completo: str, liga: str, plantilla: List[tuple]) -> Equipo:
        """Crea un equipo con su plantilla completa"""
        jugadores = []
        for nombre, posicion, nivel in plantilla:
            jugador = self._crear_jugador(nombre, posicion, nivel, codigo)
            jugadores.append(jugador)
        
        equipo = Equipo(nombre_completo, liga, jugadores)
        self.equipos[codigo] = equipo
        return equipo
    
    def _crear_jugador(self, nombre: str, posicion: str, nivel: int, equipo: str) -> Jugador:
        """
        Crea un jugador y lo agrega a la base de datos con ID único
        """
        jugador = Jugador(
            nombre=nombre,
            posicion=posicion,
            nivel=nivel,
            equipo=equipo,
            goles=0,
            asistencias=0,
            partidos_jugados=0,
            minutos_jugados=0,
            tarjetas_amarillas=0,
            tarjetas_rojas=0,
            titulos_colectivos=0
        )
        
        # Crear ID único (nombre + equipo)
        jugador_id = f"{nombre}_{equipo}"
        self.jugadores[jugador_id] = jugador
        return jugador
    
    def _crear_base_datos(self):
        """Crea toda la base de datos de equipos y jugadores"""
        
        
        # === LIGA PROFESIONAL ARGENTINA ===
        # === LIGA PROFESIONAL ARGENTINA ===
        # === BRASILEIRÃO (Série A) ===
        
        # === LIGA CHILENA - 20 equipos ===
        self._crear_equipo("colo_colo", "Colo-Colo", "Liga Chilena", [
            ("Cortés", "POR", 78), ("Subero", "DEF", 74), ("Salas", "DEF", 73),
            ("Pizarro", "DEL", 76), ("Gil", "MED", 75), ("Fuentes", "MED", 74),
            ("Rojas", "DEF", 72), ("Solari", "DEL", 75), ("Bolanos", "MED", 73),
            ("Amor", "DEF", 72), ("Costa", "DEL", 74)
        ])

        self._crear_equipo("ucatolica", "Universidad Católica", "Liga Chilena", [
            ("Toselli", "POR", 77), ("Díaz", "DEF", 73), ("Lanaro", "DEF", 72),
            ("Zampedri", "DEL", 75), ("Astudillo", "MED", 74), ("Cepeda", "MED", 73),
            ("Fuenzalida", "DEF", 71), ("Donoso", "DEL", 74), ("Mendez", "MED", 72),
            ("Parot", "DEF", 71), ("Tapia", "DEL", 73)
        ])

        self._crear_equipo("uchile", "Universidad de Chile", "Liga Chilena", [
            ("Castillo", "POR", 75), ("Maidana", "DEF", 72), ("Cornejo", "DEF", 71),
            ("Palacios", "DEL", 74), ("Larrivey", "MED", 73), ("Echeverria", "MED", 72),
            ("Osorio", "DEF", 70), ("Rubio", "DEL", 73), ("Lopez", "MED", 71),
            ("Reyes", "DEF", 70), ("Fernandez", "DEL", 72)
        ])

        self._crear_equipo("cobresal", "Cobresal", "Liga Chilena", [
            ("Santelices", "POR", 74), ("Becer", "DEF", 71), ("Torres", "DEF", 70),
            ("Jorquera", "DEL", 73), ("Mesa", "MED", 72), ("Gonzalez", "MED", 71),
            ("Pizarro", "DEF", 69), ("Valencia", "DEL", 72), ("Rojas", "MED", 70),
            ("Contreras", "DEF", 69), ("Carrasco", "DEL", 71)
        ])

        self._crear_equipo("nublense", "Ñublense", "Liga Chilena", [
            ("López", "POR", 73), ("Carvajal", "DEF", 70), ("Soto", "DEF", 69),
            ("Moya", "DEL", 72), ("Rivera", "MED", 71), ("Valenzuela", "MED", 70),
            ("Rojas", "DEF", 68), ("Gutiérrez", "DEL", 71), ("Martínez", "MED", 69),
            ("Fernández", "DEF", 68), ("Salazar", "DEL", 70)
        ])

        self._crear_equipo("ohiggins", "O'Higgins", "Liga Chilena", [
            ("Carranza", "POR", 72), ("Navarrete", "DEF", 69), ("Fuentes", "DEF", 68),
            ("Cepeda", "DEL", 71), ("Torres", "MED", 70), ("Gutiérrez", "MED", 69),
            ("Silva", "DEF", 67), ("Rojas", "DEL", 70), ("Vargas", "MED", 68),
            ("Muñoz", "DEF", 67), ("Contreras", "DEL", 69)
        ])

        self._crear_equipo("audax", "Audax Italiano", "Liga Chilena", [
            ("Gómez", "POR", 71), ("Torres", "DEF", 68), ("Reyes", "DEF", 67),
            ("Palma", "DEL", 70), ("Henríquez", "MED", 69), ("Castro", "MED", 68),
            ("Mendoza", "DEF", 66), ("Sáez", "DEL", 69), ("Gutiérrez", "MED", 67),
            ("Vargas", "DEF", 66), ("Fuentes", "DEL", 68)
        ])

        self._crear_equipo("union_esp", "Unión Española", "Liga Chilena", [
            ("Sánchez", "POR", 72), ("Pereira", "DEF", 69), ("González", "DEF", 68),
            ("Córdova", "DEL", 71), ("Farías", "MED", 70), ("Rojas", "MED", 69),
            ("Silva", "DEF", 67), ("Rubio", "DEL", 70), ("Martínez", "MED", 68),
            ("Torres", "DEF", 67), ("García", "DEL", 69)
        ])

        self._crear_equipo("everton", "Everton", "Liga Chilena", [
            ("Vargas", "POR", 71), ("Ceratto", "DEF", 68), ("Oyarzún", "DEF", 67),
            ("Medina", "DEL", 70), ("Luna", "MED", 69), ("Carvajal", "MED", 68),
            ("Riquelme", "DEF", 66), ("Sáez", "DEL", 69), ("Orellana", "MED", 67),
            ("Pizarro", "DEF", 66), ("Ramírez", "DEL", 68)
        ])

        self._crear_equipo("coquimbo", "Coquimbo Unido", "Liga Chilena", [
            ("Velásquez", "POR", 70), ("Cabión", "DEF", 67), ("Torres", "DEF", 66),
            ("Aban", "DEL", 69), ("Gutiérrez", "MED", 68), ("Rojas", "MED", 67),
            ("Pizarro", "DEF", 65), ("Villanueva", "DEL", 68), ("Carvajal", "MED", 66),
            ("Muñoz", "DEF", 65), ("Salinas", "DEL", 67)
        ])

        self._crear_equipo("huachipato", "Huachipato", "Liga Chilena", [
            ("Leyton", "POR", 71), ("Altamirano", "DEF", 68), ("Gutiérrez", "DEF", 67),
            ("Mazzantti", "DEL", 70), ("Martínez", "MED", 69), ("Cárdenas", "MED", 68),
            ("Díaz", "DEF", 66), ("Cruz", "DEL", 69), ("Villanueva", "MED", 67),
            ("Rojas", "DEF", 66), ("Álvarez", "DEL", 68)
        ])

        self._crear_equipo("palestino", "Palestino", "Liga Chilena", [
            ("Rojas", "POR", 70), ("Carrasco", "DEF", 67), ("Corral", "DEF", 66),
            ("Carrasco", "DEL", 69), ("Fuentes", "MED", 68), ("Ahumada", "MED", 67),
            ("Torres", "DEF", 65), ("Dávila", "DEL", 68), ("Rojas", "MED", 66),
            ("González", "DEF", 65), ("Soto", "DEL", 67)
        ])

        self._crear_equipo("curico", "Curicó Unido", "Liga Chilena", [
            ("Mucci", "POR", 69), ("Torres", "DEF", 66), ("Pino", "DEF", 65),
            ("Figueroa", "DEL", 68), ("Ormeño", "MED", 67), ("Cepeda", "MED", 66),
            ("Rojas", "DEF", 64), ("Vilches", "DEL", 67), ("Gutiérrez", "MED", 65),
            ("Muñoz", "DEF", 64), ("Salazar", "DEL", 66)
        ])

        self._crear_equipo("copiapó", "Deportes Copiapó", "Liga Chilena", [
            ("González", "POR", 68), ("Rojas", "DEF", 65), ("Torres", "DEF", 64),
            ("Carvajal", "DEL", 67), ("Martínez", "MED", 66), ("López", "MED", 65),
            ("Silva", "DEF", 63), ("Gutiérrez", "DEL", 66), ("Rojas", "MED", 64),
            ("Muñoz", "DEF", 63), ("Castro", "DEL", 65)
        ])

        self._crear_equipo("magallanes", "Magallanes", "Liga Chilena", [
            ("Castillo", "POR", 67), ("González", "DEF", 64), ("Rojas", "DEF", 63),
            ("Pizarro", "DEL", 66), ("Martínez", "MED", 65), ("López", "MED", 64),
            ("Silva", "DEF", 62), ("Gutiérrez", "DEL", 65), ("Rojas", "MED", 63),
            ("Muñoz", "DEF", 62), ("Castro", "DEL", 64)
        ])

        self._crear_equipo("unionlc", "Unión La Calera", "Liga Chilena", [
            ("Villanueva", "POR", 68), ("Torres", "DEF", 65), ("Rojas", "DEF", 64),
            ("Carvajal", "DEL", 67), ("Martínez", "MED", 66), ("López", "MED", 65),
            ("Silva", "DEF", 63), ("Gutiérrez", "DEL", 66), ("Rojas", "MED", 64),
            ("Muñoz", "DEF", 63), ("Castro", "DEL", 65)
        ])

        self._crear_equipo("antofa", "Deportes Antofagasta", "Liga Chilena", [
            ("Rojas", "POR", 67), ("González", "DEF", 64), ("Torres", "DEF", 63),
            ("Pizarro", "DEL", 66), ("Martínez", "MED", 65), ("López", "MED", 64),
            ("Silva", "DEF", 62), ("Gutiérrez", "DEL", 65), ("Rojas", "MED", 63),
            ("Muñoz", "DEF", 62), ("Castro", "DEL", 64)
        ])

        self._crear_equipo("iquique", "Deportes Iquique", "Liga Chilena", [
            ("González", "POR", 66), ("Rojas", "DEF", 63), ("Torres", "DEF", 62),
            ("Carvajal", "DEL", 65), ("Martínez", "MED", 64), ("López", "MED", 63),
            ("Silva", "DEF", 61), ("Gutiérrez", "DEL", 64), ("Rojas", "MED", 62),
            ("Muñoz", "DEF", 61), ("Castro", "DEL", 63)
        ])

        self._crear_equipo("temuco", "Deportes Temuco", "Liga Chilena", [
            ("Torres", "POR", 65), ("González", "DEF", 62), ("Rojas", "DEF", 61),
            ("Pizarro", "DEL", 64), ("Martínez", "MED", 63), ("López", "MED", 62),
            ("Silva", "DEF", 60), ("Gutiérrez", "DEL", 63), ("Rojas", "MED", 61),
            ("Muñoz", "DEF", 60), ("Castro", "DEL", 62)
        ])

        self._crear_equipo("laserena", "Deportes La Serena", "Liga Chilena", [
            ("Rojas", "POR", 64), ("González", "DEF", 61), ("Torres", "DEF", 60),
            ("Carvajal", "DEL", 63), ("Martínez", "MED", 62), ("López", "MED", 61),
            ("Silva", "DEF", 59), ("Gutiérrez", "DEL", 62), ("Rojas", "MED", 60),
            ("Muñoz", "DEF", 59), ("Castro", "DEL", 61)
        ])

        # === LIGA URUGUAYA - 20 equipos ===
        self._crear_equipo("penarol", "Peñarol", "Liga Uruguaya", [
            ("Dawson", "POR", 77), ("Rodríguez", "DEF", 74), ("González", "DEF", 73),
            ("Aguirre", "DEL", 76), ("Cristóforo", "MED", 75), ("Zeballos", "MED", 74),
            ("Olivera", "DEF", 72), ("Rodríguez", "DEL", 75), ("Sosa", "MED", 73),
            ("Coelho", "DEF", 72), ("López", "DEL", 74)
        ])

        self._crear_equipo("nacional", "Nacional", "Liga Uruguaya", [
            ("Rochet", "POR", 78), ("Polenta", "DEF", 75), ("Marchesín", "DEF", 74),
            ("Bergessio", "DEL", 77), ("Trezza", "MED", 76), ("Ramírez", "MED", 75),
            ("Felipe", "DEF", 73), ("Candido", "DEL", 76), ("Varela", "MED", 74),
            ("Laborda", "DEF", 73), ("Gigantini", "DEL", 75)
        ])

        self._crear_equipo("liverpool_ur", "Liverpool", "Liga Uruguaya", [
            ("López", "POR", 75), ("Pereira", "DEF", 72), ("Silva", "DEF", 71),
            ("Ocampo", "DEL", 74), ("Barboza", "MED", 73), ("Rodríguez", "MED", 72),
            ("Machado", "DEF", 70), ("Medina", "DEL", 73), ("González", "MED", 71),
            ("Fagúndez", "DEF", 70), ("López", "DEL", 72)
        ])

        self._crear_equipo("defensor", "Defensor Sporting", "Liga Uruguaya", [
            ("Irusta", "POR", 74), ("Goyen", "DEF", 71), ("Sant'Anna", "DEF", 70),
            ("Alvarez", "DEL", 73), ("Castro", "MED", 72), ("Gutiérrez", "MED", 71),
            ("Píriz", "DEF", 69), ("Rodríguez", "DEL", 72), ("Machado", "MED", 70),
            ("Coelho", "DEF", 69), ("López", "DEL", 71)
        ])

        self._crear_equipo("wanderers", "Montevideo Wanderers", "Liga Uruguaya", [
            ("De Amores", "POR", 73), ("López", "DEF", 70), ("Gómez", "DEF", 69),
            ("Santos", "DEL", 72), ("Ferreira", "MED", 71), ("Castro", "MED", 70),
            ("Rodríguez", "DEF", 68), ("González", "DEL", 71), ("Silva", "MED", 69),
            ("Pereira", "DEF", 68), ("Martínez", "DEL", 70)
        ])

        self._crear_equipo("fenix", "Fénix", "Liga Uruguaya", [
            ("Gómez", "POR", 72), ("Rodríguez", "DEF", 69), ("Silva", "DEF", 68),
            ("López", "DEL", 71), ("Martínez", "MED", 70), ("González", "MED", 69),
            ("Pereira", "DEF", 67), ("Fernández", "DEL", 70), ("Rodríguez", "MED", 68),
            ("Gómez", "DEF", 67), ("Silva", "DEL", 69)
        ])

        self._crear_equipo("riverplate_ur", "River Plate", "Liga Uruguaya", [
            ("Suárez", "POR", 73), ("Machado", "DEF", 70), ("Rodríguez", "DEF", 69),
            ("Castro", "DEL", 72), ("González", "MED", 71), ("Silva", "MED", 70),
            ("Pereira", "DEF", 68), ("López", "DEL", 71), ("Martínez", "MED", 69),
            ("Gómez", "DEF", 68), ("Rodríguez", "DEL", 70)
        ])

        self._crear_equipo("cerrito", "Cerrito", "Liga Uruguaya", [
            ("Rodríguez", "POR", 71), ("González", "DEF", 68), ("Silva", "DEF", 67),
            ("Martínez", "DEL", 70), ("López", "MED", 69), ("Gómez", "MED", 68),
            ("Pereira", "DEF", 66), ("Rodríguez", "DEL", 69), ("Silva", "MED", 67),
            ("González", "DEF", 66), ("Martínez", "DEL", 68)
        ])

        self._crear_equipo("cerro", "Cerro", "Liga Uruguaya", [
            ("Silva", "POR", 70), ("Rodríguez", "DEF", 67), ("González", "DEF", 66),
            ("López", "DEL", 69), ("Martínez", "MED", 68), ("Gómez", "MED", 67),
            ("Pereira", "DEF", 65), ("Silva", "DEL", 68), ("Rodríguez", "MED", 66),
            ("González", "DEF", 65), ("López", "DEL", 67)
        ])

        self._crear_equipo("bostonriver", "Boston River", "Liga Uruguaya", [
            ("Gómez", "POR", 71), ("Rodríguez", "DEF", 68), ("Silva", "DEF", 67),
            ("López", "DEL", 70), ("Martínez", "MED", 69), ("González", "MED", 68),
            ("Pereira", "DEF", 66), ("Rodríguez", "DEL", 69), ("Silva", "MED", 67),
            ("Gómez", "DEF", 66), ("López", "DEL", 68)
        ])

        self._crear_equipo("danubio", "Danubio", "Liga Uruguaya", [
            ("Rodríguez", "POR", 72), ("González", "DEF", 69), ("Silva", "DEF", 68),
            ("López", "DEL", 71), ("Martínez", "MED", 70), ("Gómez", "MED", 69),
            ("Pereira", "DEF", 67), ("Rodríguez", "DEL", 70), ("Silva", "MED", 68),
            ("González", "DEF", 67), ("López", "DEL", 69)
        ])

        self._crear_equipo("liverpool_ur", "Liverpool", "Liga Uruguaya", [
            ("López", "POR", 73), ("Rodríguez", "DEF", 70), ("González", "DEF", 69),
            ("Silva", "DEL", 72), ("Martínez", "MED", 71), ("Gómez", "MED", 70),
            ("Pereira", "DEF", 68), ("López", "DEL", 71), ("Rodríguez", "MED", 69),
            ("González", "DEF", 68), ("Silva", "DEL", 70)
        ])

        self._crear_equipo("mvdwanderers", "Montevideo Wanderers", "Liga Uruguaya", [
            ("Gómez", "POR", 72), ("Rodríguez", "DEF", 69), ("Silva", "DEF", 68),
            ("López", "DEL", 71), ("Martínez", "MED", 70), ("González", "MED", 69),
            ("Pereira", "DEF", 67), ("Rodríguez", "DEL", 70), ("Silva", "MED", 68),
            ("Gómez", "DEF", 67), ("López", "DEL", 69)
        ])

        self._crear_equipo("plaza", "Plaza Colonia", "Liga Uruguaya", [
            ("Rodríguez", "POR", 71), ("González", "DEF", 68), ("Silva", "DEF", 67),
            ("López", "DEL", 70), ("Martínez", "MED", 69), ("Gómez", "MED", 68),
            ("Pereira", "DEF", 66), ("Rodríguez", "DEL", 69), ("Silva", "MED", 67),
            ("González", "DEF", 66), ("López", "DEL", 68)
        ])

        self._crear_equipo("progreso", "Progreso", "Liga Uruguaya", [
            ("Silva", "POR", 70), ("Rodríguez", "DEF", 67), ("González", "DEF", 66),
            ("López", "DEL", 69), ("Martínez", "MED", 68), ("Gómez", "MED", 67),
            ("Pereira", "DEF", 65), ("Silva", "DEL", 68), ("Rodríguez", "MED", 66),
            ("González", "DEF", 65), ("López", "DEL", 67)
        ])

        self._crear_equipo("racing_ur", "Racing", "Liga Uruguaya", [
            ("Gómez", "POR", 69), ("Rodríguez", "DEF", 66), ("Silva", "DEF", 65),
            ("López", "DEL", 68), ("Martínez", "MED", 67), ("González", "MED", 66),
            ("Pereira", "DEF", 64), ("Rodríguez", "DEL", 67), ("Silva", "MED", 65),
            ("Gómez", "DEF", 64), ("López", "DEL", 66)
        ])

        self._crear_equipo("rentistas", "Rentistas", "Liga Uruguaya", [
            ("Rodríguez", "POR", 68), ("González", "DEF", 65), ("Silva", "DEF", 64),
            ("López", "DEL", 67), ("Martínez", "MED", 66), ("Gómez", "MED", 65),
            ("Pereira", "DEF", 63), ("Rodríguez", "DEL", 66), ("Silva", "MED", 64),
            ("González", "DEF", 63), ("López", "DEL", 65)
        ])

        self._crear_equipo("sudamerica", "Sud América", "Liga Uruguaya", [
            ("Silva", "POR", 67), ("Rodríguez", "DEF", 64), ("González", "DEF", 63),
            ("López", "DEL", 66), ("Martínez", "MED", 65), ("Gómez", "MED", 64),
            ("Pereira", "DEF", 62), ("Silva", "DEL", 65), ("Rodríguez", "MED", 63),
            ("González", "DEF", 62), ("López", "DEL", 64)
        ])

        self._crear_equipo("torque", "Torque", "Liga Uruguaya", [
            ("Gómez", "POR", 66), ("Rodríguez", "DEF", 63), ("Silva", "DEF", 62),
            ("López", "DEL", 65), ("Martínez", "MED", 64), ("González", "MED", 63),
            ("Pereira", "DEF", 61), ("Rodríguez", "DEL", 64), ("Silva", "MED", 62),
            ("Gómez", "DEF", 61), ("López", "DEL", 63)
        ])

        # === LIGA PARAGUAYA - 20 equipos ===
        self._crear_equipo("olimpia", "Olimpia", "Liga Paraguaya", [
            ("Olveira", "POR", 77), ("Salcedo", "DEF", 74), ("Zalazar", "DEF", 73),
            ("Cardozo", "DEL", 76), ("Quintana", "MED", 75), ("Orzusa", "MED", 74),
            ("Pinto", "DEF", 72), ("Toral", "DEL", 75), ("Hugo", "MED", 73),
            ("Báez", "DEF", 72), ("W. González", "DEL", 74)
        ])

        self._crear_equipo("libertad", "Libertad", "Liga Paraguaya", [
            ("M. Silva", "POR", 76), ("P. Velázquez", "DEF", 73), ("M. Espinoza", "DEF", 72),
            ("L. Villalba", "DEL", 75), ("I. Franco", "MED", 74), ("R. Martínez", "MED", 73),
            ("A. Rojas", "DEF", 71), ("H. Paredes", "DEL", 74), ("J. Ferreira", "MED", 72),
            ("C. Campuzano", "DEF", 71), ("D. Mendieta", "DEL", 73)
        ])

        self._crear_equipo("cerro_porteno", "Cerro Porteño", "Liga Paraguaya", [
            ("J. Aguilar", "POR", 75), ("R. Rojas", "DEF", 72), ("A. Benítez", "DEF", 71),
            ("F. Fernández", "DEL", 74), ("L. Riveros", "MED", 73), ("D. Churín", "MED", 72),
            ("C. Arrua", "DEF", 70), ("R. Morales", "DEL", 73), ("J. Núñez", "MED", 71),
            ("M. Corujo", "DEF", 70), ("A. Romero", "DEL", 72)
        ])

        self._crear_equipo("guarani", "Guaraní", "Liga Paraguaya", [
            ("G. Giménez", "POR", 74), ("R. Cáceres", "DEF", 71), ("M. Benítez", "DEF", 70),
            ("F. Báez", "DEL", 73), ("J. Colmán", "MED", 72), ("A. Contrera", "MED", 71),
            ("L. de la Cruz", "DEF", 69), ("R. Bogarín", "DEL", 72), ("M. Villasanti", "MED", 70),
            ("A. Duarte", "DEF", 69), ("J. Mendoza", "DEL", 71)
        ])

        self._crear_equipo("nacional_par", "Nacional", "Liga Paraguaya", [
            ("A. Silva", "POR", 73), ("J. Báez", "DEF", 70), ("C. Ruiz", "DEF", 69),
            ("B. Arce", "DEL", 72), ("R. Rojas", "MED", 71), ("J. González", "MED", 70),
            ("M. Alcaraz", "DEF", 68), ("L. Haedo", "DEL", 71), ("A. Núñez", "MED", 69),
            ("R. Cardozo", "DEF", 68), ("J. Santacruz", "DEL", 70)
        ])

        self._crear_equipo("solamerica", "Sol de América", "Liga Paraguaya", [
            ("R. Muñoz", "POR", 72), ("M. Benítez", "DEF", 69), ("C. Villagra", "DEF", 68),
            ("J. Salinas", "DEL", 71), ("L. Cáceres", "MED", 70), ("R. Martínez", "MED", 69),
            ("A. Rojas", "DEF", 67), ("F. García", "DEL", 70), ("J. Ferreira", "MED", 68),
            ("M. Giménez", "DEF", 67), ("D. Mendieta", "DEL", 69)
        ])

        self._crear_equipo("spquereno", "Sportivo Luqueño", "Liga Paraguaya", [
            ("J. Aguilar", "POR", 71), ("R. Rojas", "DEF", 68), ("A. Benítez", "DEF", 67),
            ("F. Fernández", "DEL", 70), ("L. Riveros", "MED", 69), ("D. Churín", "MED", 68),
            ("C. Arrua", "DEF", 66), ("R. Morales", "DEL", 69), ("J. Núñez", "MED", 67),
            ("M. Corujo", "DEF", 66), ("A. Romero", "DEL", 68)
        ])

        self._crear_equipo("general", "General Caballero", "Liga Paraguaya", [
            ("G. Giménez", "POR", 70), ("R. Cáceres", "DEF", 67), ("M. Benítez", "DEF", 66),
            ("F. Báez", "DEL", 69), ("J. Colmán", "MED", 68), ("A. Contrera", "MED", 67),
            ("L. de la Cruz", "DEF", 65), ("R. Bogarín", "DEL", 68), ("M. Villasanti", "MED", 66),
            ("A. Duarte", "DEF", 65), ("J. Mendoza", "DEL", 67)
        ])

        self._crear_equipo("resistencia", "Resistencia", "Liga Paraguaya", [
            ("A. Silva", "POR", 69), ("J. Báez", "DEF", 66), ("C. Ruiz", "DEF", 65),
            ("B. Arce", "DEL", 68), ("R. Rojas", "MED", 67), ("J. González", "MED", 66),
            ("M. Alcaraz", "DEF", 64), ("L. Haedo", "DEL", 67), ("A. Núñez", "MED", 65),
            ("R. Cardozo", "DEF", 64), ("J. Santacruz", "DEL", 66)
        ])

        self._crear_equipo("tacuary", "Tacuary", "Liga Paraguaya", [
            ("R. Muñoz", "POR", 68), ("M. Benítez", "DEF", 65), ("C. Villagra", "DEF", 64),
            ("J. Salinas", "DEL", 67), ("L. Cáceres", "MED", 66), ("R. Martínez", "MED", 65),
            ("A. Rojas", "DEF", 63), ("F. García", "DEL", 66), ("J. Ferreira", "MED", 64),
            ("M. Giménez", "DEF", 63), ("D. Mendieta", "DEL", 65)
        ])

        self._crear_equipo("trinidense", "Trinidense", "Liga Paraguaya", [
            ("J. Aguilar", "POR", 67), ("R. Rojas", "DEF", 64), ("A. Benítez", "DEF", 63),
            ("F. Fernández", "DEL", 66), ("L. Riveros", "MED", 65), ("D. Churín", "MED", 64),
            ("C. Arrua", "DEF", 62), ("R. Morales", "DEL", 65), ("J. Núñez", "MED", 63),
            ("M. Corujo", "DEF", 62), ("A. Romero", "DEL", 64)
        ])

        self._crear_equipo("guairena", "Guaireña", "Liga Paraguaya", [
            ("G. Giménez", "POR", 66), ("R. Cáceres", "DEF", 63), ("M. Benítez", "DEF", 62),
            ("F. Báez", "DEL", 65), ("J. Colmán", "MED", 64), ("A. Contrera", "MED", 63),
            ("L. de la Cruz", "DEF", 61), ("R. Bogarín", "DEL", 64), ("M. Villasanti", "MED", 62),
            ("A. Duarte", "DEF", 61), ("J. Mendoza", "DEL", 63)
        ])

        self._crear_equipo("12octubre", "12 de Octubre", "Liga Paraguaya", [
            ("A. Silva", "POR", 65), ("J. Báez", "DEF", 62), ("C. Ruiz", "DEF", 61),
            ("B. Arce", "DEL", 64), ("R. Rojas", "MED", 63), ("J. González", "MED", 62),
            ("M. Alcaraz", "DEF", 60), ("L. Haedo", "DEL", 63), ("A. Núñez", "MED", 61),
            ("R. Cardozo", "DEF", 60), ("J. Santacruz", "DEL", 62)
        ])

        self._crear_equipo("independiente", "Independiente", "Liga Paraguaya", [
            ("R. Muñoz", "POR", 64), ("M. Benítez", "DEF", 61), ("C. Villagra", "DEF", 60),
            ("J. Salinas", "DEL", 63), ("L. Cáceres", "MED", 62), ("R. Martínez", "MED", 61),
            ("A. Rojas", "DEF", 59), ("F. García", "DEL", 62), ("J. Ferreira", "MED", 60),
            ("M. Giménez", "DEF", 59), ("D. Mendieta", "DEL", 61)
        ])

        self._crear_equipo("riverplate_par", "River Plate", "Liga Paraguaya", [
            ("J. Aguilar", "POR", 63), ("R. Rojas", "DEF", 60), ("A. Benítez", "DEF", 59),
            ("F. Fernández", "DEL", 62), ("L. Riveros", "MED", 61), ("D. Churín", "MED", 60),
            ("C. Arrua", "DEF", 58), ("R. Morales", "DEL", 61), ("J. Núñez", "MED", 59),
            ("M. Corujo", "DEF", 58), ("A. Romero", "DEL", 60)
        ])

        self._crear_equipo("sanlorenzo_par", "San Lorenzo", "Liga Paraguaya", [
            ("G. Giménez", "POR", 62), ("R. Cáceres", "DEF", 59), ("M. Benítez", "DEF", 58),
            ("F. Báez", "DEL", 61), ("J. Colmán", "MED", 60), ("A. Contrera", "MED", 59),
            ("L. de la Cruz", "DEF", 57), ("R. Bogarín", "DEL", 60), ("M. Villasanti", "MED", 58),
            ("A. Duarte", "DEF", 57), ("J. Mendoza", "DEL", 59)
        ])

        self._crear_equipo("presidente", "Presidente Hayes", "Liga Paraguaya", [
            ("A. Silva", "POR", 61), ("J. Báez", "DEF", 58), ("C. Ruiz", "DEF", 57),
            ("B. Arce", "DEL", 60), ("R. Rojas", "MED", 59), ("J. González", "MED", 58),
            ("M. Alcaraz", "DEF", 56), ("L. Haedo", "DEL", 59), ("A. Núñez", "MED", 57),
            ("R. Cardozo", "DEF", 56), ("J. Santacruz", "DEL", 58)
        ])

        self._crear_equipo("deportivo", "Deportivo Santaní", "Liga Paraguaya", [
            ("R. Muñoz", "POR", 60), ("M. Benítez", "DEF", 57), ("C. Villagra", "DEF", 56),
            ("J. Salinas", "DEL", 59), ("L. Cáceres", "MED", 58), ("R. Martínez", "MED", 57),
            ("A. Rojas", "DEF", 55), ("F. García", "DEL", 58), ("J. Ferreira", "MED", 56),
            ("M. Giménez", "DEF", 55), ("D. Mendieta", "DEL", 57)
        ])

        self._crear_equipo("fernandodela", "Fernando de la Mora", "Liga Paraguaya", [
            ("J. Aguilar", "POR", 59), ("R. Rojas", "DEF", 56), ("A. Benítez", "DEF", 55),
            ("F. Fernández", "DEL", 58), ("L. Riveros", "MED", 57), ("D. Churín", "MED", 56),
            ("C. Arrua", "DEF", 54), ("R. Morales", "DEL", 57), ("J. Núñez", "MED", 55),
            ("M. Corujo", "DEF", 54), ("A. Romero", "DEL", 56)
        ])
        # === LIGA MX (MÉXICO) - 20 equipos ===
        self._crear_equipo("america", "Club América", "Liga MX", [
            ("Ochoa", "POR", 82), ("Reyes", "DEF", 76), ("Valdez", "DEF", 75),
            ("Cáceres", "DEF", 74), ("Fuentes", "DEF", 73), ("Fidalgo", "MED", 77),
            ("Zendejas", "MED", 76), ("Valencia", "DEL", 78), ("Henry", "DEL", 77),
            ("Quiñones", "DEL", 76), ("Sánchez", "MED", 75)
        ])

        self._crear_equipo("chivas", "Guadalajara", "Liga MX", [
            ("Jiménez", "POR", 78), ("Briseño", "DEF", 74), ("Sepúlveda", "DEF", 73),
            ("Mozo", "DEF", 72), ("Oliveira", "DEF", 71), ("Beltran", "MED", 76),
            ("Núñez", "MED", 74), ("Vega", "DEL", 77), ("Ronaldo", "DEL", 75),
            ("Alvarado", "DEL", 74), ("Guzmán", "MED", 73)
        ])

        self._crear_equipo("tigres", "Tigres UANL", "Liga MX", [
            ("Nahuel", "POR", 81), ("Samir", "DEF", 76), ("Reyes", "DEF", 75),
            ("Angulo", "DEF", 74), ("Pizarro", "MED", 77), ("Córdova", "MED", 76),
            ("Gignac", "DEL", 80), ("Ibañez", "DEL", 76), ("Bruno", "MED", 75),
            ("Aquino", "DEL", 75), ("Gorriarán", "MED", 74)
        ])

        self._crear_equipo("monterrey", "Monterrey", "Liga MX", [
            ("Andrada", "POR", 80), ("Medina", "DEF", 76), ("Guzmán", "DEF", 75),
            ("Vásquez", "DEF", 74), ("Gallardo", "DEF", 73), ("Romero", "MED", 77),
            ("Cannobio", "MED", 75), ("Berterame", "DEL", 77), ("Janssen", "DEL", 76),
            ("Meza", "MED", 76), ("Alonso", "MED", 74)
        ])

        self._crear_equipo("cruzazul", "Cruz Azul", "Liga MX", [
            ("Corona", "POR", 79), ("Escobar", "DEF", 74), ("Piovi", "DEF", 73),
            ("Rivero", "DEF", 72), ("Rotondi", "MED", 75), ("Lira", "MED", 74),
            ("Antuna", "DEL", 76), ("Cambindo", "DEL", 74), ("Rodríguez", "DEL", 73),
            ("Huescas", "MED", 73), ("Gutiérrez", "DEF", 72)
        ])

        self._crear_equipo("pumas", "Pumas UNAM", "Liga MX", [
            ("González", "POR", 77), ("Freire", "DEF", 73), ("Ortiz", "DEF", 72),
            ("Bennevendo", "DEF", 71), ("Mozo", "DEF", 72), ("Salvio", "MED", 75),
            ("López", "MED", 74), ("Dinenno", "DEL", 77), ("Rogério", "DEL", 74),
            ("Ruiz", "MED", 73), ("Berkowitz", "MED", 72)
        ])

        self._crear_equipo("toluca", "Toluca", "Liga MX", [
            ("Volpi", "POR", 76), ("Huerta", "DEF", 72), ("Mosquera", "DEF", 71),
            ("Orrantia", "MED", 73), ("Meneses", "DEL", 74), ("Ruíz", "MED", 72),
            ("Gonzalez", "DEF", 70), ("Domínguez", "DEL", 73), ("García", "MED", 71),
            ("Angulo", "DEF", 70), ("López", "DEL", 71)
        ])

        self._crear_equipo("pachuca", "Pachuca", "Liga MX", [
            ("Ustari", "POR", 75), ("Cabral", "DEF", 72), ("Barreiro", "DEF", 71),
            ("De la Rosa", "DEL", 73), ("Idrissi", "MED", 73), ("Hernández", "MED", 72),
            ("Lozano", "DEF", 70), ("Sánchez", "DEL", 72), ("Guzmán", "MED", 71),
            ("Martínez", "DEF", 70), ("Pérez", "DEL", 71)
        ])

        self._crear_equipo("leon", "León", "Liga MX", [
            ("Cota", "POR", 76), ("Tesillo", "DEF", 73), ("Barreiro", "DEF", 72),
            ("Víctor", "MED", 74), ("Rubio", "DEL", 73), ("Rodríguez", "MED", 72),
            ("Moreno", "DEF", 71), ("Davila", "DEL", 73), ("Fernández", "MED", 71),
            ("Ramírez", "DEF", 70), ("Mena", "DEL", 71)
        ])

        self._crear_equipo("tijuana", "Tijuana", "Liga MX", [
            ("Lozano", "POR", 74), ("Rivero", "DEF", 71), ("Díaz", "DEF", 70),
            ("Bou", "DEL", 72), ("Rivera", "MED", 71), ("Guzmán", "MED", 70),
            ("Castillo", "DEF", 69), ("López", "DEL", 71), ("Martínez", "MED", 70),
            ("Rodríguez", "DEF", 69), ("Corona", "DEL", 70)
        ])

        self._crear_equipo("sanluis", "Atl. San Luis", "Liga MX", [
            ("Barovero", "POR", 73), ("Guzmán", "DEF", 70), ("Torres", "DEF", 69),
            ("Sabbag", "DEL", 71), ("Bilbao", "MED", 70), ("Sanabria", "MED", 69),
            ("Hernández", "DEF", 68), ("Murillo", "DEL", 70), ("García", "MED", 69),
            ("Álvarez", "DEF", 68), ("Zaldivar", "DEL", 69)
        ])

        self._crear_equipo("juarez", "Juárez", "Liga MX", [
            ("Vázquez", "POR", 72), ("Olivera", "DEF", 69), ("Molina", "DEF", 68),
            ("García", "DEL", 70), ("Rodríguez", "MED", 69), ("Fernández", "MED", 68),
            ("Gómez", "DEF", 67), ("Martínez", "DEL", 69), ("López", "MED", 68),
            ("Hernández", "DEF", 67), ("Castro", "DEL", 68)
        ])

        self._crear_equipo("queretaro", "Querétaro", "Liga MX", [
            ("Alcalá", "POR", 71), ("Gularte", "DEF", 68), ("Novoa", "DEF", 67),
            ("Cortizo", "MED", 69), ("Sepúlveda", "DEL", 69), ("Martínez", "MED", 68),
            ("Pool", "DEF", 66), ("Gómez", "DEL", 68), ("Zamudio", "MED", 67),
            ("Pérez", "DEF", 66), ("López", "DEL", 67)
        ])

        self._crear_equipo("mazatlan", "Mazatlán", "Liga MX", [
            ("Gutiérrez", "POR", 70), ("Villegas", "DEF", 67), ("Célis", "DEF", 66),
            ("Correa", "DEL", 68), ("Medina", "MED", 67), ("Rivas", "MED", 66),
            ("Ortiz", "DEF", 65), ("Colmán", "DEL", 67), ("Meraz", "MED", 66),
            ("Moreno", "DEF", 65), ("Fernández", "DEL", 66)
        ])

        self._crear_equipo("necaxa", "Necaxa", "Liga MX", [
            ("Aragon", "POR", 71), ("Formiliano", "DEF", 68), ("Peña", "DEF", 67),
            ("Furch", "DEL", 69), ("Battocchio", "MED", 68), ("Gómez", "MED", 67),
            ("Mayorga", "DEF", 66), ("Silvera", "DEL", 68), ("Esquivel", "MED", 67),
            ("Ortiz", "DEF", 66), ("García", "DEL", 67)
        ])

        self._crear_equipo("puebla", "Puebla", "Liga MX", [
            ("Silva", "POR", 72), ("Gonzalez", "DEF", 69), ("Reyes", "DEF", 68),
            ("Parra", "DEL", 70), ("Martínez", "MED", 69), ("Guzmán", "MED", 68),
            ("Velázquez", "DEF", 67), ("Tabó", "DEL", 69), ("Ormeño", "MED", 68),
            ("García", "DEF", 67), ("Álvarez", "DEL", 68)
        ])

        self._crear_equipo("santos", "Santos Laguna", "Liga MX", [
            ("Acevedo", "POR", 75), ("Dória", "DEF", 72), ("Rodríguez", "DEF", 71),
            ("Corona", "MED", 73), ("Precido", "DEL", 72), ("Gómez", "MED", 71),
            ("Cervantes", "DEF", 70), ("Brunetta", "DEL", 72), ("Gonzalez", "MED", 71),
            ("Torres", "DEF", 70), ("Jabá", "DEL", 71)
        ])

        self._crear_equipo("atlas", "Atlas", "Liga MX", [
            ("Hernández", "POR", 74), ("Nervo", "DEF", 71), ("Rocha", "DEF", 70),
            ("Quiñones", "DEL", 72), ("Reyes", "MED", 71), ("Marchesín", "MED", 70),
            ("Abella", "DEF", 69), ("Zaldivar", "DEL", 71), ("Lozano", "MED", 70),
            ("Trejo", "DEF", 69), ("Aguirre", "DEL", 70)
        ])

        self._crear_equipo("mty", "Atlético MTY", "Liga MX", [
            ("García", "POR", 73), ("Madueña", "DEF", 70), ("Guzmán", "DEF", 69),
            ("Mejía", "DEL", 71), ("Kranevitter", "MED", 70), ("Gómez", "MED", 69),
            ("Angulo", "DEF", 68), ("Hurtado", "DEL", 70), ("Pineda", "MED", 69),
            ("Reyes", "DEF", 68), ("Fernández", "DEL", 69)
        ])

        # === LIGA DIMAYOR (COLOMBIA) - 20 equipos ===
        self._crear_equipo("nacional", "Atlético Nacional", "Liga Dimayor", [
            ("Quintana", "POR", 76), ("Devenish", "DEF", 73), ("Banguero", "DEF", 72),
            ("Pabón", "DEL", 75), ("Duque", "DEL", 74), ("Andrade", "MED", 73),
            ("Palacio", "MED", 72), ("Perez", "DEF", 71), ("Candelo", "MED", 72),
            ("Blandón", "DEL", 71), ("Gómez", "DEF", 71)
        ])

        self._crear_equipo("millonarios", "Millonarios", "Liga Dimayor", [
            ("Novoa", "POR", 75), ("Bertel", "DEF", 72), ("Vanegas", "DEF", 73),
            ("Cataño", "MED", 74), ("Silva", "DEL", 74), ("Vargas", "MED", 72),
            ("Pereira", "DEF", 71), ("Ruiz", "DEL", 72), ("Gómez", "MED", 71),
            ("Mackalister", "MED", 72), ("Luna", "DEF", 70)
        ])

        self._crear_equipo("america_cal", "América de Cali", "Liga Dimayor", [
            ("Mosquera", "POR", 74), ("Quiñones", "DEF", 72), ("Ramos", "DEF", 71),
            ("Sierra", "MED", 73), ("Ramos", "DEL", 73), ("Barrera", "MED", 72),
            ("Suárez", "DEF", 70), ("Waterman", "DEL", 71), ("Carbonero", "MED", 71),
            ("García", "DEF", 70), ("Mosquera", "MED", 70)
        ])

        self._crear_equipo("santafe", "Santa Fe", "Liga Dimayor", [
            ("Castillo", "POR", 73), ("Rivas", "DEF", 71), ("Torralvo", "DEF", 70),
            ("Rodallega", "DEL", 74), ("Moreno", "MED", 72), ("Batalla", "MED", 71),
            ("Mina", "DEF", 70), ("Marulanda", "DEL", 71), ("Vega", "MED", 70),
            ("Rangel", "DEF", 69), ("Gutiérrez", "MED", 69)
        ])

        self._crear_equipo("junior", "Junior", "Liga Dimayor", [
            ("Cuesta", "POR", 74), ("Hernández", "DEF", 71), ("Gutiérrez", "DEF", 70),
            ("Borre", "DEL", 73), ("Cantillo", "MED", 72), ("Vaccari", "MED", 71),
            ("Pérez", "DEF", 69), ("Pico", "DEL", 71), ("Moreno", "MED", 70),
            ("Rosero", "DEF", 69), ("Hinestroza", "DEL", 70)
        ])

        self._crear_equipo("cali", "Deportivo Cali", "Liga Dimayor", [
            ("Herrera", "POR", 73), ("Angulo", "DEF", 70), ("Castillo", "DEF", 69),
            ("Gutiérrez", "DEL", 72), ("Vásquez", "MED", 71), ("Palavecino", "MED", 70),
            ("Roa", "DEF", 68), ("Rodríguez", "DEL", 70), ("Cabrera", "MED", 69),
            ("Mera", "DEF", 68), ("Arango", "DEL", 69)
        ])

        self._crear_equipo("medellin", "Independiente Medellín", "Liga Dimayor", [
            ("Mosquera", "POR", 72), ("Torres", "DEF", 70), ("Cadavid", "DEF", 69),
            ("Pons", "DEL", 71), ("Palacios", "MED", 70), ("Castro", "MED", 69),
            ("Hernández", "DEF", 68), ("Moreno", "DEL", 70), ("Pérez", "MED", 69),
            ("Moya", "DEF", 68), ("Bustos", "DEL", 69)
        ])

        self._crear_equipo("pasto", "Deportivo Pasto", "Liga Dimayor", [
            ("Martínez", "POR", 71), ("Ramos", "DEF", 69), ("Mina", "DEF", 68),
            ("Palacios", "DEL", 70), ("Rivas", "MED", 69), ("Ayala", "MED", 68),
            ("Gómez", "DEF", 67), ("Hurtado", "DEL", 69), ("Rodríguez", "MED", 68),
            ("Pérez", "DEF", 67), ("Mosquera", "DEL", 68)
        ])

        self._crear_equipo("bucaramanga", "Atl. Bucaramanga", "Liga Dimayor", [
            ("Chaverra", "POR", 70), ("Cárdenas", "DEF", 68), ("Márquez", "DEF", 67),
            ("Rangel", "DEL", 69), ("Balanta", "MED", 68), ("Rojas", "MED", 67),
            ("Hernández", "DEF", 66), ("Pérez", "DEL", 68), ("Gómez", "MED", 67),
            ("Torres", "DEF", 66), ("Rodríguez", "DEL", 67)
        ])

        self._crear_equipo("envigado", "Envigado", "Liga Dimayor", [
            ("García", "POR", 69), ("Mosquera", "DEF", 67), ("Hincapié", "DEF", 66),
            ("Arango", "DEL", 68), ("Moreno", "MED", 67), ("Restrepo", "MED", 66),
            ("Córdoba", "DEF", 65), ("Palacios", "DEL", 67), ("Gómez", "MED", 66),
            ("Álvarez", "DEF", 65), ("Hoyos", "DEL", 66)
        ])

        self._crear_equipo("aguilas", "Águilas Doradas", "Liga Dimayor", [
            ("Castillo", "POR", 70), ("Rentería", "DEF", 68), ("Cano", "DEF", 67),
            ("Rivas", "DEL", 69), ("Mosquera", "MED", 68), ("Gómez", "MED", 67),
            ("Torres", "DEF", 66), ("Pérez", "DEL", 68), ("Hernández", "MED", 67),
            ("Gutiérrez", "DEF", 66), ("Rodríguez", "DEL", 67)
        ])

        self._crear_equipo("oncecaldas", "Once Caldas", "Liga Dimayor", [
            ("Hernández", "POR", 71), ("Correa", "DEF", 69), ("Mosquera", "DEF", 68),
            ("García", "DEL", 70), ("Londoño", "MED", 69), ("Pérez", "MED", 68),
            ("Ramírez", "DEF", 67), ("Rodríguez", "DEL", 69), ("Gómez", "MED", 68),
            ("Álvarez", "DEF", 67), ("Henao", "DEL", 68)
        ])

        self._crear_equipo("patriotas", "Patriotas", "Liga Dimayor", [
            ("López", "POR", 68), ("Rojas", "DEF", 66), ("Gómez", "DEF", 65),
            ("Pérez", "DEL", 67), ("Hernández", "MED", 66), ("Martínez", "MED", 65),
            ("Díaz", "DEF", 64), ("Gutiérrez", "DEL", 66), ("Rodríguez", "MED", 65),
            ("Moreno", "DEF", 64), ("López", "DEL", 65)
        ])

        self._crear_equipo("aliansa", "Aliansa Petrolera", "Liga Dimayor", [
            ("Gómez", "POR", 69), ("Pérez", "DEF", 67), ("Rodríguez", "DEF", 66),
            ("Gutiérrez", "DEL", 68), ("Hernández", "MED", 67), ("Martínez", "MED", 66),
            ("Díaz", "DEF", 65), ("López", "DEL", 67), ("Gómez", "MED", 66),
            ("Moreno", "DEF", 65), ("Pérez", "DEL", 66)
        ])

        self._crear_equipo("boyaca", "Boyacá Chicó", "Liga Dimayor", [
            ("Rodríguez", "POR", 68), ("Gómez", "DEF", 66), ("Hernández", "DEF", 65),
            ("Pérez", "DEL", 67), ("Martínez", "MED", 66), ("López", "MED", 65),
            ("Díaz", "DEF", 64), ("Gutiérrez", "DEL", 66), ("Rodríguez", "MED", 65),
            ("Moreno", "DEF", 64), ("Pérez", "DEL", 65)
        ])

        self._crear_equipo("cucuta", "Cúcuta Deportivo", "Liga Dimayor", [
            ("Hernández", "POR", 69), ("Pérez", "DEF", 67), ("Gómez", "DEF", 66),
            ("Rodríguez", "DEL", 68), ("Martínez", "MED", 67), ("López", "MED", 66),
            ("Díaz", "DEF", 65), ("Gutiérrez", "DEL", 67), ("Hernández", "MED", 66),
            ("Moreno", "DEF", 65), ("Pérez", "DEL", 66)
        ])

        self._crear_equipo("tigres_fc", "Tigres FC", "Liga Dimayor", [
            ("Gómez", "POR", 67), ("Rodríguez", "DEF", 65), ("Hernández", "DEF", 64),
            ("Pérez", "DEL", 66), ("Martínez", "MED", 65), ("López", "MED", 64),
            ("Díaz", "DEF", 63), ("Gutiérrez", "DEL", 65), ("Rodríguez", "MED", 64),
            ("Moreno", "DEF", 63), ("Pérez", "DEL", 64)
        ])

        self._crear_equipo("union_mag", "Unión Magdalena", "Liga Dimayor", [
            ("Pérez", "POR", 68), ("Gómez", "DEF", 66), ("Rodríguez", "DEF", 65),
            ("Hernández", "DEL", 67), ("Martínez", "MED", 66), ("López", "MED", 65),
            ("Díaz", "DEF", 64), ("Gutiérrez", "DEL", 66), ("Pérez", "MED", 65),
            ("Moreno", "DEF", 64), ("Rodríguez", "DEL", 65)
        ])

        self._crear_equipo("cortulua", "Cortuluá", "Liga Dimayor", [
            ("Rodríguez", "POR", 67), ("Hernández", "DEF", 65), ("Pérez", "DEF", 64),
            ("Gómez", "DEL", 66), ("Martínez", "MED", 65), ("López", "MED", 64),
            ("Díaz", "DEF", 63), ("Gutiérrez", "DEL", 65), ("Rodríguez", "MED", 64),
            ("Moreno", "DEF", 63), ("Pérez", "DEL", 64)
        ])

        # === LIGA ECUATORIANA - 20 equipos ===
        self._crear_equipo("ldu", "LDU Quito", "Liga Ecuatoriana", [
            ("Galíndez", "POR", 75), ("Rodríguez", "DEF", 72), ("Quiñónez", "DEF", 71),
            ("Alzugaray", "DEL", 74), ("Martínez", "MED", 73), ("Piovi", "MED", 72),
            ("Hurtado", "DEF", 70), ("Zambrano", "DEL", 72), ("Gómez", "MED", 71),
            ("Cangá", "DEF", 70), ("Rojas", "DEL", 71)
        ])

        self._crear_equipo("barcelona", "Barcelona SC", "Liga Ecuatoriana", [
            ("Burrai", "POR", 76), ("Esterilla", "DEF", 73), ("Ayr", "DEF", 72),
            ("Fydriszewski", "DEL", 75), ("Cifuente", "MED", 74), ("Gaibor", "MED", 73),
            ("Arboleda", "DEF", 71), ("Díaz", "DEL", 73), ("Méndez", "MED", 72),
            ("Velasco", "DEF", 71), ("Rodríguez", "DEL", 72)
        ])

        self._crear_equipo("emelec", "Emelec", "Liga Ecuatoriana", [
            ("Ortiz", "POR", 74), ("Caicedo", "DEF", 71), ("Cangá", "DEF", 70),
            ("Cabeza", "DEL", 73), ("Cortez", "MED", 72), ("Quiñónez", "MED", 71),
            ("López", "DEF", 69), ("Barcos", "DEL", 72), ("Gómez", "MED", 71),
            ("Mina", "DEF", 69), ("Rojas", "DEL", 71)
        ])

        self._crear_equipo("indvalle", "Independiente Valle", "Liga Ecuatoriana", [
            ("Ramírez", "POR", 73), ("Pineida", "DEF", 70), ("García", "DEF", 69),
            ("Schunke", "DEL", 72), ("Faravelli", "MED", 71), ("Rojas", "MED", 70),
            ("Quiñónez", "DEF", 68), ("Rodríguez", "DEL", 71), ("Cifuente", "MED", 70),
            ("Mina", "DEF", 68), ("Hoyos", "DEL", 70)
        ])

        self._crear_equipo("aucas", "Aucas", "Liga Ecuatoriana", [
            ("Aycart", "POR", 72), ("Cantera", "DEF", 69), ("Nazareno", "DEF", 68),
            ("Rivas", "DEL", 71), ("Luna", "MED", 70), ("Quiñónez", "MED", 69),
            ("Gómez", "DEF", 67), ("Borja", "DEL", 70), ("Martínez", "MED", 69),
            ("Rodríguez", "DEF", 67), ("Cabeza", "DEL", 69)
        ])

        self._crear_equipo("univcatolica", "Universidad Católica", "Liga Ecuatoriana", [
            ("Zambrano", "POR", 71), ("Gómez", "DEF", 68), ("Rodríguez", "DEF", 67),
            ("Cazares", "DEL", 70), ("Martínez", "MED", 69), ("López", "MED", 68),
            ("Hernández", "DEF", 66), ("Pérez", "DEL", 69), ("Gómez", "MED", 68),
            ("Díaz", "DEF", 66), ("Rodríguez", "DEL", 68)
        ])

        self._crear_equipo("delfin", "Delfín", "Liga Ecuatoriana", [
            ("Erbez", "POR", 70), ("Kanner", "DEF", 67), ("Corozo", "DEF", 66),
            ("Garces", "DEL", 69), ("Montes", "MED", 68), ("Rojas", "MED", 67),
            ("Gómez", "DEF", 65), ("Mera", "DEL", 68), ("Martínez", "MED", 67),
            ("Rodríguez", "DEF", 65), ("Pérez", "DEL", 67)
        ])

        self._crear_equipo("tecuniv", "Técnico Universitario", "Liga Ecuatoriana", [
            ("Cuesta", "POR", 69), ("Gómez", "DEF", 66), ("Rodríguez", "DEF", 65),
            ("Pérez", "DEL", 68), ("Martínez", "MED", 67), ("López", "MED", 66),
            ("Hernández", "DEF", 64), ("Gutiérrez", "DEL", 67), ("Rodríguez", "MED", 66),
            ("Díaz", "DEF", 64), ("Pérez", "DEL", 66)
        ])

        self._crear_equipo("cuenca", "Deportivo Cuenca", "Liga Ecuatoriana", [
            ("Mora", "POR", 68), ("Pérez", "DEF", 65), ("Gómez", "DEF", 64),
            ("Rodríguez", "DEL", 67), ("Martínez", "MED", 66), ("López", "MED", 65),
            ("Hernández", "DEF", 63), ("Gutiérrez", "DEL", 66), ("Rodríguez", "MED", 65),
            ("Díaz", "DEF", 63), ("Pérez", "DEL", 65)
        ])

        self._crear_equipo("guayaquilcity", "Guayaquil City", "Liga Ecuatoriana", [
            ("Cevallos", "POR", 67), ("Gómez", "DEF", 64), ("Rodríguez", "DEF", 63),
            ("Pérez", "DEL", 66), ("Martínez", "MED", 65), ("López", "MED", 64),
            ("Hernández", "DEF", 62), ("Gutiérrez", "DEL", 65), ("Rodríguez", "MED", 64),
            ("Díaz", "DEF", 62), ("Pérez", "DEL", 64)
        ])

        self._crear_equipo("olmedo", "Olmedo", "Liga Ecuatoriana", [
            ("Rodríguez", "POR", 66), ("Hernández", "DEF", 63), ("Pérez", "DEF", 62),
            ("Gómez", "DEL", 65), ("Martínez", "MED", 64), ("López", "MED", 63),
            ("Díaz", "DEF", 61), ("Gutiérrez", "DEL", 64), ("Rodríguez", "MED", 63),
            ("Moreno", "DEF", 61), ("Pérez", "DEL", 63)
        ])

        self._crear_equipo("mushucruna", "Mushuc Runa", "Liga Ecuatoriana", [
            ("Pérez", "POR", 67), ("Gómez", "DEF", 64), ("Rodríguez", "DEF", 63),
            ("Hernández", "DEL", 66), ("Martínez", "MED", 65), ("López", "MED", 64),
            ("Díaz", "DEF", 62), ("Gutiérrez", "DEL", 65), ("Pérez", "MED", 64),
            ("Moreno", "DEF", 62), ("Rodríguez", "DEL", 64)
        ])

        self._crear_equipo("gualaceo", "Gualaceo", "Liga Ecuatoriana", [
            ("Rodríguez", "POR", 65), ("Hernández", "DEF", 62), ("Pérez", "DEF", 61),
            ("Gómez", "DEL", 64), ("Martínez", "MED", 63), ("López", "MED", 62),
            ("Díaz", "DEF", 60), ("Gutiérrez", "DEL", 63), ("Rodríguez", "MED", 62),
            ("Moreno", "DEF", 60), ("Pérez", "DEL", 62)
        ])

        self._crear_equipo("libertad", "Libertad", "Liga Ecuatoriana", [
            ("Gómez", "POR", 66), ("Rodríguez", "DEF", 63), ("Hernández", "DEF", 62),
            ("Pérez", "DEL", 65), ("Martínez", "MED", 64), ("López", "MED", 63),
            ("Díaz", "DEF", 61), ("Gutiérrez", "DEL", 64), ("Rodríguez", "MED", 63),
            ("Moreno", "DEF", 61), ("Pérez", "DEL", 63)
        ])

        self._crear_equipo("cumbaya", "Cumbayá", "Liga Ecuatoriana", [
            ("Hernández", "POR", 64), ("Pérez", "DEF", 61), ("Gómez", "DEF", 60),
            ("Rodríguez", "DEL", 63), ("Martínez", "MED", 62), ("López", "MED", 61),
            ("Díaz", "DEF", 59), ("Gutiérrez", "DEL", 62), ("Rodríguez", "MED", 61),
            ("Moreno", "DEF", 59), ("Pérez", "DEL", 61)
        ])

        self._crear_equipo("macara", "Macará", "Liga Ecuatoriana", [
            ("Pérez", "POR", 65), ("Gómez", "DEF", 62), ("Rodríguez", "DEF", 61),
            ("Hernández", "DEL", 64), ("Martínez", "MED", 63), ("López", "MED", 62),
            ("Díaz", "DEF", 60), ("Gutiérrez", "DEL", 63), ("Pérez", "MED", 62),
            ("Moreno", "DEF", 60), ("Rodríguez", "DEL", 62)
        ])

        self._crear_equipo("el_nacional", "El Nacional", "Liga Ecuatoriana", [
            ("Rodríguez", "POR", 63), ("Hernández", "DEF", 60), ("Pérez", "DEF", 59),
            ("Gómez", "DEL", 62), ("Martínez", "MED", 61), ("López", "MED", 60),
            ("Díaz", "DEF", 58), ("Gutiérrez", "DEL", 61), ("Rodríguez", "MED", 60),
            ("Moreno", "DEF", 58), ("Pérez", "DEL", 60)
        ])

        self._crear_equipo("indjunior", "Independiente Juniors", "Liga Ecuatoriana", [
            ("Gómez", "POR", 64), ("Rodríguez", "DEF", 61), ("Hernández", "DEF", 60),
            ("Pérez", "DEL", 63), ("Martínez", "MED", 62), ("López", "MED", 61),
            ("Díaz", "DEF", 59), ("Gutiérrez", "DEL", 62), ("Rodríguez", "MED", 61),
            ("Moreno", "DEF", 59), ("Pérez", "DEL", 61)
        ])

        self._crear_equipo("9octubre", "9 de Octubre", "Liga Ecuatoriana", [
            ("Hernández", "POR", 62), ("Pérez", "DEF", 59), ("Gómez", "DEF", 58),
            ("Rodríguez", "DEL", 61), ("Martínez", "MED", 60), ("López", "MED", 59),
            ("Díaz", "DEF", 57), ("Gutiérrez", "DEL", 60), ("Rodríguez", "MED", 59),
            ("Moreno", "DEF", 57), ("Pérez", "DEL", 59)
        ])
        self._crear_equipo("flamengo", "Flamengo", "Liga Brasileña", [
            ("Rossi","POR",75), ("Filipe_Luis","DEF",74), ("Fabrício_Bruno","DEF",73),
            ("David_Luiz","DEF",72), ("Ayrton_Lucas","DEF",73), ("Gerson","MED",75),
            ("Arrascaeta","MED",77), ("Éverton_Ribeiro","MED",75), ("Pulgar","MED",73),
            ("Bruno_Henrique","DEL",76), ("Pedro","DEL",77)
        ])

        self._crear_equipo("palmeiras", "Palmeiras", "Liga Brasileña", [
            ("Weverton","POR",76), ("Murilo","DEF",73), ("Gómez","DEF",75),
            ("Mayke","DEF",72), ("Piquerez","DEF",73), ("Zé_Rafael","MED",74),
            ("Veiga","MED",76), ("Menino","MED",72), ("Endrick","DEL",75),
            ("Rony","DEL",74), ("Dudu","DEL",76)
        ])

        self._crear_equipo("fluminense", "Fluminense", "Liga Brasileña", [
            ("Fábio","POR",74), ("Samuel_Xavier","DEF",72), ("Felipe_Melo","DEF",70),
            ("Nino","DEF",73), ("Marcelo","DEF",74), ("André","MED",75),
            ("Ganso","MED",73), ("Keno","DEL",74), ("Arias","DEL",75),
            ("Cano","DEL",77), ("John_Kennedy","DEL",72)
        ])

        self._crear_equipo("gremio", "Grêmio", "Liga Brasileña", [
            ("Marchesín","POR",73), ("Kannemann","DEF",72), ("Reinaldo","DEF",71),
            ("Rodrigo_Ely","DEF",70), ("João_Pedro","DEF",69), ("Carballo","MED",73),
            ("Pepê","MED",72), ("Cristaldo","MED",74), ("Franco_Cristaldo","MED",73),
            ("Suárez","DEL",76), ("Ferreira","DEL",72)
        ])

        self._crear_equipo("internacional", "Internacional", "Liga Brasileña", [
            ("Rochet","POR",75), ("Vitão","DEF",72), ("Mercado","DEF",70),
            ("René","DEF",71), ("Bustos","DEF",71), ("Aránguiz","MED",74),
            ("Mauricio","MED",73), ("Alan_Patrick","MED",74), ("Bruno_Henrique","MED",72),
            ("Enner_Valencia","DEL",75), ("Pedro_Henrique","DEL",73)
        ])

        self._crear_equipo("atletico_mg", "Atlético Mineiro", "Liga Brasileña", [
            ("Everson","POR",74), ("Guilherme_Arana","DEF",73), ("Gemerson","DEF",72),
            ("Rever","DEF",70), ("Mariano","DEF",70), ("Otávio","MED",72),
            ("Hulk","DEL",77), ("Paulinho","DEL",74), ("Edenílson","MED",74),
            ("Pedrinho","MED",72), ("Zaracho","MED",74)
        ])

        self._crear_equipo("botafogo", "Botafogo", "Liga Brasileña", [
            ("Perri","POR",73), ("Adryelson","DEF",72), ("Bastos","DEF",70),
            ("Marçal","DEF",71), ("Di_Plácido","DEF",70), ("Tchê_Tchê","MED",72),
            ("Marlon_Freitas","MED",72), ("Eduardo","MED",74), ("Júnior_Santos","DEL",73),
            ("Tiquinho_Soares","DEL",76), ("Luís_Henrique","DEL",72)
        ])

        self._crear_equipo("santos", "Santos", "Liga Brasileña", [
            ("João_Paulo","POR",73), ("Joaquim","DEF",69), ("Messias","DEF",70),
            ("Dodô","DEF",70), ("Lucas_Pires","DEF",68), ("Jean_Lucas","MED",71),
            ("Lucas_Lima","MED",70), ("Soteldo","DEL",74), ("Marcos_Leonardo","DEL",75),
            ("Mendonça","DEL",71), ("Rincon","MED",70)
        ])

        self._crear_equipo("saopaulo", "São Paulo", "Liga Brasileña", [
            ("Rafael","POR",73), ("Rafinha","DEF",70), ("Arboleda","DEF",73),
            ("Beraldo","DEF",71), ("Caio_Paulista","DEF",70), ("Luciano","DEL",75),
            ("Calleri","DEL",76), ("Wellington_Rato","MED",71), ("Alisson","MED",70),
            ("Galoppo","MED",72), ("Michel_Araujo","MED",70)
        ])

        self._crear_equipo("corinthians", "Corinthians", "Liga Brasileña", [
            ("Cássio","POR",74), ("Fagner","DEF",72), ("Murillo","DEF",71),
            ("Gil","DEF",70), ("Bidon","MED",70), ("Maycon","MED",72),
            ("Giuliano","MED",72), ("Renato_Augusto","MED",73), ("Mosquito","DEL",71),
            ("Yuri_Alberto","DEL",75), ("Romero","DEL",72)
        ])

        self._crear_equipo("bahia", "Bahia", "Liga Brasileña", [
            ("Marcos_Felipe","POR",70), ("Kanu","DEF",69), ("Vitor_Hugo","DEF",70),
            ("Rezende","MED",69), ("Cauly","MED",71), ("Biel","DEL",71),
            ("Everton_Ribeiro","MED",70), ("Acevedo","MED",70), ("Thaciano","MED",69),
            ("Ademir","DEL",70), ("Everaldo","DEL",71)
        ])

        self._crear_equipo("athletico", "Athletico Paranaense", "Liga Brasileña", [
            ("Bento","POR",74), ("Khellven","DEF",71), ("Thiago_Andrade","DEF",70),
            ("Cacá","DEF",70), ("Cuello","MED",71), ("Erick","MED",72),
            ("Fernandinho","MED",74), ("Christian","MED",71), ("Canobbio","DEL",73),
            ("Vitor_Roque","DEL",75), ("Pablo","DEL",72)
        ])

        self._crear_equipo("bragantino", "Red Bull Bragantino", "Liga Brasileña", [
            ("Cleiton","POR",72), ("Aderlan","DEF",70), ("Luan_Cândido","DEF",70),
            ("Léo_Ortiz","DEF",71), ("Lucas_Evangelista","MED",72), ("Eric_Ramires","MED",70),
            ("Sasha","DEL",72), ("Helinho","DEL",71), ("Thiago_Borbas","DEL",72),
            ("Vitinho","MED",70), ("Lincoln","MED",69)
        ])

        self._crear_equipo("fortaleza", "Fortaleza", "Liga Brasileña", [
            ("Boeck","POR",70), ("Benevenuto","DEF",70), ("Titi","DEF",70),
            ("Pacheco","DEF",69), ("Tinga","DEF",69), ("Lucas_Sasha","MED",71),
            ("Pochettino","MED",72), ("Calebe","MED",70), ("Marinho","DEL",73),
            ("Lucero","DEL",73), ("Yago_Pikachu","DEL",71)
        ])

        self._crear_equipo("cuiaba", "Cuiabá", "Liga Brasileña", [
            ("Walter","POR",69), ("Alan_Empereur","DEF",69), ("Uendel","DEF",68),
            ("F.Santos","DEF",68), ("Clayson","DEL",70), ("Denilson","MED",69),
            ("Ramiro","MED",70), ("Ceppelini","MED",69), ("Deyverson","DEL",72),
            ("Jonathan_Cafu","DEL",70), ("Rikelme","DEF",67)
        ])

        self._crear_equipo("goias", "Goiás", "Liga Brasileña", [
            ("Tadeu","POR",71), ("Yan_Souto","DEF",68), ("Sidimar","DEF",68),
            ("Sander","DEF",69), ("Hugo","DEF",68), ("Matheus_Bidu","MED",68),
            ("Guilherme","MED",69), ("Vinicius","DEL",71), ("Morelli","MED",69),
            ("Palacios","DEL",70), ("Allano","DEL",70)
        ])

        self._crear_equipo("coritiba", "Coritiba", "Liga Brasileña", [
            ("Gabriel","POR",69), ("Natanael","DEF",68), ("Henrique","DEF",68),
            ("Jamerson","DEF",67), ("Boschilia","MED",69), ("Robson","DEL",71),
            ("Bruno_Gomes","MED",69), ("Slimani","DEL",70), ("Andrey","MED",69),
            ("Pablo_Thomaz","DEL",69), ("Zé_Roberto","DEL",68)
        ])

        self._crear_equipo("america_mg", "América Mineiro", "Liga Brasileña", [
            ("Matheus_Cavichioli","POR",69), ("Maidana","DEF",69), ("Marlon","DEF",68),
            ("Juninho","MED",70), ("Aloisio","DEL",70), ("Mastriani","DEL",71),
            ("Adyson","DEL",69), ("Felipe_Azevedo","DEL",69), ("Emerson","DEF",68),
            ("Lucas_Kal","DEF",68), ("Paulinho_Boas","MED",68)
        ])

        self._crear_equipo("vasco", "Vasco da Gama", "Liga Brasileña", [
            ("Léo_Jardim","POR",71), ("Medel","DEF",70), ("Léo_Pereira","DEF",70),
            ("Pitón","DEF",70), ("Pumita_Rodríguez","DEF",69), ("Praxedes","MED",70),
            ("Payet","MED",74), ("Zé_Gabriel","MED",70), ("Gabriel_Peck","MED",69),
            ("Pumita_Rodríguez","DEF",70), ("Vegetti","DEL",74)
        ])

        self._crear_equipo("cruzeiro", "Cruzeiro", "Liga Brasileña", [
            ("Rafael_Cabral","POR",71), ("Neris","DEF",69), ("Castán","DEF",69),
            ("William","DEF",69), ("Marlon","DEF",68), ("Wallisson","MED",70),
            ("Ramiro","MED",70), ("Bruno_Rodrigues","DEL",72), ("Matheus_Pereira","MED",71),
            ("Arthur_Gomes","DEL",71), ("Gilberto","DEL",72)
        ])

        self._crear_equipo("river", "River Plate", "Liga Argentina", [
            ("Armani","POR",75), ("P.Díaz","DEF",73), ("E.Díaz","DEF",70),
            ("Casco","DEF",71), ("L.G.Pirez","DEF",69), ("E.Pérez","MED",74),
            ("Aliendro","MED",72), ("I.Fernández","MED",73), ("Echeverri","MED",70),
            ("Barco","DEL",74), ("Borja","DEL",75)
        ])

        self._crear_equipo("boca", "Boca Juniors", "Liga Argentina", [
            ("Romero","POR",73), ("Advíncula","DEF",72), ("M.Rojo","DEF",73),
            ("Figal","DEF",70), ("F.Fabra","DEF",69), ("G.Fernández","MED",72),
            ("E.Fernández","MED",70), ("K.Zenón","MED",71), ("C.Medina","MED",70),
            ("Cavani","DEL",74), ("Langoni","DEL",70)
        ])

        self._crear_equipo("racing", "Racing Club", "Liga Argentina", [
            ("Arias","POR",73), ("Martirena","DEF",69), ("Piovi","DEF",70),
            ("Insúa","DEF",68), ("Sigali","DEF",71), ("Nardoni","MED",70),
            ("A.Moreno","MED",72), ("J.Gómez","MED",69), ("Almendra","MED",70),
            ("R.Martínez","DEL",72), ("Hauche","DEL",70)
        ])

        self._crear_equipo("sanlor", "San Lorenzo", "Liga Argentina", [
            ("Gómez","POR",70), ("Hernández","DEF",69), ("Giay","DEF",69),
            ("Gattoni","DEF",70), ("Luján","DEF",68), ("Maroni","MED",68),
            ("Barrios","MED",70), ("Leguizamón","MED",69), ("Martegani","MED",70),
            ("Bareiro","DEL",73), ("Vombergar","DEL",71)
        ])

        self._crear_equipo("indep", "Independiente", "Liga Argentina", [
            ("Rey","POR",70), ("Pérez","DEF",68), ("Báez","DEF",69),
            ("Costa","DEF",68), ("Quiroga","DEF",67), ("Marcone","MED",71),
            ("F.López","MED",70), ("Giménez","MED",69), ("S.López","MED",69),
            ("Canelo","DEL",70), ("Isla","DEL",68)
        ])

        self._crear_equipo("estud", "Estudiantes", "Liga Argentina", [
            ("Andújar","POR",71), ("Sosa","DEF",70), ("Godoy","DEF",68),
            ("Muñoz","DEF",68), ("Ascacíbar","MED",72), ("Zuqui","MED",70),
            ("J.Rodríguez","MED",71), ("Rollheiser","DEL",74), ("Benedetti","DEL",70),
            ("Carrillo","DEL",72), ("Mancuso","DEF",68)
        ])

        self._crear_equipo("talleres", "Talleres", "Liga Argentina", [
            ("Herrera","POR",70), ("L.Díaz","DEF",69), ("Portillo","DEF",68),
            ("Benavídez","DEF",69), ("R.Pérez","DEF",67), ("Villagra","MED",70),
            ("Garro","MED",71), ("Sosa","MED",69), ("Ortegoza","MED",68),
            ("Santos","DEL",73), ("Bustos","DEL",72)
        ])

        self._crear_equipo("velez", "Vélez Sarsfield", "Liga Argentina", [
            ("Burián","POR",70), ("Gómez","DEF",70), ("Giannetti","DEF",69),
            ("Ortega","DEF",68), ("Guidara","DEF",69), ("Cáseres","MED",70),
            ("Florentín","MED",69), ("G.Florentín","MED",69), ("Castro","MED",68),
            ("G.Fernández","DEL",72), ("Pratto","DEL",71)
        ])

        self._crear_equipo("defyjus", "Defensa y Justicia", "Liga Argentina", [
            ("Unsain","POR",71), ("Tripichio","DEF",69), ("Cardona","DEF",68),
            ("Soto","DEF",68), ("Frías","DEF",67), ("J.López","MED",70),
            ("K.Gutiérrez","MED",69), ("Alanís","MED",69), ("U.Fernández","MED",68),
            ("N.Fernández","DEL",71), ("Solari","DEL",70)
        ])

        self._crear_equipo("argentinos", "Argentinos Juniors", "Liga Argentina", [
            ("Lanzillota","POR",70), ("Torrén","DEF",70), ("Villalba","DEF",68),
            ("Costa","DEF",68), ("A.Rodríguez","DEF",67), ("Redondo","MED",72),
            ("A.Rodríguez","MED",69), ("Metilli","MED",69), ("Moyano","MED",68),
            ("Ávalos","DEL",72), ("Verón","DEL",70)
        ])

        self._crear_equipo("rosario", "Rosario Central", "Liga Argentina", [
            ("Broun","POR",70), ("Quintana","DEF",69), ("Mallo","DEF",68),
            ("D.Martínez","DEF",68), ("Giaccone","DEF",67), ("Ortiz","MED",70),
            ("Toledo","MED",68), ("Infantino","MED",70), ("O'Connor","MED",67),
            ("Véliz","DEL",73), ("Campaz","DEL",72)
        ])

        self._crear_equipo("colon", "Colón", "Liga Argentina", [
            ("Chicco","POR",70), ("Delgado","DEF",68), ("Garcés","DEF",69),
            ("Nardelli","DEF",68), ("Ábila","DEL",72), ("Pierotti","MED",70),
            ("Vega","MED",69), ("Álvarez","MED",69), ("Teuten","DEF",67),
            ("Benítez","DEL",70), ("Meza","MED",70)
        ])

        self._crear_equipo("union", "Unión", "Liga Argentina", [
            ("Moyano","POR",69), ("Calderón","DEF",69), ("Corvalán","DEF",68),
            ("Gerometta","DEF",67), ("Esquivel","DEL",70), ("Machuca","MED",70),
            ("Portillo","MED",68), ("T.González","MED",68), ("Luna Diale","MED",69),
            ("Zenón","MED",68), ("Juárez","DEL",70)
        ])

        self._crear_equipo("tigre", "Tigre", "Liga Argentina", [
            ("Marinelli","POR",69), ("Blondel","DEF",70), ("Demartini","DEF",68),
            ("Prieto","DEF",68), ("Luciatti","DEF",69), ("Castro","MED",71),
            ("Menossi","MED",70), ("Armoa","MED",69), ("Colidio","DEL",71),
            ("Retegui","DEL",74), ("Zabala","DEL",70)
        ])

        self._crear_equipo("banfield", "Banfield", "Liga Argentina", [
            ("Cambeses","POR",69), ("Coronel","DEF",69), ("Maciel","DEF",68),
            ("Insúa","DEF",68), ("Sosa","MED",69), ("J.Sosa","MED",68),
            ("M.González","MED",69), ("Dátolo","MED",68), ("Chávez","DEL",70),
            ("Cuadra","DEL",70), ("Urzi","DEL",70)
        ])

        self._crear_equipo("lanus", "Lanús", "Liga Argentina", [
            ("Acuña","POR",69), ("Aude","DEF",68), ("C.Pérez","DEF",68),
            ("López","DEF",69), ("Braghieri","DEF",68), ("Belmonte","MED",70),
            ("M.González","MED",69), ("Boggio","MED",68), ("De La Vega","DEL",74),
            ("L.Díaz","DEL",69), ("Sand","DEL",70)
        ])

        self._crear_equipo("huracan", "Huracán", "Liga Argentina", [
            ("Meza","POR",69), ("Gudiño","DEF",68), ("Tobio","DEF",69),
            ("Ibañez","DEF",68), ("Moya","DEF",67), ("Hezze","MED",70),
            ("Cristaldo","MED",72), ("Gauto","MED",69), ("Garre","DEL",71),
            ("Cóccaro","DEL",73), ("J.Gauto","DEL",70)
        ])

        self._crear_equipo("gimnasia", "Gimnasia LP", "Liga Argentina", [
            ("Durso","POR",69), ("Morales","DEF",68), ("Enrique","DEF",68),
            ("Ramírez","DEF",67), ("Colazo","DEF",68), ("Alemán","MED",70),
            ("Castro","MED",69), ("Soldano","DEL",70), ("Domínguez","MED",69),
            ("Mammini","DEL",69), ("Tarragona","DEL",70)
        ])

        self._crear_equipo("newells", "Newell’s", "Liga Argentina", [
            ("Hoyos","POR",69), ("C.Ditta","DEF",70), ("I.Glavinovich","DEF",68),
            ("Cacciabue","MED",69), ("Sforza","MED",70), ("Balzi","MED",69),
            ("Reasco","DEL",70), ("Portillo","MED",69), ("F.González","DEL",69),
            ("Aguirre","DEL",70), ("M.Pérez","DEF",67)
        ])

        self._crear_equipo("godoy", "Godoy Cruz", "Liga Argentina", [
            ("D.Rodríguez","POR",69), ("Barrios","DEF",68), ("Galdames","MED",70),
            ("Bullaude","MED",69), ("Chávez","MED",69), ("Badaloni","DEL",70),
            ("Salomón","DEF",68), ("Vega","MED",69), ("N.Fernández","DEL",71),
            ("Larrosa","DEL",70), ("Ojeda","DEL",69)
        ])



        # PREMIER LEAGUE - Completar todos a 11 jugadores
        self._crear_equipo("mc", "Manchester City", "Premier League", [
            ("Ederson", "POR", 88), ("Walker", "DEF", 85), ("Stones", "DEF", 86), 
            ("Dias", "DEF", 89), ("Gvardiol", "DEF", 82), ("Rodri", "MED", 91),
            ("De_Bruyne", "MED", 92), ("Bernardo", "MED", 88), ("Foden", "MED", 86),
            ("Haaland", "DEL", 94), ("Grealish", "DEL", 84)
        ])
        
        self._crear_equipo("liv", "Liverpool", "Premier League", [
            ("Alisson", "POR", 89), ("Alexander-Arnold", "DEF", 87), ("Van_Dijk", "DEF", 90),
            ("Konate", "DEF", 83), ("Robertson", "DEF", 85), ("Fabinho", "MED", 84),
            ("Henderson", "MED", 81), ("Thiago", "MED", 86), ("Salah", "DEL", 90),
            ("Nunez", "DEL", 82), ("Diaz", "DEL", 85)
        ])
        
        self._crear_equipo("ars", "Arsenal", "Premier League", [
            ("Raya", "POR", 82), ("White", "DEF", 83), ("Saliba", "DEF", 85),
            ("Gabriel", "DEF", 84), ("Zinchenko", "DEF", 81), ("Partey", "MED", 85),
            ("Odegaard", "MED", 87), ("Rice", "MED", 86), ("Saka", "DEL", 88),
            ("Jesus", "DEL", 84), ("Martinelli", "DEL", 83)
        ])
        
        self._crear_equipo("che", "Chelsea", "Premier League", [
            ("Sanchez", "POR", 80), ("James", "DEF", 84), ("Silva", "DEF", 85),
            ("Colwill", "DEF", 78), ("Chilwell", "DEF", 82), ("Caicedo", "MED", 82),
            ("Enzo", "MED", 85), ("Palmer", "MED", 84), ("Sterling", "DEL", 85),
            ("Jackson", "DEL", 79), ("Mudryk", "DEL", 80)
        ])
        
        self._crear_equipo("mu", "Manchester United", "Premier League", [
            ("Onana", "POR", 83), ("Dalot", "DEF", 79), ("Varane", "DEF", 83),
            ("Martinez", "DEF", 84), ("Shaw", "DEF", 82), ("Casemiro", "MED", 86),
            ("Bruno", "MED", 88), ("Mount", "MED", 82), ("Rashford", "DEL", 85),
            ("Hojlund", "DEL", 78), ("Garnacho", "DEL", 79)
        ])
        
        self._crear_equipo("tot", "Tottenham", "Premier League", [
            ("Vicario", "POR", 79), ("Porro", "DEF", 80), ("Romero", "DEF", 84),
            ("Van_de_Ven", "DEF", 81), ("Udogie", "DEF", 78), ("Bissouma", "MED", 80),
            ("Maddison", "MED", 84), ("Sarr", "MED", 76), ("Johnson", "DEL", 79),
            ("Son", "DEL", 86), ("Richarlison", "DEL", 81)
        ])
        
        # NEWCASTLE - Completar a 11 jugadores
        self._crear_equipo("new", "Newcastle", "Premier League", [
            ("Pope", "POR", 82), ("Trippier", "DEF", 83), ("Schar", "DEF", 80),
            ("Botman", "DEF", 79), ("Burn", "DEF", 76), ("Guimaraes", "MED", 84),
            ("Longstaff", "MED", 74), ("Joelinton", "MED", 78), ("Almiron", "DEL", 79),
            ("Wilson", "DEL", 78), ("Gordon", "DEL", 76)
        ])
        
        # ASTON VILLA - Completar a 11 jugadores
        self._crear_equipo("avl", "Aston Villa", "Premier League", [
            ("Martinez", "POR", 84), ("Cash", "DEF", 79), ("Konsa", "DEF", 78),
            ("Pau_Torres", "DEF", 81), ("Digne", "DEF", 80), ("McGinn", "MED", 79),
            ("Luiz", "MED", 82), ("Ramsey", "MED", 76), ("Bailey", "DEL", 77),
            ("Watkins", "DEL", 82), ("Diaby", "DEL", 80)
        ])
        
        # WEST HAM - Completar a 11 jugadores
        self._crear_equipo("wes", "West Ham", "Premier League", [
            ("Areola", "POR", 78), ("Coufal", "DEF", 76), ("Zouma", "DEF", 77),
            ("Aguerd", "DEF", 76), ("Emerson", "DEF", 75), ("Rice", "MED", 84),
            ("Soucek", "MED", 78), ("Paqueta", "MED", 81), ("Bowen", "DEL", 80),
            ("Antonio", "DEL", 76), ("Benrahma", "DEL", 78)
        ])
        
        # BRIGHTON - Completar a 11 jugadores
        self._crear_equipo("bha", "Brighton", "Premier League", [
            ("Steele", "POR", 74), ("Veltman", "DEF", 75), ("Dunk", "DEF", 77),
            ("Webster", "DEF", 74), ("Estupinan", "DEF", 78), ("Caicedo", "MED", 82),
            ("Mac_Allister", "MED", 81), ("Gross", "MED", 79), ("Mitoma", "DEL", 79),
            ("Ferguson", "DEL", 76), ("March", "DEL", 74)
        ])
        
        # WOLVES - Completar a 11 jugadores
        self._crear_equipo("wol", "Wolves", "Premier League", [
            ("Sa", "POR", 76), ("Semedo", "DEF", 76), ("Kilman", "DEF", 74),
            ("Dawson", "DEF", 73), ("Ait_Nouri", "DEF", 75), ("Neves", "MED", 80),
            ("Moutinho", "MED", 76), ("Neto", "MED", 77), ("Traore", "DEL", 76),
            ("Jimenez", "DEL", 78), ("Cunha", "DEL", 77)
        ])
        
        # CRYSTAL PALACE - Completar a 11 jugadores
        self._crear_equipo("cry", "Crystal Palace", "Premier League", [
            ("Guaita", "POR", 75), ("Ward", "DEF", 74), ("Andersen", "DEF", 77),
            ("Guehi", "DEF", 76), ("Mitchell", "DEF", 73), ("Gallagher", "MED", 78),
            ("Hughes", "MED", 74), ("Eze", "MED", 79), ("Zaha", "DEL", 80),
            ("Ayew", "DEL", 72), ("Mateta", "DEL", 75)
        ])
        
        # FULHAM - Completar a 11 jugadores
        self._crear_equipo("ful", "Fulham", "Premier League", [
            ("Leno", "POR", 78), ("Tete", "DEF", 74), ("Adarabioyo", "DEF", 75),
            ("Ream", "DEF", 73), ("Robinson", "DEF", 76), ("Palhinha", "MED", 81),
            ("Reed", "MED", 74), ("Pereira", "MED", 78), ("Willian", "DEL", 77),
            ("Mitrovic", "DEL", 80), ("Iwobi", "DEL", 76)
        ])
        
        # EVERTON - Completar a 11 jugadores
        self._crear_equipo("eve", "Everton", "Premier League", [
            ("Pickford", "POR", 81), ("Coleman", "DEF", 74), ("Tarkowski", "DEF", 76),
            ("Branthwaite", "DEF", 73), ("Mykolenko", "DEF", 72), ("Gueye", "MED", 76),
            ("Onana", "MED", 75), ("Doucoure", "MED", 74), ("Harrison", "DEL", 73),
            ("Calvert-Lewin", "DEL", 77), ("McNeil", "DEL", 74)
        ])
        
        # BURNLEY - Completar a 11 jugadores
        self._crear_equipo("bur", "Burnley", "Premier League", [
            ("Trafford", "POR", 70), ("Roberts", "DEF", 69), ("O_Shea", "DEF", 71),
            ("Esteve", "DEF", 70), ("Taylor", "DEF", 72), ("Cullen", "MED", 73),
            ("Berge", "MED", 74), ("Brownhill", "MED", 71), ("Gudmundsson", "DEL", 75),
            ("Amdouni", "DEL", 72), ("Foster", "DEL", 70)
        ])
        
        # NOTTINGHAM FOREST - Completar a 11 jugadores
        self._crear_equipo("not", "Nottingham Forest", "Premier League", [
            ("Turner", "POR", 72), ("Aina", "DEF", 71), ("Murillo", "DEF", 73),
            ("Boly", "DEF", 72), ("Toffolo", "DEF", 70), ("Yates", "MED", 74),
            ("Mangala", "MED", 72), ("Gibbs-White", "MED", 76), ("Elanga", "DEL", 73),
            ("Wood", "DEL", 75), ("Hudson-Odoi", "DEL", 74)
        ])
        
        # BOURNEMOUTH - Completar a 11 jugadores
        self._crear_equipo("bou", "Bournemouth", "Premier League", [
            ("Neto", "POR", 73), ("Smith", "DEF", 72), ("Zabarnyi", "DEF", 74),
            ("Senesi", "DEF", 73), ("Kerkez", "DEF", 71), ("Cook", "MED", 75),
            ("Christie", "MED", 74), ("Kluivert", "MED", 76), ("Semenyo", "DEL", 73),
            ("Solanke", "DEL", 77), ("Tavernier", "DEL", 72)
        ])
        
        # SHEFFIELD UNITED - Completar a 11 jugadores
        self._crear_equipo("shf", "Sheffield United", "Premier League", [
            ("Foderingham", "POR", 69), ("Bogle", "DEF", 68), ("Egan", "DEF", 70),
            ("Robinson", "DEF", 69), ("Lowe", "DEF", 67), ("Norwood", "MED", 72),
            ("Souza", "MED", 70), ("Hamer", "MED", 73), ("McAtee", "DEL", 71),
            ("McBurnie", "DEL", 69), ("Osula", "DEL", 66)
        ])
        
        # LUTON TOWN - Completar a 11 jugadores
        self._crear_equipo("lut", "Luton Town", "Premier League", [
            ("Kaminski", "POR", 68), ("Doughty", "DEF", 67), ("Lockyer", "DEF", 69),
            ("Mengi", "DEF", 68), ("Bell", "DEF", 66), ("Nakamba", "MED", 71),
            ("Barkley", "MED", 74), ("Mpanzu", "MED", 69), ("Townsend", "DEL", 72),
            ("Morris", "DEL", 68), ("Adebayo", "DEL", 70)
        ])
        
        # LEICESTER CITY - Completar a 11 jugadores
        self._crear_equipo("lei", "Leicester City", "Premier League", [
            ("Hermansen", "POR", 72), ("Justin", "DEF", 74), ("Vestergaard", "DEF", 73),
            ("Faes", "DEF", 72), ("Kristiansen", "DEF", 71), ("Winks", "MED", 76),
            ("Ndidi", "MED", 77), ("Dewsbury-Hall", "MED", 74), ("Fatawu", "DEL", 72),
            ("Vardy", "DEL", 78), ("Mavididi", "DEL", 73)
        ])
        
        # LA LIGA - Completar todos a 11 jugadores
        self._crear_equipo("rmd", "Real Madrid", "La Liga", [
            ("Courtois", "POR", 89), ("Carvajal", "DEF", 86), ("Militao", "DEF", 85),
            ("Rudiger", "DEF", 84), ("Mendy", "DEF", 83), ("Modric", "MED", 88),
            ("Kroos", "MED", 87), ("Camavinga", "MED", 84), ("Vinicius", "DEL", 91),
            ("Benzema", "DEL", 89), ("Rodrygo", "DEL", 85)
        ])
        
        self._crear_equipo("bar", "Barcelona", "La Liga", [
            ("Ter_Stegen", "POR", 88), ("Kounde", "DEF", 84), ("Araujo", "DEF", 83),
            ("Christensen", "DEF", 81), ("Balde", "DEF", 80), ("Pedri", "MED", 87),
            ("Gavi", "MED", 84), ("De_Jong", "MED", 86), ("Raphinha", "DEL", 83),
            ("Lewandowski", "DEL", 89), ("Dembele", "DEL", 85)
        ])
        
        self._crear_equipo("atl", "Atletico Madrid", "La Liga", [
            ("Oblak", "POR", 90), ("Molina", "DEF", 82), ("Gimenez", "DEF", 85),
            ("Savic", "DEF", 83), ("Hermoso", "DEF", 82), ("Koke", "MED", 84),
            ("De_Paul", "MED", 83), ("Llorente", "MED", 84), ("Felix", "DEL", 86),
            ("Griezmann", "DEL", 87), ("Correa", "DEL", 81)
        ])
        
                # REAL SOCIEDAD - Completar a 11 jugadores REALES
        self._crear_equipo("rsoc", "Real Sociedad", "La Liga", [
            ("Remiro", "POR", 82), ("Traore", "DEF", 76), ("Le_Normand", "DEF", 81),
            ("Zubeldia", "DEF", 78), ("Rico", "DEF", 77), ("Zubimendi", "MED", 84),
            ("Merino", "MED", 82), ("Silva", "MED", 83), ("Kubo", "DEL", 83),
            ("Sørloth", "DEL", 79), ("Oyarzabal", "DEL", 84)
        ])
        
        # SEVILLA - Completar a 11 jugadores REALES
        self._crear_equipo("sev", "Sevilla", "La Liga", [
            ("Dmitrović", "POR", 78), ("Navas", "DEF", 77), ("Bade", "DEF", 76),
            ("Marcão", "DEF", 75), ("Acuña", "DEF", 79), ("Rakitić", "MED", 80),
            ("Gudelj", "MED", 77), ("Jordan", "MED", 76), ("Ocampos", "DEL", 78),
            ("En-Nesyri", "DEL", 79), ("Lamela", "DEL", 77)
        ])
        
        # VALENCIA - Completar a 11 jugadores REALES
        self._crear_equipo("val", "Valencia", "La Liga", [
            ("Mamardashvili", "POR", 80), ("Correia", "DEF", 75), ("Diakhaby", "DEF", 76),
            ("Cömert", "DEF", 74), ("Gayà", "DEF", 81), ("Guillamón", "MED", 75),
            ("Musah", "MED", 77), ("Almeida", "MED", 73), ("Lino", "DEL", 76),
            ("Cavani", "DEL", 79), ("Duro", "DEL", 74)
        ])
        
        # VILLARREAL - Completar a 11 jugadores REALES
        self._crear_equipo("vil", "Villarreal", "La Liga", [
            ("Reina", "POR", 77), ("Foyth", "DEF", 79), ("Pau_Torres", "DEF", 82),
            ("Albiol", "DEF", 76), ("Moreno", "DEF", 78), ("Parejo", "MED", 83),
            ("Capoue", "MED", 77), ("Baena", "MED", 76), ("Chukwueze", "DEL", 81),
            ("Jackson", "DEL", 77), ("Morales", "DEL", 75)
        ])
        
        # REAL BETIS - Completar a 11 jugadores REALES
        self._crear_equipo("bet", "Real Betis", "La Liga", [
            ("Bravo", "POR", 76), ("Sabaly", "DEF", 75), ("Peña", "DEF", 74),
            ("Felipe", "DEF", 73), ("Miranda", "DEF", 72), ("Guido", "MED", 76),
            ("Rodri", "MED", 75), ("Fekir", "MED", 82), ("Juanmi", "DEL", 75),
            ("Iglesias", "DEL", 77), ("Canales", "DEL", 79)
        ])
        
        # ATHLETIC BILBAO - Completar a 11 jugadores REALES
        self._crear_equipo("ath", "Athletic Bilbao", "La Liga", [
            ("Simón", "POR", 80), ("De_Marcos", "DEF", 76), ("Vivian", "DEF", 75),
            ("Iñigo", "DEF", 77), ("Yuri", "DEF", 76), ("Vesga", "MED", 74),
            ("Dani_García", "MED", 75), ("Sancet", "MED", 78), ("Iñaki", "DEL", 79),
            ("Williams", "DEL", 81), ("Berenguer", "DEL", 76)
        ])
        
        # OSASUNA - Completar a 11 jugadores REALES
        self._crear_equipo("osa", "Osasuna", "La Liga", [
            ("Herrera", "POR", 75), ("Vidal", "DEF", 72), ("David_García", "DEF", 76),
            ("Aridane", "DEF", 73), ("Cruz", "DEF", 71), ("Torró", "MED", 74),
            ("Moncayola", "MED", 73), ("Brasanac", "MED", 72), ("Rubén_García", "DEL", 73),
            ("Ávila", "DEL", 72), ("Budimir", "DEL", 75)
        ])
        
        # GETAFE - Completar a 11 jugadores REALES
        self._crear_equipo("get", "Getafe", "La Liga", [
            ("Soria", "POR", 74), ("Damián", "DEF", 71), ("Djené", "DEF", 73),
            ("Duarte", "DEF", 72), ("Algobia", "DEF", 70), ("Maksimović", "MED", 73),
            ("Arambarri", "MED", 74), ("Millà", "MED", 71), ("Ünal", "DEL", 76),
            ("Mayoral", "DEL", 73), ("Mata", "DEL", 72)
        ])
        
        # RAYO VALLECANO - Completar a 11 jugadores REALES
        self._crear_equipo("ray", "Rayo Vallecano", "La Liga", [
            ("Dimitrievski", "POR", 75), ("Balliu", "DEF", 72), ("Lejeune", "DEF", 73),
            ("Catena", "DEF", 72), ("García", "DEF", 71), ("Valentín", "MED", 73),
            ("Comesaña", "MED", 72), ("Trejo", "MED", 74), ("Palazón", "DEL", 75),
            ("De_Tomás", "DEL", 76), ("Camello", "DEL", 73)
        ])
        
        # CELTA VIGO - Completar a 11 jugadores REALES
        self._crear_equipo("cel", "Celta Vigo", "La Liga", [
            ("Marchesín", "POR", 76), ("Mallo", "DEF", 73), ("Aidoo", "DEF", 74),
            ("Núñez", "DEF", 72), ("Galán", "DEF", 73), ("Beltran", "MED", 75),
            ("Tapia", "MED", 73), ("Veiga", "MED", 77), ("Aspas", "DEL", 82),
            ("Iago", "DEL", 76), ("Larsen", "DEL", 74)
        ])
        
        # CADIZ - Completar a 11 jugadores REALES
        self._crear_equipo("cad", "Cadiz", "La Liga", [
            ("Ledesma", "POR", 73), ("Iza", "DEF", 71), ("Fali", "DEF", 72),
            ("Chust", "DEF", 70), ("Espino", "DEF", 71), ("Alcaraz", "MED", 73),
            ("Emeterio", "MED", 70), ("Bongonda", "MED", 72), ("Negredo", "DEL", 74),
            ("Lozano", "DEL", 71), ("Sobrino", "DEL", 70)
        ])
        
        # GRANADA - Completar a 11 jugadores REALES
        self._crear_equipo("gra", "Granada", "La Liga", [
            ("Maximiano", "POR", 72), ("Quini", "DEF", 69), ("Torrente", "DEF", 68),
            ("Sánchez", "DEF", 70), ("Neva", "DEF", 69), ("Gonalons", "MED", 71),
            ("Montoro", "MED", 70), ("Puertas", "MED", 72), ("Suárez", "DEL", 73),
            ("Uzuni", "DEL", 71), ("Calderón", "DEL", 69)
        ])
        
        # LAS PALMAS - Completar a 11 jugadores REALES
        self._crear_equipo("las", "Las Palmas", "La Liga", [
            ("Valles", "POR", 71), ("Álex_Suárez", "DEF", 69), ("Coco", "DEF", 70),
            ("Marmol", "DEF", 68), ("Cardona", "DEF", 69), ("Fabio", "MED", 72),
            ("Enzo", "MED", 71), ("Pejiño", "MED", 70), ("Sandrá", "DEL", 72),
            ("Moleiro", "DEL", 73), ("Cardona", "DEL", 71)
        ])
        
        # ALMERIA - Completar a 11 jugadores REALES
        self._crear_equipo("alm", "Almeria", "La Liga", [
            ("Fernando", "POR", 70), ("Akieme", "DEF", 69), ("Babić", "DEF", 68),
            ("Kaiky", "DEF", 67), ("Centelles", "DEF", 68), ("Robertone", "MED", 72),
            ("Samú", "MED", 69), ("Portillo", "MED", 70), ("Embarba", "DEL", 73),
            ("Sadiq", "DEL", 74), ("Ramazani", "DEL", 71)
        ])
        
        # MALLORCA - Completar a 11 jugadores REALES
        self._crear_equipo("mal", "Mallorca", "La Liga", [
            ("Rajković", "POR", 75), ("Maffeo", "DEF", 72), ("Valjent", "DEF", 73),
            ("Raíllo", "DEF", 71), ("Copete", "DEF", 70), ("Baba", "MED", 72),
            ("Morlanes", "MED", 73), ("Darder", "MED", 74), ("Kang-in", "DEL", 76),
            ("Muriqui", "DEL", 72), ("Ndiaye", "DEL", 71)
        ])
        
        # ALAVES - Completar a 11 jugadores REALES
        self._crear_equipo("alv", "Alaves", "La Liga", [
            ("Sivera", "POR", 72), ("Tenaglia", "DEF", 69), ("Laguardia", "DEF", 71),
            ("Abqar", "DEF", 68), ("Duarte", "DEF", 70), ("Pina", "MED", 71),
            ("Guridi", "MED", 70), ("Jason", "MED", 69), ("Rioja", "DEL", 73),
            ("Sylla", "DEL", 72), ("Villalibre", "DEL", 70)
        ])
        
        # GIRONA - Completar a 11 jugadores REALES
        self._crear_equipo("gir", "Girona", "La Liga", [
            ("Juan_Carlos", "POR", 73), ("Arnau", "DEF", 71), ("Juanpe", "DEF", 72),
            ("Bernardo", "DEF", 70), ("Gutiérrez", "DEF", 71), ("Herrera", "MED", 73),
            ("Romeu", "MED", 74), ("Riquelme", "MED", 72), ("Stuani", "DEL", 76),
            ("Castellanos", "DEL", 75), ("Reinier", "DEL", 73)
        ])
        
                # SERIE A - JUVENTUS
        self._crear_equipo("juv", "Juventus", "Serie A", [
            ("Szczęsny", "POR", 85), ("Danilo", "DEF", 82), ("Bremer", "DEF", 83),
            ("Sandró", "DEF", 80), ("Cuadrado", "DEF", 81), ("Locatelli", "MED", 84),
            ("Rabiot", "MED", 83), ("McKennie", "MED", 79), ("Chiesa", "DEL", 85),
            ("Vlahović", "DEL", 84), ("Di María", "DEL", 83)
        ])
        
        # INTER MILAN
        self._crear_equipo("int", "Inter Milan", "Serie A", [
            ("Onana", "POR", 84), ("Darmian", "DEF", 78), ("Bastoni", "DEF", 83),
            ("De Vrij", "DEF", 82), ("Dumfries", "DEF", 81), ("Barella", "MED", 86),
            ("Çalhanoğlu", "MED", 84), ("Mkhitaryan", "MED", 80), ("Martínez", "DEL", 87),
            ("Lukaku", "DEL", 84), ("Džeko", "DEL", 82)
        ])
        
        # AC MILAN
        self._crear_equipo("mil", "AC Milan", "Serie A", [
            ("Maignan", "POR", 86), ("Calabria", "DEF", 79), ("Tomori", "DEF", 83),
            ("Kjær", "DEF", 80), ("Hernández", "DEF", 84), ("Tonali", "MED", 83),
            ("Bennacer", "MED", 82), ("Díaz", "MED", 81), ("Leão", "DEL", 86),
            ("Giroud", "DEL", 82), ("Rebić", "DEL", 79)
        ])
        
        # NAPOLI
        self._crear_equipo("nap", "Napoli", "Serie A", [
            ("Meret", "POR", 82), ("Di Lorenzo", "DEF", 82), ("Kim", "DEF", 84),
            ("Rrahmani", "DEF", 80), ("Mário Rui", "DEF", 78), ("Lobotka", "MED", 83),
            ("Zieliński", "MED", 84), ("Anguissa", "MED", 81), ("Kvaratskhelia", "DEL", 86),
            ("Osimhen", "DEL", 87), ("Politano", "DEL", 80)
        ])
        
        # AS ROMA
        self._crear_equipo("rom", "AS Roma", "Serie A", [
            ("Rui Patrício", "POR", 81), ("Mancini", "DEF", 80), ("Smalling", "DEF", 82),
            ("Ibañez", "DEF", 79), ("Spinazzola", "DEF", 80), ("Cristante", "MED", 81),
            ("Matic", "MED", 80), ("Pellegrini", "MED", 83), ("Dybala", "DEL", 85),
            ("Abraham", "DEL", 82), ("El Shaarawy", "DEL", 79)
        ])
        
        # LAZIO
        self._crear_equipo("laz", "Lazio", "Serie A", [
            ("Provedel", "POR", 80), ("Marušić", "DEF", 77), ("Casale", "DEF", 78),
            ("Romagnoli", "DEF", 81), ("Hysaj", "DEF", 76), ("Milinković-Savić", "MED", 85),
            ("Cataldi", "MED", 77), ("Alberto", "MED", 82), ("Anderson", "DEL", 81),
            ("Immobile", "DEL", 84), ("Zaccagni", "DEL", 80)
        ])
        
        # ATALANTA
        self._crear_equipo("ata", "Atalanta", "Serie A", [
            ("Musso", "POR", 80), ("Tolói", "DEF", 79), ("Djimsiti", "DEF", 78),
            ("Scalvini", "DEF", 77), ("Mæhle", "DEF", 76), ("De Roon", "MED", 79),
            ("Koopmeiners", "MED", 80), ("Pasalic", "MED", 78), ("Lookman", "DEL", 81),
            ("Højlund", "DEL", 78), ("Muriel", "DEL", 80)
        ])
        
        # FIORENTINA
        self._crear_equipo("fio", "Fiorentina", "Serie A", [
            ("Terracciano", "POR", 77), ("Dodô", "DEF", 76), ("Milenković", "DEF", 79),
            ("Igor", "DEF", 77), ("Biraghi", "DEF", 75), ("Amrabat", "MED", 81),
            ("Bonaventura", "MED", 78), ("Castrovilli", "MED", 77), ("González", "DEL", 80),
            ("Jović", "DEL", 77), ("Saponara", "DEL", 76)
        ])
        
        # TORINO
        self._crear_equipo("tor", "Torino", "Serie A", [
            ("Milinković-Savić", "POR", 79), ("Zima", "DEF", 75), ("Buongiorno", "DEF", 76),
            ("Rodríguez", "DEF", 74), ("Aina", "DEF", 73), ("Linetty", "MED", 75),
            ("Ilić", "MED", 74), ("Radošević", "MED", 73), ("Vojvoda", "DEL", 75),
            ("Sanabria", "DEL", 76), ("Radonjić", "DEL", 74)
        ])
        
        # UDINESE
        self._crear_equipo("udi", "Udinese", "Serie A", [
            ("Silvestri", "POR", 77), ("Becão", "DEF", 76), ("Pérez", "DEF", 75),
            ("Bijol", "DEF", 74), ("Udogie", "DEF", 73), ("Walace", "MED", 76),
            ("Arslan", "MED", 75), ("Pereyra", "MED", 77), ("Deulofeu", "DEL", 78),
            ("Success", "DEL", 73), ("Beto", "DEL", 75)
        ])
        
        # GENOA
        self._crear_equipo("gen", "Genoa", "Serie A", [
            ("Martínez", "POR", 75), ("Vásquez", "DEF", 72), ("Bani", "DEF", 73),
            ("Ostigard", "DEF", 71), ("Criscito", "DEF", 74), ("Strootman", "MED", 73),
            ("Badelj", "MED", 72), ("Portanova", "MED", 71), ("Ekuban", "DEL", 72),
            ("Destro", "DEL", 73), ("Pandev", "DEL", 72)
        ])
        
        # EMPOLI
        self._crear_equipo("emp", "Empoli", "Serie A", [
            ("Vicario", "POR", 76), ("Stojanović", "DEF", 71), ("Ismajli", "DEF", 72),
            ("Luperto", "DEF", 70), ("Parisi", "DEF", 69), ("Bandinelli", "MED", 72),
            ("Henderson", "MED", 71), ("Bajrami", "MED", 73), ("Zurkowski", "DEL", 72),
            ("Satriano", "DEL", 71), ("Caputo", "DEL", 73)
        ])
        
        # LECCE
        self._crear_equipo("lec", "Lecce", "Serie A", [
            ("Falcone", "POR", 73), ("Gendrey", "DEF", 69), ("Baschirotto", "DEF", 70),
            ("Umtiti", "DEF", 72), ("Gallo", "DEF", 68), ("Blin", "MED", 70),
            ("Gonzalez", "MED", 69), ("Hjulmand", "MED", 68), ("Strefezza", "DEL", 72),
            ("Ceesay", "DEL", 70), ("Colombo", "DEL", 69)
        ])
        
        # VERONA
        self._crear_equipo("ver", "Verona", "Serie A", [
            ("Montipò", "POR", 74), ("Dawidowicz", "DEF", 71), ("Hien", "DEF", 70),
            ("Magnani", "DEF", 69), ("Doig", "DEF", 68), ("Tameze", "MED", 72),
            ("Hrustic", "MED", 71), ("Lazović", "MED", 70), ("Ngonge", "DEL", 71),
            ("Gaich", "DEL", 70), ("Henry", "DEL", 69)
        ])
        
        # CAGLIARI
        self._crear_equipo("cal", "Cagliari", "Serie A", [
            ("Radunović", "POR", 72), ("Zappa", "DEF", 68), ("Goldaniga", "DEF", 69),
            ("Altare", "DEF", 67), ("Lyons", "DEF", 66), ("Nández", "MED", 73),
            ("Makoumbou", "MED", 68), ("Rog", "MED", 71), ("Luvumbo", "DEL", 69),
            ("Pavoletti", "DEL", 70), ("Shomurodov", "DEL", 71)
        ])
        
        # FROSINONE
        self._crear_equipo("fro", "Frosinone", "Serie A", [
            ("Turati", "POR", 70), ("Lusuardi", "DEF", 66), ("Monterisi", "DEF", 67),
            ("Lucchesi", "DEF", 65), ("Marchizza", "DEF", 66), ("Gori", "MED", 68),
            ("Mazzitelli", "MED", 67), ("Garritano", "MED", 66), ("Ciano", "DEL", 68),
            ("Moro", "DEL", 67), ("Mulattieri", "DEL", 69)
        ])
        
        # SASSUOLO
        self._crear_equipo("sas", "Sassuolo", "Serie A", [
            ("Consigli", "POR", 76), ("Toljan", "DEF", 73), ("Ferrari", "DEF", 75),
            ("Erlić", "DEF", 72), ("Rogerio", "DEF", 71), ("Frattesi", "MED", 78),
            ("López", "MED", 74), ("Thorstvedt", "MED", 73), ("Berardi", "DEL", 80),
            ("Defrel", "DEL", 73), ("Laurentié", "DEL", 72)
        ])
        
        # SAMPDORIA
        self._crear_equipo("sam", "Sampdoria", "Serie A", [
            ("Audero", "POR", 75), ("Bereszynski", "DEF", 72), ("Nuytinck", "DEF", 71),
            ("Colley", "DEF", 70), ("Augello", "DEF", 69), ("Rincón", "MED", 73),
            ("Vieira", "MED", 72), ("Sabiri", "MED", 71), ("Gabbiadini", "DEL", 74),
            ("Quagliarella", "DEL", 73), ("Lammers", "DEL", 70)
        ])
        
        # MONZA
        self._crear_equipo("mon", "Monza", "Serie A", [
            ("Di Gregorio", "POR", 74), ("Calabria", "DEF", 71), ("Mari", "DEF", 72),
            ("Carlos", "DEF", 70), ("Birindelli", "DEF", 69), ("Sensi", "MED", 75),
            ("Pessina", "MED", 74), ("Machín", "MED", 73), ("Mota", "DEL", 72),
            ("Caprari", "DEL", 73), ("Petagna", "DEL", 72)
        ])
        
        # BOLOGNA
        self._crear_equipo("bol", "Bologna", "Serie A", [
            ("Skorupski", "POR", 77), ("Posch", "DEF", 73), ("Soumaoro", "DEF", 74),
            ("Lucumí", "DEF", 72), ("Cambiaso", "DEF", 71), ("Domínguez", "MED", 76),
            ("Schouten", "MED", 75), ("Soriano", "MED", 74), ("Orsolini", "DEL", 77),
            ("Arnautović", "DEL", 76), ("Barrow", "DEL", 75)
        ])
        
                # BUNDESLIGA - BAYERN MUNICH
        self._crear_equipo("bay", "Bayern Munich", "Bundesliga", [
            ("Neuer", "POR", 88), ("Pavard", "DEF", 82), ("De Ligt", "DEF", 85),
            ("Hernández", "DEF", 84), ("Davies", "DEF", 83), ("Kimmich", "MED", 89),
            ("Goretzka", "MED", 85), ("Musiala", "MED", 86), ("Sané", "DEL", 86),
            ("Mané", "DEL", 85), ("Gnabry", "DEL", 84)
        ])
        
        # BORUSSIA DORTMUND
        self._crear_equipo("bvb", "Borussia Dortmund", "Bundesliga", [
            ("Kobel", "POR", 84), ("Meunier", "DEF", 79), ("Süle", "DEF", 82),
            ("Schlotterbeck", "DEF", 81), ("Guerreiro", "DEF", 80), ("Bellingham", "MED", 87),
            ("Can", "MED", 80), ("Reus", "MED", 83), ("Adeyemi", "DEL", 79),
            ("Malen", "DEL", 80), ("Moukoko", "DEL", 78)
        ])
        
        # RB LEIPZIG
        self._crear_equipo("rbz", "RB Leipzig", "Bundesliga", [
            ("Gulácsi", "POR", 83), ("Henrichs", "DEF", 78), ("Orban", "DEF", 80),
            ("Gvardiol", "DEF", 82), ("Raum", "DEF", 79), ("Laimer", "MED", 82),
            ("Schlager", "MED", 78), ("Forsberg", "MED", 81), ("Nkunku", "DEL", 86),
            ("Werner", "DEL", 82), ("Silva", "DEL", 80)
        ])
        
        # BAYER LEVERKUSEN
        self._crear_equipo("lev", "Bayer Leverkusen", "Bundesliga", [
            ("Hrádecký", "POR", 82), ("Frimpong", "DEF", 78), ("Tah", "DEF", 80),
            ("Hincapié", "DEF", 77), ("Bakker", "DEF", 76), ("Palacios", "MED", 81),
            ("Andrich", "MED", 78), ("Wirtz", "MED", 84), ("Diaby", "DEL", 83),
            ("Schick", "DEL", 82), ("Hložek", "DEL", 77)
        ])
        
        # EINTRACHT FRANKFURT
        self._crear_equipo("fra", "Eintracht Frankfurt", "Bundesliga", [
            ("Trapp", "POR", 81), ("Buta", "DEF", 75), ("Ndicka", "DEF", 79),
            ("Tuta", "DEF", 76), ("Lenz", "DEF", 74), ("Sow", "MED", 78),
            ("Rode", "MED", 77), ("Götze", "MED", 80), ("Kolo Muani", "DEL", 82),
            ("Borré", "DEL", 77), ("Kamada", "DEL", 79)
        ])
        
        # FREIBURG
        self._crear_equipo("fre", "Freiburg", "Bundesliga", [
            ("Flekken", "POR", 79), ("Sildillia", "DEF", 73), ("Ginter", "DEF", 80),
            ("Lienhart", "DEF", 77), ("Günter", "DEF", 78), ("Höfler", "MED", 77),
            ("Eggestein", "MED", 76), ("Doan", "MED", 75), ("Griffo", "DEL", 79),
            ("Gregoritsch", "DEL", 76), ("Höler", "DEL", 75)
        ])
        
        # WOLFSBURG
        self._crear_equipo("wol_de", "VfL Wolfsburg", "Bundesliga", [
            ("Casteels", "POR", 81), ("Baku", "DEF", 77), ("Lacroix", "DEF", 78),
            ("Bornauw", "DEF", 76), ("Otávio", "DEF", 75), ("Arnold", "MED", 79),
            ("Gerhardt", "MED", 77), ("Svanberg", "MED", 76), ("Wimmer", "DEL", 75),
            ("Nmecha", "DEL", 77), ("Wind", "DEL", 76)
        ])
        
        # BORUSSIA M'GLADBACH
        self._crear_equipo("bmg", "Borussia M'gladbach", "Bundesliga", [
            ("Omlin", "POR", 78), ("Scally", "DEF", 74), ("Elvedi", "DEF", 79),
            ("Itakura", "DEF", 76), ("Bensebaini", "DEF", 77), ("Kone", "MED", 78),
            ("Weigl", "MED", 77), ("Hofmann", "MED", 79), ("Plea", "DEL", 78),
            ("Thuram", "DEL", 80), ("Stindl", "DEL", 77)
        ])
        
        # UNION BERLIN
        self._crear_equipo("uni", "Union Berlin", "Bundesliga", [
            ("Rønnow", "POR", 77), ("Jaeckel", "DEF", 73), ("Knoche", "DEF", 76),
            ("Leite", "DEF", 74), ("Gießelmann", "DEF", 72), ("Khedira", "MED", 76),
            ("Seguin", "MED", 74), ("Haberer", "MED", 73), ("Becker", "DEL", 77),
            ("Siebatcheu", "DEL", 75), ("Michel", "DEL", 74)
        ])
        
        # VFB STUTTGART
        self._crear_equipo("stu", "VfB Stuttgart", "Bundesliga", [
            ("Müller", "POR", 75), ("Mavropanos", "DEF", 74), ("Anton", "DEF", 75),
            ("Ito", "DEF", 72), ("Sosa", "DEF", 73), ("Endo", "MED", 76),
            ("Karazor", "MED", 72), ("Mangala", "MED", 73), ("Silas", "DEL", 75),
            ("Guirassy", "DEL", 74), ("Tomas", "DEL", 72)
        ])
        
        # MAINZ 05
        self._crear_equipo("may", "Mainz 05", "Bundesliga", [
            ("Zentner", "POR", 76), ("Widmer", "DEF", 73), ("Bell", "DEF", 74),
            ("Hack", "DEF", 72), ("Caci", "DEF", 71), ("Kohr", "MED", 74),
            ("Barkok", "MED", 72), ("Stach", "MED", 73), ("Lee", "DEL", 74),
            ("Ingvartsen", "DEL", 73), ("Burkardt", "DEL", 72)
        ])
        
        # HOFFENHEIM
        self._crear_equipo("hof", "Hoffenheim", "Bundesliga", [
            ("Baumann", "POR", 76), ("Kadeřábek", "DEF", 73), ("Vogt", "DEF", 75),
            ("Akpoguma", "DEF", 72), ("Skov", "DEF", 71), ("Geiger", "MED", 74),
            ("Prömel", "MED", 73), ("Baumgartner", "MED", 76), ("Dabbur", "DEL", 75),
            ("Kramarić", "DEL", 78), ("Rutter", "DEL", 73)
        ])
        
        # FC AUGSBURG
        self._crear_equipo("aug", "FC Augsburg", "Bundesliga", [
            ("Gikiewicz", "POR", 74), ("Gumny", "DEF", 70), ("Gouweleeuw", "DEF", 73),
            ("Uduokhai", "DEF", 71), ("Iago", "DEF", 69), ("Dorsch", "MED", 72),
            ("Maier", "MED", 71), ("Rexhbecaj", "MED", 70), ("Berisha", "DEL", 73),
            ("Demirović", "DEL", 72), ("Niederlechner", "DEL", 71)
        ])
        
        # HERTHA BERLIN
        self._crear_equipo("her", "Hertha Berlin", "Bundesliga", [
            ("Christensen", "POR", 73), ("Kenny", "DEF", 71), ("Rogério", "DEF", 72),
            ("Kempf", "DEF", 70), ("Plattenhardt", "DEF", 71), ("Tousart", "MED", 73),
            ("Serdar", "MED", 72), ("Lukebakio", "MED", 73), ("Jovetić", "DEL", 74),
            ("Kanga", "DEL", 71), ("Richter", "DEL", 72)
        ])
        
        # VFL BOCHUM
        self._crear_equipo("boc", "VfL Bochum", "Bundesliga", [
            ("Riemann", "POR", 72), ("Gamboa", "DEF", 68), ("Masovic", "DEF", 70),
            ("Ordets", "DEF", 69), ("Soares", "DEF", 67), ("Losilla", "MED", 71),
            ("Stöger", "MED", 70), ("Asano", "MED", 69), ("Hofmann", "DEL", 71),
            ("Zoller", "DEL", 69), ("Antwi-Adjei", "DEL", 68)
        ])
        
        # FC KOLN
        self._crear_equipo("col", "FC Koln", "Bundesliga", [
            ("Schwäbe", "POR", 75), ("Schmitz", "DEF", 71), ("Hübers", "DEF", 72),
            ("Chabot", "DEF", 70), ("Hector", "DEF", 73), ("Skhiri", "MED", 76),
            ("Ljubicic", "MED", 72), ("Kainz", "MED", 73), ("Maina", "DEL", 72),
            ("Tigges", "DEL", 71), ("Adamyan", "DEL", 70)
        ])
        
        # WERDER BREMEN
        self._crear_equipo("bre", "Werder Bremen", "Bundesliga", [
            ("Pavlenka", "POR", 75), ("Weiser", "DEF", 73), ("Stark", "DEF", 74),
            ("Friedl", "DEF", 72), ("Jung", "DEF", 71), ("Bittencourt", "MED", 74),
            ("Stage", "MED", 72), ("Schmid", "MED", 71), ("Ducksch", "DEL", 75),
            ("Füllkrug", "DEL", 76), ("Burke", "DEL", 70)
        ])
        
        # SV DARMSTADT
        self._crear_equipo("dar", "SV Darmstadt", "Bundesliga", [
            ("Schuhen", "POR", 70), ("Bader", "DEF", 67), ("Pfeiffer", "DEF", 68),
            ("Gjasula", "DEF", 66), ("Holland", "DEF", 65), ("Schnellhardt", "MED", 68),
            ("Kempe", "MED", 67), ("Honsak", "MED", 66), ("Tietz", "DEL", 69),
            ("Pfeiffer", "DEL", 67), ("Seydel", "DEL", 66)
        ])
        
                # LIGUE 1 - PARIS SAINT-GERMAIN
        self._crear_equipo("psg", "Paris Saint-Germain", "Ligue 1", [
            ("Donnarumma", "POR", 87), ("Hakimi", "DEF", 84), ("Marquinhos", "DEF", 87),
            ("Ramos", "DEF", 84), ("Mendes", "DEF", 82), ("Verratti", "MED", 86),
            ("Vitinha", "MED", 81), ("Soler", "MED", 80), ("Messi", "DEL", 89),
            ("Mbappé", "DEL", 91), ("Neymar", "DEL", 88)
        ])
        
        # MARSEILLE
        self._crear_equipo("mar", "Marseille", "Ligue 1", [
            ("Pau López", "POR", 80), ("Clauss", "DEF", 78), ("Balerdi", "DEF", 77),
            ("Gigot", "DEF", 76), ("Kolasinac", "DEF", 75), ("Rongier", "MED", 79),
            ("Veretout", "MED", 78), ("Guendouzi", "MED", 79), ("Under", "DEL", 78),
            ("Alexis", "DEL", 80), ("Payet", "DEL", 79)
        ])
        
        # LYON
        self._crear_equipo("oly", "Lyon", "Ligue 1", [
            ("Lopes", "POR", 82), ("Gusto", "DEF", 76), ("Lukeba", "DEF", 78),
            ("Diomandé", "DEF", 75), ("Tagliafico", "DEF", 77), ("Caqueret", "MED", 79),
            ("Lepenant", "MED", 74), ("Tolisso", "MED", 78), ("Cherki", "DEL", 77),
            ("Lacazette", "DEL", 82), ("Dembélé", "DEL", 76)
        ])
        
        # AS MONACO
        self._crear_equipo("asm", "AS Monaco", "Ligue 1", [
            ("Nübel", "POR", 81), ("Vanderson", "DEF", 77), ("Disasi", "DEF", 79),
            ("Badiashile", "DEF", 78), ("Caio Henrique", "DEF", 76), ("Fofana", "MED", 80),
            ("Camara", "MED", 75), ("Golovin", "MED", 79), ("Diatta", "DEL", 76),
            ("Ben Yedder", "DEL", 83), ("Embolo", "DEL", 78)
        ])
        
        # RENNES
        self._crear_equipo("ren", "Rennes", "Ligue 1", [
            ("Mandanda", "POR", 79), ("Traoré", "DEF", 75), ("Omari", "DEF", 76),
            ("Theate", "DEF", 75), ("Truffert", "DEF", 74), ("Santamaria", "MED", 77),
            ("Majer", "MED", 78), ("Bourigeaud", "MED", 77), ("Doku", "DEL", 78),
            ("Kalimuendo", "DEL", 76), ("Gouiri", "DEL", 79)
        ])
        
        # LILLE
        self._crear_equipo("lil", "Lille", "Ligue 1", [
            ("Chevalier", "POR", 77), ("Diakité", "DEF", 74), ("Fonte", "DEF", 76),
            ("Djalo", "DEF", 73), ("Ismaily", "DEF", 72), ("André", "MED", 78),
            ("Angel Gomes", "MED", 76), ("Bamba", "MED", 75), ("David", "DEL", 81),
            ("Bayo", "DEL", 73), ("Zhegrova", "DEL", 74)
        ])
        
        # NICE
        self._crear_equipo("nic", "Nice", "Ligue 1", [
            ("Schmeichel", "POR", 80), ("Lotomba", "DEF", 74), ("Todibo", "DEF", 78),
            ("Dante", "DEF", 77), ("Bard", "DEF", 73), ("Thuram", "MED", 77),
            ("Rosario", "MED", 75), ("Boudaoui", "MED", 74), ("Pépé", "DEL", 78),
            ("Laborde", "DEL", 76), ("Delort", "DEL", 75)
        ])
        
        # LENS
        self._crear_equipo("len", "Lens", "Ligue 1", [
            ("Samba", "POR", 79), ("Gradit", "DEF", 75), ("Danso", "DEF", 76),
            ("Medina", "DEF", 74), ("Frankowski", "DEF", 73), ("Fofana", "MED", 78),
            ("Samed", "MED", 75), ("Machado", "MED", 74), ("Sotoca", "DEL", 77),
            ("Openda", "DEL", 79), ("Saïd", "DEL", 73)
        ])
        
        # STRASBOURG
        self._crear_equipo("str", "Strasbourg", "Ligue 1", [
            ("Sels", "POR", 76), ("Delaune", "DEF", 72), ("Nyamsi", "DEF", 73),
            ("Perrin", "DEF", 72), ("Guilbert", "DEF", 71), ("Bellegarde", "MED", 75),
            ("Prcić", "MED", 73), ("Diarra", "MED", 72), ("Diallo", "DEL", 74),
            ("Gameiro", "DEL", 75), ("Ajorque", "DEL", 74)
        ])
        
        # NANTES
        self._crear_equipo("nan", "Nantes", "Ligue 1", [
            ("Lafont", "POR", 78), ("Appiah", "DEF", 73), ("Pallois", "DEF", 74),
            ("Castelletto", "DEF", 72), ("Merlin", "DEF", 71), ("Chirivella", "MED", 75),
            ("Moutoussamy", "MED", 73), ("Blas", "MED", 76), ("Simon", "DEL", 77),
            ("Ganago", "DEL", 73), ("Guessand", "DEL", 72)
        ])
        
        # REIMS
        self._crear_equipo("rei", "Reims", "Ligue 1", [
            ("Diouf", "POR", 75), ("Foket", "DEF", 72), ("Agbadou", "DEF", 73),
            ("Abdelhamid", "DEF", 74), ("De Smet", "DEF", 70), ("Matusiwa", "MED", 74),
            ("Cajuste", "MED", 73), ("Ito", "MED", 72), ("Balogun", "DEL", 78),
            ("Munetsi", "DEL", 75), ("Flips", "DEL", 71)
        ])
        
        # MONTPELLIER
        self._crear_equipo("mtp", "Montpellier", "Ligue 1", [
            ("Lecomte", "POR", 74), ("Sacko", "DEF", 71), ("Jullien", "DEF", 73),
            ("Estève", "DEF", 72), ("Oyongo", "DEF", 70), ("Ferri", "MED", 73),
            ("Chotard", "MED", 72), ("Savannier", "MED", 76), ("Nordín", "DEL", 73),
            ("Wahi", "DEL", 75), ("Germain", "DEL", 72)
        ])
        
        # TOULOUSE
        self._crear_equipo("tou", "Toulouse", "Ligue 1", [
            ("Dupe", "POR", 73), ("Desler", "DEF", 71), ("Rouault", "DEF", 72),
            ("Nicolaisen", "DEF", 71), ("Sylla", "DEF", 70), ("Spierings", "MED", 73),
            ("Dejaegere", "MED", 72), ("Van den Boomen", "MED", 74), ("Aboukhlal", "DEL", 74),
            ("Dallinga", "DEL", 73), ("Ratao", "DEL", 71)
        ])
        
        # LORIENT
        self._crear_equipo("lor", "Lorient", "Ligue 1", [
            ("Mannone", "POR", 74), ("Kalulu", "DEF", 71), ("Laporte", "DEF", 72),
            ("Talbi", "DEF", 71), ("Le Goff", "DEF", 70), ("Abergel", "MED", 73),
            ("Le Fée", "MED", 72), ("Ponceau", "MED", 71), ("Moffi", "DEL", 77),
            ("Koné", "DEL", 73), ("Dieng", "DEL", 72)
        ])
        
        # BREST
        self._crear_equipo("brest", "Brest", "Ligue 1", [
            ("Bizot", "POR", 73), ("Lala", "DEF", 71), ("Chardonnet", "DEF", 72),
            ("Herelle", "DEF", 70), ("Duverne", "DEF", 69), ("Magnetti", "MED", 72),
            ("Belkebla", "MED", 71), ("Camara", "MED", 70), ("Honorat", "DEL", 74),
            ("Mounié", "DEL", 73), ("Le Douaron", "DEL", 71)
        ])
        
        # CLERMONT
        self._crear_equipo("cle", "Clermont", "Ligue 1", [
            ("Diaw", "POR", 72), ("Zedadka", "DEF", 69), ("Wieteska", "DEF", 70),
            ("Ogier", "DEF", 69), ("Borges", "DEF", 68), ("Gastien", "MED", 71),
            ("Samed", "MED", 70), ("Khaoui", "MED", 69), ("Rashani", "DEL", 72),
            ("Andrić", "DEL", 71), ("Kyei", "DEL", 70)
        ])
        
        # METZ
        self._crear_equipo("metz", "Metz", "Ligue 1", [
            ("Oukidja", "POR", 73), ("Centonze", "DEF", 70), ("Traoré", "DEF", 71),
            ("Kouyaté", "DEF", 69), ("Udol", "DEF", 68), ("N'Doram", "MED", 72),
            ("Camara", "MED", 71), ("Sarr", "MED", 70), ("Mikautadze", "DEL", 73),
            ("Maziz", "DEL", 70), ("Jallow", "DEL", 69)
        ])
        
        # LE HAVRE
        self._crear_equipo("hav", "Le Havre", "Ligue 1", [
            ("Gorgelin", "POR", 71), ("Operi", "DEF", 68), ("Sangante", "DEF", 69),
            ("Lloris", "DEF", 67), ("El Hajjam", "DEF", 66), ("Kechta", "MED", 70),
            ("Alioui", "MED", 69), ("Boutaïb", "MED", 68), ("Bayo", "DEL", 71),
            ("Kitala", "DEL", 69), ("Cornette", "DEL", 68)
        ])
        
                # PRIMEIRA LIGA - BENFICA
        self._crear_equipo("ben", "Benfica", "Primeira Liga", [
            ("Vlachodimos", "POR", 82), ("Bah", "DEF", 77), ("António Silva", "DEF", 79),
            ("Otamendi", "DEF", 81), ("Grimaldo", "DEF", 80), ("Florentino", "MED", 78),
            ("Enzo", "MED", 83), ("João Mário", "MED", 79), ("Rafa", "DEL", 82),
            ("Gonçalo Ramos", "DEL", 80), ("Neres", "DEL", 79)
        ])
        
        # PORTO
        self._crear_equipo("por", "Porto", "Primeira Liga", [
            ("Diogo Costa", "POR", 83), ("João Mário", "DEF", 76), ("Pepe", "DEF", 82),
            ("Marcano", "DEF", 78), ("Zaidu", "DEF", 75), ("Uribe", "MED", 81),
            ("Eustáquio", "MED", 77), ("Otávio", "MED", 80), ("Galeno", "DEL", 78),
            ("Taremi", "DEL", 82), ("Pepê", "DEL", 79)
        ])
        
        # SPORTING CP
        self._crear_equipo("spo", "Sporting CP", "Primeira Liga", [
            ("Adán", "POR", 80), ("Porro", "DEF", 79), ("Coates", "DEF", 80),
            ("Inácio", "DEF", 78), ("Reis", "DEF", 76), ("Morita", "MED", 77),
            ("Ugarte", "MED", 79), ("Trincão", "MED", 78), ("Edwards", "DEL", 80),
            ("Paulinho", "DEL", 78), ("Santos", "DEL", 77)
        ])
        
        # BRAGA
        self._crear_equipo("bra", "Braga", "Primeira Liga", [
            ("Matheus", "POR", 78), ("Gómez", "DEF", 75), ("Niakaté", "DEF", 76),
            ("Tormena", "DEF", 74), ("Sequeira", "DEF", 73), ("Al Musrati", "MED", 79),
            ("Castro", "MED", 76), ("Horta", "MED", 78), ("Ruiz", "DEL", 77),
            ("Abel Ruiz", "DEL", 76), ("Banza", "DEL", 75)
        ])
        
        # VITORIA GUIMARAES
        self._crear_equipo("vit", "Vitoria Guimaraes", "Primeira Liga", [
            ("Bruno Varela", "POR", 75), ("Manu", "DEF", 72), ("Villanueva", "DEF", 73),
            ("Bruma", "DEF", 71), ("Hákon", "DEF", 70), ("André", "MED", 74),
            ("Tiago Silva", "MED", 73), ("Almeida", "MED", 72), ("André Silva", "DEL", 75),
            ("Jota", "DEL", 73), ("Nelson", "DEL", 72)
        ])
        
        # GIL VICENTE
        self._crear_equipo("gui", "Gil Vicente", "Primeira Liga", [
            ("Andrew", "POR", 73), ("Carvalho", "DEF", 70), ("Fernando", "DEF", 71),
            ("Cunha", "DEF", 69), ("Talocha", "DEF", 68), ("Fujimoto", "MED", 72),
            ("Boateng", "MED", 71), ("Kanya", "MED", 70), ("Depú", "DEL", 73),
            ("Navarro", "DEL", 72), ("Lino", "DEL", 71)
        ])
        
        # RIO AVE
        self._crear_equipo("avo", "Rio Ave", "Primeira Liga", [
            ("Jhonatan", "POR", 72), ("Costinha", "DEF", 69), ("Aderllan", "DEF", 70),
            ("Patrick", "DEF", 68), ("Gelson", "DEF", 67), ("Vitor", "MED", 71),
            ("Guga", "MED", 70), ("Joca", "MED", 69), ("Embaló", "DEL", 72),
            ("Aziz", "DEL", 71), ("Zé Manuel", "DEL", 70)
        ])
        
        # MOREIRENSE
        self._crear_equipo("mor", "Moreirense", "Primeira Liga", [
            ("Kewin", "POR", 71), ("Marcelo", "DEF", 68), ("Lucas", "DEF", 69),
            ("Steven", "DEF", 67), ("Fábio", "DEF", 66), ("Gomes", "MED", 70),
            ("Sori", "MED", 69), ("Camacho", "MED", 68), ("Kodisang", "DEL", 71),
            ("Frimpong", "DEL", 70), ("Plata", "DEL", 69)
        ])
        
        # TONDELA
        self._crear_equipo("ton", "Tondela", "Primeira Liga", [
            ("Babić", "POR", 70), ("Jota", "DEF", 67), ("Modibo", "DEF", 68),
            ("Neto", "DEF", 66), ("Tiago", "DEF", 65), ("Pedro", "MED", 69),
            ("Jaquité", "MED", 68), ("Rafael", "MED", 67), ("Juan", "DEL", 70),
            ("Mario", "DEL", 69), ("Teló", "DEL", 68)
        ])
        
        # RIO AVE (segundo equipo con mismo nombre)
        self._crear_equipo("rio", "Rio Ave B", "Primeira Liga", [
            ("Magrão", "POR", 69), ("Brenno", "DEF", 66), ("Aderlan", "DEF", 67),
            ("Jorge", "DEF", 65), ("Zé", "DEF", 64), ("Guga", "MED", 68),
            ("Vitor", "MED", 67), ("Joca", "MED", 66), ("Embaló", "DEL", 69),
            ("Aziz", "DEL", 68), ("Manuel", "DEL", 67)
        ])
        
        # CASA PIA
        self._crear_equipo("csmf", "Casa Pia", "Primeira Liga", [
            ("Ricardo", "POR", 70), ("Léo", "DEF", 67), ("Nermin", "DEF", 68),
            ("Vasco", "DEF", 66), ("Afonso", "DEF", 65), ("Neto", "MED", 69),
            ("Takahashi", "MED", 68), ("Rafael", "MED", 67), ("Kiki", "DEL", 70),
            ("Felippe", "DEL", 69), ("Jota", "DEL", 68)
        ])
        
        # BELENENSES
        self._crear_equipo("bel", "Belenenses", "Primeira Liga", [
            ("Felipe", "POR", 69), ("Chima", "DEF", 66), ("Gonçalo", "DEF", 67),
            ("Rúben", "DEF", 65), ("Tiago", "DEF", 64), ("Silvestre", "MED", 68),
            ("Afonso", "MED", 67), ("Mateus", "MED", 66), ("Rúben", "DEL", 69),
            ("Kikas", "DEL", 68), ("Gonçalo", "DEL", 67)
        ])
        
        # PORTIMONENSE
        self._crear_equipo("port", "Portimonense", "Primeira Liga", [
            ("Kosuke", "POR", 71), ("Fahd", "DEF", 68), ("Lucas", "DEF", 69),
            ("Pedrão", "DEF", 67), ("Moura", "DEF", 66), ("Carlinhos", "MED", 70),
            ("Lucas", "MED", 69), ("Shuhei", "MED", 68), ("Wesley", "DEL", 71),
            ("Ronaldo", "DEL", 70), ("Gonçalo", "DEL", 69)
        ])
        
        # SANTA CLARA
        self._crear_equipo("san", "Santa Clara", "Primeira Liga", [
            ("Gabriel", "POR", 70), ("Paulo", "DEF", 67), ("Mansur", "DEF", 68),
            ("Rafael", "DEF", 66), ("Ricardo", "DEF", 65), ("Costinha", "MED", 69),
            ("Rafael", "MED", 68), ("Lincoln", "MED", 67), ("Rafael", "DEL", 70),
            ("Mansur", "DEL", 69), ("Ricardo", "DEL", 68)
        ])
        
        # FAMALICAO
        self._crear_equipo("far", "Famalicao", "Primeira Liga", [
            ("Ivan", "POR", 69), ("Alex", "DEF", 66), ("Patrick", "DEF", 67),
            ("Riccieli", "DEF", 65), ("Nehuén", "DEF", 64), ("Pêpê", "MED", 68),
            ("Gustavo", "MED", 67), ("Ivo", "MED", 66), ("Simon", "DEL", 69),
            ("Chiquinho", "DEL", 68), ("Jaime", "DEL", 67)
        ])
        
        # AROUCA
        self._crear_equipo("aro", "Arouca", "Primeira Liga", [
            ("Ignacio", "POR", 68), ("Thales", "DEF", 65), ("Jeremy", "DEF", 66),
            ("Bruno", "DEF", 64), ("Mateus", "DEF", 63), ("David", "MED", 67),
            ("André", "MED", 66), ("Pedro", "MED", 65), ("Oday", "DEL", 68),
            ("André", "DEL", 67), ("Rafael", "DEL", 66)
        ])
        
        # VIZELA
        self._crear_equipo("viz", "Vizela", "Primeira Liga", [
            ("Fabijan", "POR", 67), ("Anderson", "DEF", 64), ("Bruno", "DEF", 65),
            ("Kiko", "DEF", 63), ("Samu", "DEF", 62), ("Claude", "MED", 66),
            ("Alex", "MED", 65), ("Nuno", "MED", 64), ("Kiko", "DEL", 67),
            ("Samu", "DEL", 66), ("Anderson", "DEL", 65)
        ])
        
        # ESTORIL
        self._crear_equipo("est", "Estoril", "Primeira Liga", [
            ("Daniel", "POR", 69), ("Carleto", "DEF", 66), ("Lucas", "DEF", 67),
            ("Bernard", "DEF", 65), ("João", "DEF", 64), ("Gamboa", "MED", 68),
            ("João", "MED", 67), ("Francisco", "MED", 66), ("André", "DEL", 69),
            ("Rafik", "DEL", 68), ("Tiago", "DEL", 67)
        ])
                # EREDIVISIE - AJAX
        self._crear_equipo("aja", "Ajax", "Eredivisie", [
            ("Rulli", "POR", 81), ("Rensch", "DEF", 76), ("Jurriën", "DEF", 79),
            ("Bassey", "DEF", 77), ("Wijndal", "DEF", 76), ("Álvarez", "MED", 80),
            ("Klaassen", "MED", 78), ("Berghuis", "MED", 79), ("Tadic", "DEL", 82),
            ("Bergwijn", "DEL", 80), ("Brobbey", "DEL", 77)
        ])
        
        # PSV EINDHOVEN
        self._crear_equipo("psv", "PSV Eindhoven", "Eredivisie", [
            ("Benítez", "POR", 80), ("Teze", "DEF", 75), ("Boscagli", "DEF", 77),
            ("Obispo", "DEF", 74), ("Max", "DEF", 76), ("Sangaré", "MED", 79),
            ("Veerman", "MED", 78), ("Simons", "MED", 77), ("Bakayoko", "DEL", 76),
            ("De Jong", "DEL", 79), ("Gakpo", "DEL", 81)
        ])
        
        # FEYENOORD
        self._crear_equipo("fey", "Feyenoord", "Eredivisie", [
            ("Bijlow", "POR", 79), ("Geertruida", "DEF", 76), ("Trauner", "DEF", 77),
            ("Hancko", "DEF", 75), ("Hartman", "DEF", 74), ("Kökçü", "MED", 80),
            ("Wieffer", "MED", 75), ("Szymański", "MED", 76), ("Dilrosun", "DEL", 75),
            ("Giménez", "DEL", 77), ("Idrissi", "DEL", 76)
        ])
        
        # AZ ALKMAAR
        self._crear_equipo("az", "AZ Alkmaar", "Eredivisie", [
            ("Ryan", "POR", 78), ("Sugawara", "DEF", 74), ("Hatzidiakos", "DEF", 75),
            ("Beukema", "DEF", 73), ("Kerkez", "DEF", 72), ("Reijnders", "MED", 77),
            ("Clasie", "MED", 76), ("De Wit", "MED", 75), ("Pavlidis", "DEL", 76),
            ("Karlsson", "DEL", 75), ("Meerdink", "DEL", 73)
        ])
        
        # FC TWENTE
        self._crear_equipo("twn", "FC Twente", "Eredivisie", [
            ("Unnerstall", "POR", 77), ("Brenet", "DEF", 73), ("Pröpper", "DEF", 74),
            ("Hilgers", "DEF", 72), ("Smal", "DEF", 71), ("Sadílek", "MED", 75),
            ("Vlap", "MED", 74), ("Tzolis", "MED", 73), ("Cerny", "DEL", 75),
            ("Van Wolfswinkel", "DEL", 74), ("Rots", "DEL", 72)
        ])
        
        # VITESSE
        self._crear_equipo("vit_nl", "Vitesse", "Eredivisie", [
            ("Schubert", "POR", 75), ("Arcus", "DEF", 71), ("Oroz", "DEF", 72),
            ("Isimat-Mirin", "DEF", 73), ("Wittek", "DEF", 70), ("Tronstad", "MED", 74),
            ("Bero", "MED", 73), ("Manhoef", "MED", 72), ("Buitink", "DEL", 73),
            ("Openda", "DEL", 74), ("Darfalou", "DEL", 71)
        ])
        
        # FC UTRECHT
        self._crear_equipo("uti", "FC Utrecht", "Eredivisie", [
            ("Barkas", "POR", 74), ("Van der Maarel", "DEF", 72), ("Van der Hoorn", "DEF", 73),
            ("Janssen", "DEF", 71), ("Douvikas", "DEF", 70), ("Booth", "MED", 73),
            ("Van de Streek", "MED", 72), ("Boussaid", "MED", 71), ("Dost", "DEL", 74),
            ("Labyad", "DEL", 73), ("Mahi", "DEL", 72)
        ])
        
        # FC GRONINGEN
        self._crear_equipo("gro", "FC Groningen", "Eredivisie", [
            ("Leeuwenburgh", "POR", 73), ("Dammers", "DEF", 70), ("Te Wierik", "DEF", 71),
            ("Blokhuis", "DEF", 69), ("Määttä", "DEF", 68), ("Duarte", "MED", 72),
            ("Hove", "MED", 71), ("Suslov", "MED", 70), ("Ngonge", "DEL", 72),
            ("Abraham", "DEL", 71), ("Oratmangoen", "DEL", 70)
        ])
        
        # HERACLES
        self._crear_equipo("her_nl", "Heracles", "Eredivisie", [
            ("Blaswich", "POR", 72), ("Fadiga", "DEF", 69), ("Rente", "DEF", 70),
            ("Quagliata", "DEF", 68), ("Bakboord", "DEF", 67), ("Kiomourtzoglou", "MED", 71),
            ("De la Torre", "MED", 70), ("Vloet", "MED", 69), ("Burgzorg", "DEL", 71),
            ("Sierhuis", "DEL", 70), ("Arweiler", "DEL", 69)
        ])
        
        # WILLEM II
        self._crear_equipo("wil", "Willem II", "Eredivisie", [
            ("Wellenreuther", "POR", 71), ("Köhlert", "DEF", 68), ("Holmen", "DEF", 69),
            ("Heerkens", "DEF", 67), ("Sow", "DEF", 66), ("Spierings", "MED", 70),
            ("Llonch", "MED", 69), ("Nunnely", "MED", 68), ("Kabangu", "DEL", 70),
            ("Wriedt", "DEL", 69), ("Ndayishimiye", "DEL", 68)
        ])
        
        # SC HEERENVEEN
        self._crear_equipo("hee", "SC Heerenveen", "Eredivisie", [
            ("Mous", "POR", 72), ("Van Ewijk", "DEF", 69), ("Van Beek", "DEF", 70),
            ("Bochniewicz", "DEF", 68), ("Wålemark", "DEF", 67), ("Tahiri", "MED", 71),
            ("Haye", "MED", 70), ("Olsson", "MED", 69), ("Colassin", "DEL", 71),
            ("Sarr", "DEL", 70), ("Akkaynak", "DEL", 69)
        ])
        
        # PEC ZWOLLE
        self._crear_equipo("pec", "PEC Zwolle", "Eredivisie", [
            ("Schendelaar", "POR", 70), ("Van Polen", "DEF", 68), ("Kersten", "DEF", 69),
            ("Lamprou", "DEF", 67), ("Saymak", "DEF", 66), ("Huiberts", "MED", 70),
            ("Ghoochannejhad", "MED", 69), ("Drost", "MED", 68), ("Redan", "DEL", 70),
            ("Thy", "DEL", 69), ("Johnsen", "DEL", 68)
        ])
        
        # FORTUNA SITTARD
        self._crear_equipo("for", "Fortuna Sittard", "Eredivisie", [
            ("Pandur", "POR", 71), ("Cox", "DEF", 68), ("Guth", "DEF", 69),
            ("Angha", "DEF", 67), ("Dijks", "DEF", 66), ("Tekie", "MED", 70),
            ("Seuntjens", "MED", 69), ("Fer", "MED", 68), ("Córdoba", "DEL", 71),
            ("Noslin", "DEL", 70), ("Semedo", "DEL", 69)
        ])
        
        # SPARTA ROTTERDAM
        self._crear_equipo("spa_nl", "Sparta Rotterdam", "Eredivisie", [
            ("Okoye", "POR", 72), ("Abrashi", "DEF", 69), ("Vriends", "DEF", 70),
            ("Beugelsdijk", "DEF", 68), ("Pinto", "DEF", 67), ("De Guzmán", "MED", 71),
            ("Brouwers", "MED", 70), ("Mijnans", "MED", 69), ("Lauritsen", "DEL", 71),
            ("Saito", "DEL", 70), ("Duarte", "DEL", 69)
        ])
        
        # GO AHEAD EAGLES
        self._crear_equipo("goe", "Go Ahead Eagles", "Eredivisie", [
            ("De Lange", "POR", 70), ("Kuipers", "DEF", 67), ("Kramer", "DEF", 68),
            ("Idzes", "DEF", 66), ("Linssen", "DEF", 65), ("Rommens", "MED", 69),
            ("Botta", "MED", 68), ("Edvardsen", "MED", 67), ("Stokkers", "DEL", 70),
            ("Duits", "DEL", 69), ("Oratmangoen", "DEL", 68)
        ])
        
        # CAMBUUR
        self._crear_equipo("cam", "Cambuur", "Eredivisie", [
            ("Stevens", "POR", 69), ("Schmidt", "DEF", 66), ("Mac-Intosch", "DEF", 67),
            ("Bergsma", "DEF", 65), ("Siemens", "DEF", 64), ("Hoedemakers", "MED", 68),
            ("Jacobs", "MED", 67), ("Sambissa", "MED", 66), ("Uldriķis", "DEL", 69),
            ("Bangura", "DEL", 68), ("Smit", "DEL", 67)
        ])
        
        # NEC NIJMEGEN
        self._crear_equipo("nec", "NEC Nijmegen", "Eredivisie", [
            ("Cillessen", "POR", 75), ("Van Rooij", "DEF", 71), ("Marquez", "DEF", 72),
            ("Nuytinck", "DEF", 70), ("El Karouani", "DEF", 69), ("Schöne", "MED", 73),
            ("Tannane", "MED", 72), ("Proper", "MED", 71), ("Dimitriadis", "DEL", 72),
            ("Ogawa", "DEL", 71), ("Bruns", "DEL", 70)
        ])
        
        # ALMERE CITY
        self._crear_equipo("almc", "Almere City", "Eredivisie", [
            ("De Lange", "POR", 68), ("Van de Looi", "DEF", 65), ("Akkaynak", "DEF", 66),
            ("Hilterman", "DEF", 64), ("Resink", "DEF", 63), ("Duijvestijn", "MED", 67),
            ("Hansson", "MED", 66), ("Kökcü", "MED", 65), ("Hendriks", "DEL", 68),
            ("Smeets", "DEL", 67), ("Van La Parra", "DEL", 66)
        ])
    def _generar_plantilla_11_jugadores(self, nivel_base: int) -> List[tuple]:
        """Genera una plantilla genérica de exactamente 11 jugadores"""
        plantilla = []
        posiciones = [
            ("Portero", "POR", 1.0), ("Lateral_Derecho", "DEF", 0.9), ("Central_1", "DEF", 1.0),
            ("Central_2", "DEF", 0.95), ("Lateral_Izquierdo", "DEF", 0.9), ("Mediocentro", "MED", 1.0),
            ("Interior_Derecho", "MED", 1.1), ("Interior_Izquierdo", "MED", 1.1), ("Extremo_Derecho", "DEL", 1.2),
            ("Delantero_Centro", "DEL", 1.3), ("Extremo_Izquierdo", "DEL", 1.2)
        ]
        
        for nombre, posicion, multiplicador in posiciones:
            # Variar el nivel ligeramente (±5) y aplicar multiplicador de posición
            variacion = random.randint(-5, 5)
            nivel_jugador = max(45, min(95, int(nivel_base * multiplicador) + variacion))
            plantilla.append((nombre, posicion, nivel_jugador))
        
        return plantilla
        
        for nombre, posicion, _ in posiciones:
            # Variar el nivel ligeramente
            variacion = random.randint(-8, 8)
            nivel_jugador = max(45, min(95, nivel_base + variacion))
            plantilla.append((nombre, posicion, nivel_jugador))
        
        return plantilla
    
    def obtener_todos_los_equipos(self) -> Dict[str, Equipo]:
        """Retorna todos los equipos"""
        return self.equipos
    
    def obtener_equipo(self, codigo: str) -> Equipo:
        """Obtiene un equipo específico"""
        return self.equipos.get(codigo)
    
    def obtener_nivel_equipo(self, codigo: str) -> int:
        """Obtiene el nivel calculado de un equipo"""
        equipo = self.obtener_equipo(codigo)
        return equipo.calcular_nivel_equipo() if equipo else 50
    
    def obtener_ligas(self) -> Dict[str, Dict[str, int]]:
        """Retorna la estructura de ligas para compatibilidad"""
        ligas = {}
        equipos_por_liga = {}
        
        # Agrupar equipos por liga
        for codigo, equipo in self.equipos.items():
            if equipo.liga not in equipos_por_liga:
                equipos_por_liga[equipo.liga] = {}
            equipos_por_liga[equipo.liga][codigo] = equipo.calcular_nivel_equipo()
        
        return equipos_por_liga
    
    def reset_estadisticas_temporada(self):
        """Resetea las estadísticas de todos los jugadores para nueva temporada"""
        for jugador in self.jugadores.values():
            jugador.goles = 0
            jugador.asistencias = 0
            jugador.partidos_jugados = 0
            jugador.minutos_jugados = 0
            jugador.tarjetas_amarillas = 0
            jugador.tarjetas_rojas = 0
    
    def obtener_top_goleadores(self, limite: int = 10) -> List[Jugador]:
        """Obtiene el top de goleadores"""
        jugadores_con_goles = [j for j in self.jugadores.values() if j.goles > 0]
        return sorted(jugadores_con_goles, key=lambda x: x.goles, reverse=True)[:limite]
    
    def obtener_top_asistentes(self, limite: int = 10) -> List[Jugador]:
        """Obtiene el top de asistentes"""
        jugadores_con_asistencias = [j for j in self.jugadores.values() if j.asistencias > 0]
        return sorted(jugadores_con_asistencias, key=lambda x: x.asistencias, reverse=True)[:limite]
    
    
    
    def registrar_campeon(self, competicion: str, equipo: str):
        """Registra un equipo como campeón de una competición"""
        if competicion in ['champions', 'europa', 'conference']:
            self.campeones[competicion] = equipo
        else:
            self.campeones['ligas'][competicion] = equipo
        
        # Dar bonus de títulos a todos los jugadores del equipo campeón
        equipo_obj = self.obtener_equipo(equipo)
        if equipo_obj:
            for jugador in equipo_obj.jugadores:
                jugador.titulos_colectivos += 1
    
    def obtener_candidatos_balon_oro(self, limite: int = 20) -> List[tuple]:
        """Obtiene los candidatos al Balón de Oro considerando títulos colectivos"""
        jugadores_con_puntos = []
        
        for jugador in self.jugadores.values():
            # Verificar si el jugador es de un equipo campeón
            equipo_campeon = (
                jugador.equipo == self.campeones['champions'] or
                jugador.equipo == self.campeones['europa'] or
                jugador.equipo == self.campeones['conference'] or
                jugador.equipo in self.campeones['ligas'].values()
            )
            
            puntos = jugador.calcular_puntos_balon_oro(equipo_campeon)
            
            # BONUS ADICIONAL POR COMPETICIONES IMPORTANTES
            if jugador.equipo == self.campeones['champions']:
                puntos *= 1.3  # 30% extra por ganar Champions
            elif jugador.equipo == self.campeones['europa']:
                puntos *= 1.2  # 20% extra por ganar Europa League
            elif jugador.equipo == self.campeones['conference']:
                puntos *= 1.1  # 10% extra por ganar Conference
            
            if puntos > 0:
                jugadores_con_puntos.append((jugador, puntos))
        
        return sorted(jugadores_con_puntos, key=lambda x: x[1], reverse=True)[:limite]
    
# Instancia global de la base de datos
base_datos = BaseDatos()