import random as rm

gol1 = 0
gol2 = 0
equipos = {
    "mc": 85,
    "liv": 75,
    "ars": 60,
    "che": 74,
    "mu": 50,
    "tot": 65,
    "new": 55,
    "avl": 50,
    "wes": 45,
    "bha": 40,
    "wol": 45,
    "cry": 40,
    "ful": 40,
    "eve": 35,
    "bur": 30,
    "not": 25,
    "bou": 35,
    "shf": 25,
    "lut": 20,
    "lei": 45,

    # La Liga
    "rmd": 82,
    "bar": 75,
    "atl": 75,
    "sev": 50,
    "bet": 40,
    "rsoc": 70,
    "vil": 45,
    "val": 55,
    "ath": 50,
    "osa": 45,
    "get": 40,
    "ray": 35,
    "cel": 25,
    "cad": 30,
    "gra": 25,
    "las": 35,
    "alm": 30,
    "mal": 40,
    "alv": 20,
    "gir": 30,

    # Serie A
    "juv": 79,
    "int": 75,
    "mil": 65,
    "nap": 45,
    "rom": 50,
    "laz": 60,
    "ata": 80,
    "fio": 55,
    "tor": 45,
    "udi": 35,
    "gen": 35,
    "emp": 30,
    "lec": 25,
    "ver": 40,
    "cal": 30,
    "fro": 25,
    "sas": 35,
    "sam": 30,
    "mon": 40,
    "bol": 20,

    # Bundesliga
    "bay": 84,
    "bvb": 65,
    "rbz": 70,
    "lev": 45,
    "fra": 35,
    "fre": 35,
    "wol_de": 40,
    "bmg": 55,
    "uni": 50,
    "stu": 20,
    "may": 35,
    "hof": 30,
    "aug": 25,
    "her": 30,
    "boc": 25,
    "col": 30,
    "bre": 30,
    "dar": 20,

    # Ligue 1
    "psg": 70,
    "mar": 30,
    "oly": 60,
    "asm": 40,
    "ren": 35,
    "lil": 40,
    "nic": 45,
    "len": 35,
    "str": 30,
    "nan": 25,
    "rei": 30,
    "mtp": 25,
    "tou": 30,
    "lor": 20,
    "brest": 25,
    "cle": 20,
    "metz": 25,
    "hav": 15,

    # Primeira Liga
    "ben": 70,
    "por": 65,
    "spo": 45,
    "bra": 40,
    "vit": 35,
    "gui": 30,
    "avo": 25,
    "mor": 25,
    "ton": 20,
    "rio": 25,
    "csmf": 30,
    "bel": 20,
    "port": 25,
    "san": 20,
    "far": 15,
    "aro": 20,
    "viz": 15,
    "est": 25,

    # Eredivisie
    "aja": 25,
    "psv": 45,
    "fey": 30,
    "az": 35,
    "twn": 30,
    "vit_nl": 25,
    "uti": 20,
    "gro": 20,
    "her_nl": 25,
    "wil": 15,
    "hee": 20,
    "pec": 15,
    "for": 20,
    "spa_nl": 15,
    "goe": 10,
    "cam": 15,
    "nec": 20,
    "almc": 25,
}

while True:
    equipo1 = input("Ingrese el primer equipo: ")
    equipo2 = input("Ingrese el segundo equipo: ")
    
    if equipo1 not in equipos:
        print(f"Equipo '{equipo1}' no encontrado")
        continue
    if equipo2 not in equipos:
        print(f"Equipo '{equipo2}' no encontrado")
        continue
        
    nivel1 = equipos[equipo1]
    nivel2 = equipos[equipo2]
    level = nivel1 - nivel2
    sumalevel = nivel1 + nivel2
    
    for i in range(0, 90):
        prob = rm.randint(1, 200)
        if prob > 195:
            prob2 = rm.randint(0, sumalevel)
            if prob2 <= nivel1:
                gol1 = gol1 + 1
            else:
                gol2 = gol2 + 1
                
    print(equipo1, gol1, " : ", gol2, equipo2)
    gol1 = 0
    gol2 = 0