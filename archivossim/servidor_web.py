from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime
from typing import Dict, List, Tuple
import random as rm
from collections import defaultdict

# Importar las funciones del simulador
import sys
sys.path.append('archivossim')
from base_datos import base_datos
from simuladorcompleto import (
    simular_partido_con_jugadores,
    simular_liga_con_jugadores,
    simular_champions_league,
    simular_europa_league,
    simular_conference_league,
    obtener_clasificados_europeos
)

class SimuladorHTTPHandler(BaseHTTPRequestHandler):
    
    def _set_headers(self, content_type='application/json'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers()
    
    def do_GET(self):
        if self.path == '/':
            self._serve_html()
        elif self.path == '/api/equipos':
            self._get_equipos()
        elif self.path == '/api/ligas':
            self._get_ligas()
        elif self.path.startswith('/api/equipo/'):
            equipo_codigo = self.path.split('/')[-1]
            self._get_equipo_detalles(equipo_codigo)
        elif self.path == '/api/jugadores/goleadores':
            self._get_top_goleadores()
        elif self.path == '/api/jugadores/asistentes':
            self._get_top_asistentes()
        elif self.path == '/api/jugadores/balon-oro':
            self._get_candidatos_balon_oro()
        else:
            self.send_error(404)
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b''
        
        data = {}
        if post_data:
            try:
                data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                data = {}

        if self.path == '/api/simular-partido':
            self._simular_partido(data)
        elif self.path == '/api/simular-liga':
            self._simular_liga(data)
        elif self.path == '/api/simular-temporada':
            self._simular_temporada_completa()
        elif self.path == '/api/reset':
            self._reset_estadisticas()
        else:
            self.send_error(404)

    
    def _serve_html(self):
        """Sirve la interfaz HTML"""
        self._set_headers('text/html')
        html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚽ Simulador de Fútbol Europeo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }
        
        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .tab {
            padding: 15px 30px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
            border-bottom: 3px solid transparent;
        }
        
        .tab:hover {
            color: #667eea;
        }
        
        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .card h3 {
            color: #667eea;
            margin-bottom: 15px;
        }
        
        select, input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 15px;
            transition: border-color 0.3s;
        }
        
        select:focus, input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
            width: 100%;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .resultado {
            background: white;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
        }
        
        .resultado h4 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .marcador {
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
            text-align: center;
            color: #333;
        }
        
        .tabla {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .tabla th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
        }
        
        .tabla td {
            padding: 10px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .tabla tr:hover {
            background: #f8f9fa;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #667eea;
            font-size: 18px;
        }
        
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        @media (max-width: 768px) {
            .grid-2 {
                grid-template-columns: 1fr;
            }
        }
        
        .evento {
            padding: 8px;
            margin: 5px 0;
            background: #f0f0f0;
            border-radius: 5px;
        }
        
        .evento.gol {
            background: #d4edda;
            border-left: 3px solid #28a745;
        }
        
        .evento.tarjeta-amarilla {
            background: #fff3cd;
            border-left: 3px solid #ffc107;
        }
        
        .evento.tarjeta-roja {
            background: #f8d7da;
            border-left: 3px solid #dc3545;
        }
        
        .medalla {
            font-size: 20px;
            margin-right: 5px;
        }
        
        .progress {
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 20px 0;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚽ Simulador de Fútbol Europeo</h1>
            <p>Simula partidos, ligas y temporadas completas con estadísticas detalladas</p>
        </header>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('partido')">🎮 Partido</button>
            <button class="tab" onclick="showTab('liga')">🏆 Liga</button>
            <button class="tab" onclick="showTab('temporada')">🌍 Temporada Completa</button>
            <button class="tab" onclick="showTab('estadisticas')">📊 Estadísticas</button>
        </div>
        
        <!-- TAB: Partido Individual -->
        <div id="tab-partido" class="tab-content active">
            <div class="card">
                <h3>🎮 Simular Partido Individual</h3>
                <select id="equipo1-partido">
                    <option value="">Selecciona Equipo 1</option>
                </select>
                <select id="equipo2-partido">
                    <option value="">Selecciona Equipo 2</option>
                </select>
                <button onclick="simularPartido()">⚽ Simular Partido</button>
            </div>
            <div id="resultado-partido"></div>
        </div>
        
        <!-- TAB: Liga -->
        <div id="tab-liga" class="tab-content">
            <div class="card">
                <h3>🏆 Simular Liga Completa</h3>
                <select id="liga-select">
                    <option value="">Selecciona una Liga</option>
                    <option value="Premier League">🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League</option>
                    <option value="La Liga">🇪🇸 La Liga</option>
                    <option value="Serie A">🇮🇹 Serie A</option>
                    <option value="Bundesliga">🇩🇪 Bundesliga</option>
                    <option value="Ligue 1">🇫🇷 Ligue 1</option>
                    <option value="Primeira Liga">🇵🇹 Primeira Liga</option>
                    <option value="Eredivisie">🇳🇱 Eredivisie</option>
                </select>
                <button onclick="simularLiga()">🏆 Simular Liga</button>
            </div>
            <div id="resultado-liga"></div>
        </div>
        
        <!-- TAB: Temporada Completa -->
        <div id="tab-temporada" class="tab-content">
            <div class="card">
                <h3>🌍 Simular Temporada Completa</h3>
                <p>Simula todas las ligas europeas + Champions, Europa y Conference League</p>
                <button onclick="simularTemporada()">🚀 Iniciar Simulación Completa</button>
                <button onclick="resetEstadisticas()" style="background: #dc3545; margin-top: 10px;">🔄 Reset Estadísticas</button>
            </div>
            <div id="progress-container" style="display: none;">
                <div class="progress">
                    <div id="progress-bar" class="progress-bar">0%</div>
                </div>
                <p id="progress-text" style="text-align: center; color: #667eea;"></p>
            </div>
            <div id="resultado-temporada"></div>
        </div>
        
        <!-- TAB: Estadísticas -->
        <div id="tab-estadisticas" class="tab-content">
            <div class="grid-2">
                <div class="card">
                    <h3>🥇 Top Goleadores</h3>
                    <button onclick="cargarGoleadores()">📊 Ver Goleadores</button>
                    <div id="lista-goleadores"></div>
                </div>
                <div class="card">
                    <h3>🎯 Top Asistentes</h3>
                    <button onclick="cargarAsistentes()">📊 Ver Asistentes</button>
                    <div id="lista-asistentes"></div>
                </div>
            </div>
            <div class="card">
                <h3>🏆 Candidatos Balón de Oro</h3>
                <button onclick="cargarBalonOro()">📊 Ver Candidatos</button>
                <div id="lista-balon-oro"></div>
            </div>
        </div>
    </div>
    
    <script>
        // API Base URL
        const API_URL = '';
        
        // Cargar equipos al iniciar
        window.onload = async () => {
            await cargarEquipos();
        };
        
        async function cargarEquipos() {
            try {
                const response = await fetch(`${API_URL}/api/equipos`);
                const equipos = await response.json();
                
                const select1 = document.getElementById('equipo1-partido');
                const select2 = document.getElementById('equipo2-partido');
                
                equipos.forEach(equipo => {
                    const option1 = new Option(`${equipo.nombre} (${equipo.nivel})`, equipo.codigo);
                    const option2 = new Option(`${equipo.nombre} (${equipo.nivel})`, equipo.codigo);
                    select1.add(option1);
                    select2.add(option2);
                });
            } catch (error) {
                console.error('Error cargando equipos:', error);
            }
        }
        
        function showTab(tabName) {
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(`tab-${tabName}`).classList.add('active');
        }
        
        async function simularPartido() {
            const equipo1 = document.getElementById('equipo1-partido').value;
            const equipo2 = document.getElementById('equipo2-partido').value;
            
            if (!equipo1 || !equipo2) {
                alert('Selecciona ambos equipos');
                return;
            }
            
            if (equipo1 === equipo2) {
                alert('Selecciona equipos diferentes');
                return;
            }
            
            const resultadoDiv = document.getElementById('resultado-partido');
            resultadoDiv.innerHTML = '<div class="loading">⚽ Simulando partido...</div>';
            
            try {
                const response = await fetch(`${API_URL}/api/simular-partido`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({equipo1, equipo2})
                });
                
                const data = await response.json();
                
                let html = `
                    <div class="resultado">
                        <h4>🏟️ Resultado del Partido</h4>
                        <div class="marcador">
                            ${data.equipo1_nombre} ${data.goles1} - ${data.goles2} ${data.equipo2_nombre}
                        </div>
                        <h4>📝 Eventos del Partido</h4>
                `;
                
                data.eventos.forEach(evento => {
                    let clase = '';
                    let icono = '';
                    if (evento.tipo === 'gol') {
                        clase = 'gol';
                        icono = '⚽';
                    } else if (evento.tipo === 'tarjeta_amarilla') {
                        clase = 'tarjeta-amarilla';
                        icono = '🟨';
                    } else if (evento.tipo === 'tarjeta_roja') {
                        clase = 'tarjeta-roja';
                        icono = '🟥';
                    }
                    
                    html += `<div class="evento ${clase}">`;
                    html += `${icono} Min ${evento.minuto}: `;
                    
                    if (evento.tipo === 'gol') {
                        html += `¡GOL de ${evento.goleador}!`;
                        if (evento.asistente) {
                            html += ` (Asistencia: ${evento.asistente})`;
                        }
                    } else if (evento.tipo === 'tarjeta_amarilla') {
                        html += `Tarjeta amarilla para ${evento.jugador}`;
                    } else if (evento.tipo === 'tarjeta_roja') {
                        html += `Tarjeta roja para ${evento.jugador}`;
                    }
                    
                    html += `</div>`;
                });
                
                html += '</div>';
                resultadoDiv.innerHTML = html;
            } catch (error) {
                resultadoDiv.innerHTML = '<div class="resultado">❌ Error simulando partido</div>';
            }
        }
        
        async function simularLiga() {
            const liga = document.getElementById('liga-select').value;
            if (!liga) {
                alert('Selecciona una liga');
                return;
            }
            
            const resultadoDiv = document.getElementById('resultado-liga');
            resultadoDiv.innerHTML = '<div class="loading">🏆 Simulando liga completa...</div>';
            
            try {
                const response = await fetch(`${API_URL}/api/simular-liga`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({liga})
                });
                
                const data = await response.json();
                
                let html = `
                    <div class="resultado">
                        <h4>🏆 TABLA FINAL - ${data.liga}</h4>
                        <table class="tabla">
                            <thead>
                                <tr>
                                    <th>Pos</th>
                                    <th>Equipo</th>
                                    <th>Pts</th>
                                    <th>PJ</th>
                                    <th>GF</th>
                                    <th>GC</th>
                                    <th>DG</th>
                                </tr>
                            </thead>
                            <tbody>
                `;
                
                data.tabla.forEach((equipo, index) => {
                    let medalla = '';
                    if (index === 0) medalla = '🥇';
                    else if (index === 1) medalla = '🥈';
                    else if (index === 2) medalla = '🥉';
                    
                    html += `
                        <tr>
                            <td>${medalla} ${index + 1}</td>
                            <td>${equipo.nombre}</td>
                            <td><strong>${equipo.puntos}</strong></td>
                            <td>${equipo.partidos}</td>
                            <td>${equipo.gf}</td>
                            <td>${equipo.gc}</td>
                            <td>${equipo.gd >= 0 ? '+' : ''}${equipo.gd}</td>
                        </tr>
                    `;
                });
                
                html += `
                            </tbody>
                        </table>
                    </div>
                `;
                
                resultadoDiv.innerHTML = html;
            } catch (error) {
                resultadoDiv.innerHTML = '<div class="resultado">❌ Error simulando liga</div>';
            }
        }
        
        async function simularTemporada() {
            const resultadoDiv = document.getElementById('resultado-temporada');
            const progressContainer = document.getElementById('progress-container');
            const progressBar = document.getElementById('progress-bar');
            const progressText = document.getElementById('progress-text');
            
            resultadoDiv.innerHTML = '';
            progressContainer.style.display = 'block';
            progressBar.style.width = '0%';
            progressBar.textContent = '0%';
            progressText.textContent = 'Iniciando simulación...';
            
            try {
                const response = await fetch(`${API_URL}/api/simular-temporada`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'}
                });
                
                const data = await response.json();
                
                progressBar.style.width = '100%';
                progressBar.textContent = '100%';
                progressText.textContent = '¡Simulación completada!';
                
                let html = `
                    <div class="resultado">
                        <h4>🏆 RESUMEN DE LA TEMPORADA</h4>
                        
                        <h4>📊 Campeones de Liga:</h4>
                `;
                
                for (const [liga, campeon] of Object.entries(data.campeones_liga)) {
                    html += `<p>🏆 ${liga}: <strong>${campeon}</strong></p>`;
                }
                
                html += `
                        <h4>🌍 Campeones Europeos:</h4>
                        <p>🏆 Champions League: <strong>${data.campeon_champions}</strong></p>
                        <p>🏅 Europa League: <strong>${data.campeon_europa}</strong></p>
                        <p>🎯 Conference League: <strong>${data.campeon_conference}</strong></p>
                        
                        <h4>⚽ Top 5 Goleadores:</h4>
                `;
                
                data.top_goleadores.slice(0, 5).forEach((jugador, index) => {
                    const medalla = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '';
                    html += `<p>${medalla} ${jugador.nombre} (${jugador.equipo}) - ${jugador.goles} goles</p>`;
                });
                
                html += '</div>';
                resultadoDiv.innerHTML = html;
                
                setTimeout(() => {
                    progressContainer.style.display = 'none';
                }, 3000);
                
            } catch (error) {
                resultadoDiv.innerHTML = '<div class="resultado">❌ Error simulando temporada</div>';
                progressContainer.style.display = 'none';
            }
        }
        
        async function resetEstadisticas() {
            if (!confirm('¿Estás seguro de resetear todas las estadísticas?')) {
                return;
            }
            
            try {
                await fetch(`${API_URL}/api/reset`, {method: 'POST'});
                alert('✅ Estadísticas reseteadas correctamente');
            } catch (error) {
                alert('❌ Error reseteando estadísticas');
            }
        }
        
        async function cargarGoleadores() {
            const div = document.getElementById('lista-goleadores');
            div.innerHTML = '<div class="loading">Cargando...</div>';
            
            try {
                const response = await fetch(`${API_URL}/api/jugadores/goleadores`);
                const jugadores = await response.json();
                
                let html = '<table class="tabla"><thead><tr><th>Pos</th><th>Jugador</th><th>Equipo</th><th>Goles</th></tr></thead><tbody>';
                
                jugadores.forEach((j, index) => {
                    const medalla = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '';
                    html += `<tr><td>${medalla} ${index + 1}</td><td>${j.nombre}</td><td>${j.equipo}</td><td><strong>${j.goles}</strong></td></tr>`;
                });
                
                html += '</tbody></table>';
                div.innerHTML = html;
            } catch (error) {
                div.innerHTML = '<p>❌ Error cargando datos</p>';
            }
        }
        
        async function cargarAsistentes() {
            const div = document.getElementById('lista-asistentes');
            div.innerHTML = '<div class="loading">Cargando...</div>';
            
            try {
                const response = await fetch(`${API_URL}/api/jugadores/asistentes`);
                const jugadores = await response.json();
                
                let html = '<table class="tabla"><thead><tr><th>Pos</th><th>Jugador</th><th>Equipo</th><th>Asist</th></tr></thead><tbody>';
                
                jugadores.forEach((j, index) => {
                    const medalla = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '';
                    html += `<tr><td>${medalla} ${index + 1}</td><td>${j.nombre}</td><td>${j.equipo}</td><td><strong>${j.asistencias}</strong></td></tr>`;
                });
                
                html += '</tbody></table>';
                div.innerHTML = html;
            } catch (error) {
                div.innerHTML = '<p>❌ Error cargando datos</p>';
            }
        }
        
        async function cargarBalonOro() {
            const div = document.getElementById('lista-balon-oro');
            div.innerHTML = '<div class="loading">Cargando...</div>';
            
            try {
                const response = await fetch(`${API_URL}/api/jugadores/balon-oro`);
                const candidatos = await response.json();
                
                let html = '<table class="tabla"><thead><tr><th>Pos</th><th>Jugador</th><th>Equipo</th><th>Goles</th><th>Asist</th><th>Puntos</th></tr></thead><tbody>';
                
                candidatos.forEach((c, index) => {
                    const medalla = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '';
                    html += `<tr><td>${medalla} ${index + 1}</td><td>${c.nombre}</td><td>${c.equipo}</td><td>${c.goles}</td><td>${c.asistencias}</td><td><strong>${c.puntos.toFixed(2)}</strong></td></tr>`;
                });
                
                html += '</tbody></table>';
                div.innerHTML = html;
            } catch (error) {
                div.innerHTML = '<p>❌ Error cargando datos</p>';
            }
        }
    </script>
