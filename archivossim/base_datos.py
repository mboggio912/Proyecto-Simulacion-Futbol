from dataclasses import dataclass
from typing import Dict, List
import random

@dataclass
class Jugador:
    """Clase que representa a un jugador"""
    nombre: str
    posicion: str  # POR, DEF, MED, DEL
    nivel: int     # 1-99
    equipo: str
    goles: int = 0
    asistencias: int = 0
    partidos_jugados: int = 0
    minutos_jugados: int = 0
    tarjetas_amarillas: int = 0
    tarjetas_rojas: int = 0
    
    def calcular_puntos_balon_oro(self) -> float:
        """Calcula los puntos para el Balón de Oro"""
        # Fórmula que considera goles, asistencias, nivel del jugador y rendimiento del equipo
        puntos_base = (self.goles * 2.0) + (self.asistencias * 1.5)
        multiplicador_nivel = self.nivel / 85.0  # Normalizar por nivel alto
        multiplicador_partidos = min(1.0, self.partidos_jugados / 30.0)  # Penalizar poca participación
        
        return puntos_base * multiplicador_nivel * multiplicador_partidos

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
        self._crear_base_datos()
    
    def _crear_jugador(self, nombre: str, posicion: str, nivel: int, equipo_codigo: str) -> Jugador:
        """Crea un jugador y lo registra en la base de datos"""
        jugador = Jugador(nombre, posicion, nivel, equipo_codigo)
        self.jugadores[f"{equipo_codigo}_{nombre}"] = jugador
        return jugador
    
    def _crear_equipo(self, codigo: str, nombre_completo: str, liga: str, plantilla: List[tuple]) -> Equipo:
        """Crea un equipo con su plantilla completa"""
        jugadores = []
        for nombre, posicion, nivel in plantilla:
            jugador = self._crear_jugador(nombre, posicion, nivel, codigo)
            jugadores.append(jugador)
        
        equipo = Equipo(nombre_completo, liga, jugadores)
        self.equipos[codigo] = equipo
        return equipo
    
    def _crear_base_datos(self):
        """Crea toda la base de datos de equipos y jugadores"""
        
        # PREMIER LEAGUE
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
        
        # Equipos menores Premier League
        self._crear_equipo("new", "Newcastle", "Premier League", [
            ("Pope", "POR", 82), ("Trippier", "DEF", 83), ("Schar", "DEF", 80),
            ("Botman", "DEF", 79), ("Burn", "DEF", 76), ("Guimaraes", "MED", 84),
            ("Longstaff", "MED", 74), ("Joelinton", "MED", 78), ("Almiron", "DEL", 79),
            ("Wilson", "DEL", 78), ("Gordon", "DEL", 76)
        ])
        
        self._crear_equipo("avl", "Aston Villa", "Premier League", [
            ("Martinez", "POR", 84), ("Cash", "DEF", 79), ("Konsa", "DEF", 78),
            ("Pau_Torres", "DEF", 81), ("Digne", "DEF", 80), ("McGinn", "MED", 79),
            ("Luiz", "MED", 82), ("Ramsey", "MED", 76), ("Bailey", "DEL", 77),
            ("Watkins", "DEL", 82), ("Diaby", "DEL", 80)
        ])
        
        self._crear_equipo("wes", "West Ham", "Premier League", [
            ("Areola", "POR", 78), ("Coufal", "DEF", 76), ("Zouma", "DEF", 77),
            ("Aguerd", "DEF", 76), ("Emerson", "DEF", 75), ("Rice", "MED", 84),
            ("Soucek", "MED", 78), ("Paqueta", "MED", 81), ("Bowen", "DEL", 80),
            ("Antonio", "DEL", 76), ("Benrahma", "DEL", 78)
        ])
        
        self._crear_equipo("bha", "Brighton", "Premier League", [
            ("Steele", "POR", 74), ("Veltman", "DEF", 75), ("Dunk", "DEF", 77),
            ("Webster", "DEF", 74), ("Estupinan", "DEF", 78), ("Caicedo", "MED", 82),
            ("Mac_Allister", "MED", 81), ("Gross", "MED", 79), ("Mitoma", "DEL", 79),
            ("Ferguson", "DEL", 76), ("March", "DEL", 74)
        ])
        
        # Completar resto de equipos Premier League con niveles apropiados
        equipos_pl_restantes = [
            ("wol", "Wolves", [("Sa", "POR", 76), ("Semedo", "DEF", 76), ("Kilman", "DEF", 74), ("Dawson", "DEF", 73), ("Ait_Nouri", "DEF", 75), ("Neves", "MED", 80), ("Moutinho", "MED", 76), ("Neto", "MED", 77), ("Traore", "DEL", 76), ("Jimenez", "DEL", 78), ("Cunha", "DEL", 77)]),
            ("cry", "Crystal Palace", [("Guaita", "POR", 75), ("Ward", "DEF", 74), ("Andersen", "DEF", 77), ("Guehi", "DEF", 76), ("Mitchell", "DEF", 73), ("Gallagher", "MED", 78), ("Hughes", "MED", 74), ("Eze", "MED", 79), ("Zaha", "DEL", 80), ("Ayew", "DEL", 72), ("Mateta", "DEL", 75)]),
            ("ful", "Fulham", [("Leno", "POR", 78), ("Tete", "DEF", 74), ("Adarabioyo", "DEF", 75), ("Ream", "DEF", 73), ("Robinson", "DEF", 76), ("Palhinha", "MED", 81), ("Reed", "MED", 74), ("Pereira", "MED", 78), ("Willian", "DEL", 77), ("Mitrovic", "DEL", 80), ("Iwobi", "DEL", 76)]),
            ("eve", "Everton", [("Pickford", "POR", 81), ("Coleman", "DEF", 74), ("Tarkowski", "DEF", 76), ("Branthwaite", "DEF", 73), ("Mykolenko", "DEF", 72), ("Gueye", "MED", 76), ("Onana", "MED", 75), ("Doucoure", "MED", 74), ("Harrison", "DEL", 73), ("Calvert-Lewin", "DEL", 77), ("McNeil", "DEL", 74)]),
            ("bur", "Burnley", [("Trafford", "POR", 70), ("Roberts", "DEF", 69), ("O_Shea", "DEF", 71), ("Esteve", "DEF", 70), ("Taylor", "DEF", 72), ("Cullen", "MED", 73), ("Berge", "MED", 74), ("Brownhill", "MED", 71), ("Gudmundsson", "DEL", 75), ("Amdouni", "DEL", 72), ("Foster", "DEL", 70)]),
            ("not", "Nottingham Forest", [("Turner", "POR", 72), ("Aina", "DEF", 71), ("Murillo", "DEF", 73), ("Boly", "DEF", 72), ("Toffolo", "DEF", 70), ("Yates", "MED", 74), ("Mangala", "MED", 72), ("Gibbs-White", "MED", 76), ("Elanga", "DEL", 73), ("Wood", "DEL", 75), ("Hudson-Odoi", "DEL", 74)]),
            ("bou", "Bournemouth", [("Neto", "POR", 73), ("Smith", "DEF", 72), ("Zabarnyi", "DEF", 74), ("Senesi", "DEF", 73), ("Kerkez", "DEF", 71), ("Cook", "MED", 75), ("Christie", "MED", 74), ("Kluivert", "MED", 76), ("Semenyo", "DEL", 73), ("Solanke", "DEL", 77), ("Tavernier", "DEL", 72)]),
            ("shf", "Sheffield United", [("Foderingham", "POR", 69), ("Bogle", "DEF", 68), ("Egan", "DEF", 70), ("Robinson", "DEF", 69), ("Lowe", "DEF", 67), ("Norwood", "MED", 72), ("Souza", "MED", 70), ("Hamer", "MED", 73), ("McAtee", "DEL", 71), ("McBurnie", "DEL", 69), ("Osula", "DEL", 66)]),
            ("lut", "Luton Town", [("Kaminski", "POR", 68), ("Doughty", "DEF", 67), ("Lockyer", "DEF", 69), ("Mengi", "DEF", 68), ("Bell", "DEF", 66), ("Nakamba", "MED", 71), ("Barkley", "MED", 74), ("Mpanzu", "MED", 69), ("Townsend", "DEL", 72), ("Morris", "DEL", 68), ("Adebayo", "DEL", 70)]),
            ("lei", "Leicester City", [("Hermansen", "POR", 72), ("Justin", "DEF", 74), ("Vestergaard", "DEF", 73), ("Faes", "DEF", 72), ("Kristiansen", "DEF", 71), ("Winks", "MED", 76), ("Ndidi", "MED", 77), ("Dewsbury-Hall", "MED", 74), ("Fatawu", "DEL", 72), ("Vardy", "DEL", 78), ("Mavididi", "DEL", 73)])
        ]
        
        for codigo, nombre, plantilla in equipos_pl_restantes:
            self._crear_equipo(codigo, nombre, "Premier League", plantilla)
        
        # LA LIGA
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
        
        # Continuar con más equipos de La Liga, Serie A, Bundesliga, etc.
        # Por brevedad, voy a crear plantillas más simples para el resto
        
        # Resto de La Liga (simplificado)
        equipos_laliga_restantes = [
            ("rsoc", "Real Sociedad", [("Remiro", "POR", 79), ("Aritz", "DEF", 77), ("Le_Normand", "DEF", 80), ("Zubeldia", "DEF", 78), ("Munoz", "DEF", 76), ("Zubimendi", "MED", 82), ("Merino", "MED", 81), ("Silva", "MED", 83), ("Kubo", "DEL", 82), ("Sorloth", "DEL", 79), ("Oyarzabal", "DEL", 80)]),
            ("sev", "Sevilla", [("Bono", "POR", 80), ("Jesus_Navas", "DEF", 79), ("Kounde", "DEF", 82), ("Carlos", "DEF", 77), ("Acuna", "DEF", 78), ("Rakitic", "MED", 81), ("Jordan", "MED", 76), ("Papu", "MED", 79), ("Ocampos", "DEL", 78), ("En_Nesyri", "DEL", 77), ("Lamela", "DEL", 76)]),
            ("val", "Valencia", [("Giorgi", "POR", 76), ("Correia", "DEF", 75), ("Paulista", "DEF", 77), ("Diakhaby", "DEF", 74), ("Gaya", "DEF", 78), ("Guillamon", "MED", 76), ("Soler", "MED", 79), ("Musah", "MED", 77), ("Guedes", "DEL", 78), ("Gomez", "DEL", 76), ("Cavani", "DEL", 80)]),
            ("vil", "Villarreal", [("Rulli", "POR", 78), ("Foyth", "DEF", 77), ("Albiol", "DEF", 79), ("Torres", "DEF", 78), ("Moreno", "DEF", 80), ("Parejo", "MED", 82), ("Capoue", "MED", 78), ("Lo_Celso", "MED", 80), ("Chukwueze", "DEL", 79), ("Gerard", "DEL", 81), ("Baena", "DEL", 76)])
        ]
        
        # Agregar equipos menores de La Liga con niveles más bajos
        equipos_laliga_menores = [
            ("bet", "Real Betis", 72), ("ath", "Athletic Bilbao", 75), ("osa", "Osasuna", 68),
            ("get", "Getafe", 65), ("ray", "Rayo Vallecano", 63), ("cel", "Celta Vigo", 62),
            ("cad", "Cadiz", 58), ("gra", "Granada", 57), ("las", "Las Palmas", 60),
            ("alm", "Almeria", 56), ("mal", "Mallorca", 64), ("alv", "Alaves", 55),
            ("gir", "Girona", 59)
        ]
        
        for codigo, nombre, plantilla in equipos_laliga_restantes:
            self._crear_equipo(codigo, nombre, "La Liga", plantilla)
            
        for codigo, nombre, nivel_base in equipos_laliga_menores:
            plantilla_generica = self._generar_plantilla_generica(nivel_base)
            self._crear_equipo(codigo, nombre, "La Liga", plantilla_generica)
        
        # SERIE A
        equipos_seriea = [
            ("juv", "Juventus", 79), ("int", "Inter Milan", 82), ("mil", "AC Milan", 78),
            ("nap", "Napoli", 76), ("rom", "AS Roma", 74), ("laz", "Lazio", 73),
            ("ata", "Atalanta", 80), ("fio", "Fiorentina", 71), ("tor", "Torino", 68),
            ("udi", "Udinese", 65), ("gen", "Genoa", 64), ("emp", "Empoli", 62),
            ("lec", "Lecce", 58), ("ver", "Verona", 63), ("cal", "Cagliari", 59),
            ("fro", "Frosinone", 56), ("sas", "Sassuolo", 64), ("sam", "Sampdoria", 61),
            ("mon", "Monza", 63), ("bol", "Bologna", 66)
        ]
        
        for codigo, nombre, nivel_base in equipos_seriea:
            plantilla_generica = self._generar_plantilla_generica(nivel_base)
            self._crear_equipo(codigo, nombre, "Serie A", plantilla_generica)
        
        # BUNDESLIGA
        equipos_bundesliga = [
            ("bay", "Bayern Munich", 84), ("bvb", "Borussia Dortmund", 80), ("rbz", "RB Leipzig", 78),
            ("lev", "Bayer Leverkusen", 76), ("fra", "Eintracht Frankfurt", 72), ("fre", "Freiburg", 70),
            ("wol_de", "VfL Wolfsburg", 68), ("bmg", "Borussia M'gladbach", 71), ("uni", "Union Berlin", 69),
            ("stu", "VfB Stuttgart", 65), ("may", "Mainz 05", 64), ("hof", "Hoffenheim", 67),
            ("aug", "FC Augsburg", 61), ("her", "Hertha Berlin", 63), ("boc", "VfL Bochum", 58),
            ("col", "FC Koln", 60), ("bre", "Werder Bremen", 62), ("dar", "SV Darmstadt", 55)
        ]
        
        for codigo, nombre, nivel_base in equipos_bundesliga:
            plantilla_generica = self._generar_plantilla_generica(nivel_base)
            self._crear_equipo(codigo, nombre, "Bundesliga", plantilla_generica)
        
        # LIGUE 1
        equipos_ligue1 = [
            ("psg", "Paris Saint-Germain", 85), ("mar", "Marseille", 72), ("oly", "Lyon", 74),
            ("asm", "AS Monaco", 73), ("ren", "Rennes", 69), ("lil", "Lille", 71),
            ("nic", "Nice", 70), ("len", "Lens", 68), ("str", "Strasbourg", 65),
            ("nan", "Nantes", 62), ("rei", "Reims", 63), ("mtp", "Montpellier", 60),
            ("tou", "Toulouse", 61), ("lor", "Lorient", 57), ("brest", "Brest", 59),
            ("cle", "Clermont", 56), ("metz", "Metz", 58), ("hav", "Le Havre", 54)
        ]
        
        for codigo, nombre, nivel_base in equipos_ligue1:
            plantilla_generica = self._generar_plantilla_generica(nivel_base)
            self._crear_equipo(codigo, nombre, "Ligue 1", plantilla_generica)
        
        # PRIMEIRA LIGA
        equipos_primeira = [
            ("ben", "Benfica", 78), ("por", "Porto", 77), ("spo", "Sporting CP", 75),
            ("bra", "Braga", 70), ("vit", "Vitoria Guimaraes", 67), ("gui", "Gil Vicente", 62),
            ("avo", "Rio Ave", 60), ("mor", "Moreirense", 58), ("ton", "Tondela", 55),
            ("rio", "Rio Ave", 57), ("csmf", "Casa Pia", 59), ("bel", "Belenenses", 56),
            ("port", "Portimonense", 58), ("san", "Santa Clara", 57), ("far", "Famalicao", 54),
            ("aro", "Arouca", 56), ("viz", "Vizela", 53), ("est", "Estoril", 60)
        ]
        
        for codigo, nombre, nivel_base in equipos_primeira:
            plantilla_generica = self._generar_plantilla_generica(nivel_base)
            self._crear_equipo(codigo, nombre, "Primeira Liga", plantilla_generica)
        
        # EREDIVISIE
        equipos_eredivisie = [
            ("aja", "Ajax", 73), ("psv", "PSV Eindhoven", 76), ("fey", "Feyenoord", 72),
            ("az", "AZ Alkmaar", 69), ("twn", "FC Twente", 66), ("vit_nl", "Vitesse", 63),
            ("uti", "FC Utrecht", 61), ("gro", "FC Groningen", 58), ("her_nl", "Heracles", 60),
            ("wil", "Willem II", 57), ("hee", "SC Heerenveen", 59), ("pec", "PEC Zwolle", 56),
            ("for", "Fortuna Sittard", 58), ("spa_nl", "Sparta Rotterdam", 57), ("goe", "Go Ahead Eagles", 55),
            ("cam", "Cambuur", 54), ("nec", "NEC Nijmegen", 59), ("almc", "Almere City", 52)
        ]
        
        for codigo, nombre, nivel_base in equipos_eredivisie:
            plantilla_generica = self._generar_plantilla_generica(nivel_base)
            self._crear_equipo(codigo, nombre, "Eredivisie", plantilla_generica)
        
        # Crear PSG con jugadores reales
        self._crear_equipo("psg", "Paris Saint-Germain", "Ligue 1", [
            ("Donnarumma", "POR", 88), ("Hakimi", "DEF", 86), ("Marquinhos", "DEF", 87),
            ("Skriniar", "DEF", 84), ("Mendes", "DEF", 79), ("Vitinha", "MED", 82),
            ("Verratti", "MED", 87), ("Ruiz", "MED", 80), ("Dembele", "DEL", 86),
            ("Mbappe", "DEL", 95), ("Ramos", "DEL", 83)
        ])
    
    def _generar_plantilla_generica(self, nivel_base: int) -> List[tuple]:
        """Genera una plantilla genérica basada en un nivel base"""
        plantilla = []
        posiciones = [
            ("GK", "POR", 1), ("RB", "DEF", 1), ("CB1", "DEF", 1), ("CB2", "DEF", 1),
            ("LB", "DEF", 1), ("CM1", "MED", 1), ("CM2", "MED", 1), ("CAM", "MED", 1),
            ("RW", "DEL", 1), ("ST", "DEL", 1), ("LW", "DEL", 1)
        ]
        
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
    
    def obtener_candidatos_balon_oro(self, limite: int = 20) -> List[tuple]:
        """Obtiene los candidatos al Balón de Oro"""
        jugadores_con_puntos = []
        for jugador in self.jugadores.values():
            puntos = jugador.calcular_puntos_balon_oro()
            if puntos > 0:
                jugadores_con_puntos.append((jugador, puntos))
        
        return sorted(jugadores_con_puntos, key=lambda x: x[1], reverse=True)[:limite]

# Instancia global de la base de datos
base_datos = BaseDatos()