</body>
</html>'''
        self.wfile.write(html.encode())
    
    def _get_equipos(self):
        """Obtiene lista de todos los equipos"""
        self._set_headers()
        equipos = []
        for codigo, equipo in base_datos.equipos.items():
            equipos.append({
                'codigo': codigo,
                'nombre': equipo.nombre,
                'liga': equipo.liga,
                'nivel': equipo.calcular_nivel_equipo()
            })
        equipos.sort(key=lambda x: x['nivel'], reverse=True)
        self.wfile.write(json.dumps(equipos).encode())
    
    def _get_ligas(self):
        """Obtiene lista de ligas"""
        self._set_headers()
        ligas = base_datos.obtener_ligas()
        self.wfile.write(json.dumps(ligas).encode())
    
    def _get_equipo_detalles(self, codigo):
        """Obtiene detalles de un equipo específico"""
        self._set_headers()
        equipo = base_datos.obtener_equipo(codigo)
        if equipo:
            data = {
                'codigo': codigo,
                'nombre': equipo.nombre,
                'liga': equipo.liga,
                'nivel': equipo.calcular_nivel_equipo(),
                'jugadores': [
                    {
                        'nombre': j.nombre,
                        'posicion': j.posicion,
                        'nivel': j.nivel,
                        'goles': j.goles,
                        'asistencias': j.asistencias
                    } for j in equipo.jugadores
                ]
            }
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_error(404)
    
    def _simular_partido(self, data):
        """Simula un partido entre dos equipos"""
        self._set_headers()
        equipo1 = data.get('equipo1')
        equipo2 = data.get('equipo2')
        
        goles1, goles2, eventos = simular_partido_con_jugadores(equipo1, equipo2)
        
        team1 = base_datos.obtener_equipo(equipo1)
        team2 = base_datos.obtener_equipo(equipo2)
        
        resultado = {
            'equipo1': equipo1,
            'equipo2': equipo2,
            'equipo1_nombre': team1.nombre,
            'equipo2_nombre': team2.nombre,
            'goles1': goles1,
            'goles2': goles2,
            'eventos': eventos
        }
        
        self.wfile.write(json.dumps(resultado).encode())
    
    def _simular_liga(self, data):
        """Simula una liga completa"""
        self._set_headers()
        nombre_liga = data.get('liga')
        
        ligas = base_datos.obtener_ligas()
        if nombre_liga not in ligas:
            self.send_error(404)
            return
        
        equipos_liga = ligas[nombre_liga]
        tabla = simular_liga_con_jugadores(nombre_liga, equipos_liga)
        
        resultado = {
            'liga': nombre_liga,
            'tabla': [
                {
                    'codigo': codigo,
                    'nombre': base_datos.obtener_equipo(codigo).nombre,
                    'puntos': stats['puntos'],
                    'partidos': stats['partidos'],
                    'gf': stats['gf'],
                    'gc': stats['gc'],
                    'gd': stats['gd']
                }
                for codigo, stats in tabla
            ]
        }
        
        self.wfile.write(json.dumps(resultado).encode())
    
    def _simular_temporada_completa(self):
        """Simula una temporada completa"""
        self._set_headers()
        
        # Reset estadísticas
        base_datos.reset_estadisticas_temporada()
        
        # Simular todas las ligas
        ligas = base_datos.obtener_ligas()
        resultados_ligas = {}
        campeones_liga = {}
        
        for nombre_liga, equipos_dict in ligas.items():
            tabla = simular_liga_con_jugadores(nombre_liga, equipos_dict)
            resultados_ligas[nombre_liga] = tabla
            if tabla:
                campeones_liga[nombre_liga] = base_datos.obtener_equipo(tabla[0][0]).nombre
        
        # Obtener clasificados europeos
        champions, europa, conference = obtener_clasificados_europeos(resultados_ligas)
        
        # Simular competiciones europeas (necesitamos crear archivos temporales)
        import io
        
        archivo_temp = io.StringIO()
        campeon_champions = simular_champions_league(champions, archivo_temp)
        
        archivo_temp = io.StringIO()
        campeon_europa = simular_europa_league(europa, archivo_temp)
        
        archivo_temp = io.StringIO()
        campeon_conference = simular_conference_league(conference, archivo_temp)
        
        # Obtener estadísticas
        top_goleadores = base_datos.obtener_top_goleadores(10)
        top_asistentes = base_datos.obtener_top_asistentes(10)
        candidatos_balon = base_datos.obtener_candidatos_balon_oro(10)
        
        resultado = {
            'campeones_liga': campeones_liga,
            'campeon_champions': base_datos.obtener_equipo(campeon_champions).nombre if campeon_champions else '',
            'campeon_europa': base_datos.obtener_equipo(campeon_europa).nombre if campeon_europa else '',
            'campeon_conference': base_datos.obtener_equipo(campeon_conference).nombre if campeon_conference else '',
            'top_goleadores': [
                {
                    'nombre': j.nombre,
                    'equipo': base_datos.obtener_equipo(j.equipo).nombre,
                    'goles': j.goles,
                    'asistencias': j.asistencias
                }
                for j in top_goleadores
            ],
            'top_asistentes': [
                {
                    'nombre': j.nombre,
                    'equipo': base_datos.obtener_equipo(j.equipo).nombre,
                    'asistencias': j.asistencias,
                    'goles': j.goles
                }
                for j in top_asistentes
            ],
            'candidatos_balon_oro': [
                {
                    'nombre': j.nombre,
                    'equipo': base_datos.obtener_equipo(j.equipo).nombre,
                    'goles': j.goles,
                    'asistencias': j.asistencias,
                    'puntos': puntos
                }
                for j, puntos in candidatos_balon
            ]
        }
        
        self.wfile.write(json.dumps(resultado).encode())
    
    def _reset_estadisticas(self):
        """Resetea todas las estadísticas"""
        self._set_headers()
        base_datos.reset_estadisticas_temporada()
        self.wfile.write(json.dumps({'status': 'ok'}).encode())
    
    def _get_top_goleadores(self):
        """Obtiene top goleadores"""
        self._set_headers()
        top = base_datos.obtener_top_goleadores(20)
        resultado = [
            {
                'nombre': j.nombre,
                'equipo': j.equipo.upper(),
                'goles': j.goles,
                'partidos': j.partidos_jugados
            }
            for j in top
        ]
        self.wfile.write(json.dumps(resultado).encode())
    
    def _get_top_asistentes(self):
        """Obtiene top asistentes"""
        self._set_headers()
        top = base_datos.obtener_top_asistentes(20)
        resultado = [
            {
                'nombre': j.nombre,
                'equipo': j.equipo.upper(),
                'asistencias': j.asistencias,
                'partidos': j.partidos_jugados
            }
            for j in top
        ]
        self.wfile.write(json.dumps(resultado).encode())
    
    def _get_candidatos_balon_oro(self):
        """Obtiene candidatos al Balón de Oro"""
        self._set_headers()
        candidatos = base_datos.obtener_candidatos_balon_oro(20)
        resultado = [
            {
                'nombre': j.nombre,
                'equipo': j.equipo.upper(),
                'goles': j.goles,
                'asistencias': j.asistencias,
                'puntos': puntos
            }
            for j, puntos in candidatos
        ]
        self.wfile.write(json.dumps(resultado).encode())
    
    def log_message(self, format, *args):
        """Sobrescribir para logs más limpios"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8000):
    """Inicia el servidor HTTP"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimuladorHTTPHandler)
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  ⚽ SIMULADOR DE FÚTBOL EUROPEO - SERVIDOR WEB ⚽        ║
╚══════════════════════════════════════════════════════════╝

🌐 Servidor iniciado en: http://localhost:{port}
📊 Base de datos cargada: {len(base_datos.equipos)} equipos, {len(base_datos.jugadores)} jugadores

🎮 Funcionalidades disponibles:
   • Simular partidos individuales
   • Simular ligas completas
   • Simular temporada europea completa
   • Ver estadísticas de jugadores
   • Rankings: Goleadores, Asistentes, Balón de Oro

⚡ Presiona Ctrl+C para detener el servidor
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Servidor detenido correctamente")
        httpd.server_close()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Servidor web para el simulador de fútbol')
    parser.add_argument('--port', type=int, default=8000, help='Puerto del servidor (default: 8000)')
    
    args = parser.parse_args()
    run_server(args.port)