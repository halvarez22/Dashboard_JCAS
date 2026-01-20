"""
Dashboard Interactivo - Proyecto JCAS Chihuahua
Sistema de Generación de Energía Solar Fotovoltaica con BESS
MODO OSCURO PROFESIONAL
"""

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from openpyxl import load_workbook

# ============================================================================
# CONFIGURACIÓN Y ESTILOS - MODO OSCURO
# ============================================================================

# Colores para MODO OSCURO
COLORS_DARK = {
    'primary': '#00b4d8',        # Azul brillante
    'secondary': '#48cae4',      # Azul claro
    'accent': '#90e0ef',         # Azul muy claro
    'success': '#06ffa5',        # Verde neón
    'warning': '#ffd60a',        # Amarillo brillante
    'danger': '#ff006e',         # Rosa neón
    'info': '#00b4d8',           # Info azul
    'background': '#0d1117',     # Fondo oscuro GitHub
    'card': '#161b22',           # Card oscuro
    'card_border': '#30363d',    # Borde de card
    'text': '#c9d1d9',           # Texto claro
    'text_secondary': '#8b949e', # Texto secundario
    'plot_bg': '#0d1117',        # Fondo de gráficos
    'plot_paper': '#161b22',     # Papel de gráficos
    'grid': '#30363d'            # Grid de gráficos
}

# Función helper para aplicar tema oscuro a gráficos
def aplicar_tema_oscuro(fig):
    """Aplica el tema oscuro consistente a todas las figuras"""
    fig.update_layout(
        paper_bgcolor=COLORS_DARK['plot_paper'],
        plot_bgcolor=COLORS_DARK['plot_bg'],
        font={'color': COLORS_DARK['text'], 'family': 'Arial, sans-serif'},
        title_font={'size': 18, 'color': COLORS_DARK['primary']},
        xaxis=dict(
            gridcolor=COLORS_DARK['grid'],
            linecolor=COLORS_DARK['grid'],
            zerolinecolor=COLORS_DARK['grid']
        ),
        yaxis=dict(
            gridcolor=COLORS_DARK['grid'],
            linecolor=COLORS_DARK['grid'],
            zerolinecolor=COLORS_DARK['grid']
        )
    )
    return fig

# ============================================================================
# CARGA DE DATOS
# ============================================================================

def cargar_datos_excel():
    """Carga todos los datos del archivo Excel"""
    import os
    archivos = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~$')]
    archivo = archivos[0] if archivos else None
    
    if not archivo:
        raise FileNotFoundError("No se encontró el archivo Excel")
    
    datos = {}
    
    # Costo de energía
    df_costo = pd.read_excel(archivo, sheet_name='Costo $ energía', header=1)
    datos['costo_energia'] = df_costo
    
    # Energía kWh
    df_kwh = pd.read_excel(archivo, sheet_name='Energia kWh de Operacion', header=1)
    datos['energia_kwh'] = df_kwh
    
    # Volumen H2O
    df_volumen = pd.read_excel(archivo, sheet_name='Volumen H2O m3', header=1)
    datos['volumen_h2o'] = df_volumen
    
    # Resumen
    df_resumen = pd.read_excel(archivo, sheet_name='Resumen', header=1)
    datos['resumen'] = df_resumen
    
    # Producción energía
    df_produccion = pd.read_excel(archivo, sheet_name='Produccion energía eléctrica', header=3)
    datos['produccion'] = df_produccion
    
    # Modelo financiero
    df_modelo = pd.read_excel(archivo, sheet_name='Model $', header=1)
    datos['modelo_financiero'] = df_modelo
    
    return datos

# Cargar datos
print("Cargando datos del archivo Excel...")
datos = cargar_datos_excel()
print("Datos cargados exitosamente")

# Extraer datos específicos
jmas_list = ['Juarez', 'Chihuahua', 'Cuauhtemoc', 'Parral']
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# ============================================================================
# INICIALIZAR APLICACIÓN DASH
# ============================================================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],  # Tema oscuro
    title="Dashboard JCAS Chihuahua"
)

# Estilos CSS personalizados para modo oscuro
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #0d1117 !important;
                color: #c9d1d9 !important;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            .card {
                background-color: #161b22 !important;
                border: 1px solid #30363d !important;
                border-radius: 8px !important;
            }
            .card-header {
                background-color: #161b22 !important;
                border-bottom: 1px solid #30363d !important;
                color: #00b4d8 !important;
            }
            .dropdown {
                background-color: #161b22 !important;
            }
            .Select-control {
                background-color: #161b22 !important;
                border-color: #30363d !important;
            }
            hr {
                border-color: #30363d !important;
            }
            .nav-tabs .nav-link {
                color: #8b949e !important;
                background-color: #161b22 !important;
                border: 1px solid #30363d !important;
            }
            .nav-tabs .nav-link.active {
                color: #00b4d8 !important;
                background-color: #0d1117 !important;
                border-color: #30363d !important;
                border-bottom-color: transparent !important;
            }
            /* Ocultar banner de Plotly Cloud */
            ._dash-loading-callback {
                display: none !important;
            }
            .dash-graph .modebar-container .modebar-group:last-child {
                display: none !important;
            }
            /* Ocultar mensajes promocionales de Plotly */
            .plotly-notifier {
                display: none !important;
            }
            /* Ocultar el botón "Collaborate in Plotly Cloud" */
            .modebar-btn[data-title="Collaborate in Plotly Cloud"] {
                display: none !important;
            }
            /* Ocultar todos los avisos de extensiones */
            div[class*="extension-notifier"],
            div[class*="cloud-notifier"],
            div[class*="plotly-notifier"] {
                display: none !important;
            }
            /* Estilo para el enlace pai-b */
            .pai-b-link {
                position: relative;
                display: inline-block;
            }
            .pai-b-link:hover {
                color: #48cae4 !important;
                text-shadow: 0 0 8px #00b4d8;
                transform: scale(1.05);
            }
            .pai-b-link:hover strong {
                color: #48cae4 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ============================================================================
# LAYOUT DEL DASHBOARD
# ============================================================================

app.layout = dbc.Container([
    
    # ENCABEZADO CON LOGO
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        # Logo a la izquierda
                        dbc.Col([
                            html.Img(
                                src='/assets/logo-voltaic.png',
                                style={
                                    'height': '80px',
                                    'width': 'auto',
                                    'objectFit': 'contain',
                                    'maxWidth': '100%'
                                }
                            )
                        ], width=2, className="d-flex align-items-center justify-content-center"),
                        
                        # Títulos al centro
                        dbc.Col([
                            html.Div([
                                html.H1("Dashboard Ejecutivo - Proyecto JCAS Chihuahua", 
                                       className="text-center mb-2",
                                       style={
                                           'color': COLORS_DARK['primary'], 
                                           'fontWeight': 'bold', 
                                           'textShadow': f'0 0 10px {COLORS_DARK["primary"]}',
                                           'fontSize': '1.8rem',
                                           'lineHeight': '1.2'
                                       }),
                                html.H4("⚡ Sistema de Generación de Energía Solar Fotovoltaica con BESS",
                                       className="text-center mb-0",
                                       style={'color': COLORS_DARK['secondary'], 'fontSize': '1.1rem'})
                            ], className="d-flex flex-column justify-content-center h-100")
                        ], width=8),
                        
                        # Logo a la derecha (espacio para JCAS si lo tienes)
                        dbc.Col([
                            html.Div([
                                html.H5("JCAS", 
                                       style={
                                           'color': COLORS_DARK['accent'], 
                                           'fontWeight': 'bold',
                                           'textAlign': 'center'
                                       }),
                                html.P("Chihuahua", 
                                      style={
                                          'color': COLORS_DARK['text_secondary'],
                                          'textAlign': 'center',
                                          'fontSize': '0.9rem',
                                          'marginBottom': '0'
                                      })
                            ], className="d-flex flex-column justify-content-center h-100")
                        ], width=2, className="d-flex align-items-center justify-content-center")
                    ], className="align-items-center")
                ])
            ], className="shadow-lg mb-3", style={
                'background': f'linear-gradient(135deg, {COLORS_DARK["card"]} 0%, #1a1f2e 100%)',
                'borderLeft': f'5px solid {COLORS_DARK["primary"]}',
                'borderRight': f'5px solid {COLORS_DARK["accent"]}'
            })
        ])
    ], className="mb-4"),
    
    # KPIs PRINCIPALES
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("💰 Inversión Total", className="text-muted", style={'color': COLORS_DARK['text_secondary']}),
                    html.H3("$2,616 M MXN", style={'color': COLORS_DARK['primary'], 'fontWeight': 'bold'}),
                    html.P("$147.8 M USD", className="mb-0", style={'color': COLORS_DARK['text_secondary']})
                ])
            ], className="shadow-lg", style={'borderLeft': f'4px solid {COLORS_DARK["primary"]}'})
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("💵 Ahorro 15 años", className="text-muted", style={'color': COLORS_DARK['text_secondary']}),
                    html.H3("$11,055 M", style={'color': COLORS_DARK['success'], 'fontWeight': 'bold'}),
                    html.P("Ahorro neto", className="mb-0", style={'color': COLORS_DARK['text_secondary']})
                ])
            ], className="shadow-lg", style={'borderLeft': f'4px solid {COLORS_DARK["success"]}'})
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("📈 TIR Proyecto", className="text-muted", style={'color': COLORS_DARK['text_secondary']}),
                    html.H3("18.5%", style={'color': COLORS_DARK['accent'], 'fontWeight': 'bold'}),
                    html.P("Rentabilidad anual", className="mb-0", style={'color': COLORS_DARK['text_secondary']})
                ])
            ], className="shadow-lg", style={'borderLeft': f'4px solid {COLORS_DARK["accent"]}'})
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("☀️ Capacidad Solar", className="text-muted", style={'color': COLORS_DARK['text_secondary']}),
                    html.H3("150.24 MWp", style={'color': COLORS_DARK['warning'], 'fontWeight': 'bold'}),
                    html.P("+ 109.2 MWh BESS", className="mb-0", style={'color': COLORS_DARK['text_secondary']})
                ])
            ], className="shadow-lg", style={'borderLeft': f'4px solid {COLORS_DARK["warning"]}'})
        ], width=3),
    ], className="mb-4"),
    
    # SELECTOR DE JMAS
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🎯 Seleccione JMAS para análisis detallado:", className="mb-3", style={'color': COLORS_DARK['primary']}),
                    dcc.Dropdown(
                        id='jmas-selector',
                        options=[
                            {'label': '🏙️ JMAS Juárez', 'value': 'Juarez'},
                            {'label': '🏙️ JMAS Chihuahua', 'value': 'Chihuahua'},
                            {'label': '🏘️ JMAS Cuauhtémoc', 'value': 'Cuauhtemoc'},
                            {'label': '🏘️ JMAS Parral', 'value': 'Parral'},
                            {'label': '📊 CONSOLIDADO (Todas)', 'value': 'Todas'}
                        ],
                        value='Todas',
                        clearable=False,
                        style={
                            'fontSize': '14px',
                            'backgroundColor': COLORS_DARK['card'],
                            'color': COLORS_DARK['text']
                        }
                    )
                ])
            ], className="shadow-lg")
        ])
    ], className="mb-4"),
    
    # TABS PRINCIPALES
    dbc.Tabs([
        
        # TAB 1: DIAGNÓSTICO OPERATIVO
        dbc.Tab(label="📊 Diagnóstico Operativo", tab_id="tab-diagnostico", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("⚡ Consumo Energético Mensual (kWh)")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-energia-mensual')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("💲 Costo de Energía Mensual (MXN)")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-costo-mensual')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=6),
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("💧 Volumen de Agua Procesada (m³)")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-volumen-agua')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("📊 Eficiencia Energética (kWh/m³)")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-eficiencia')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=6),
            ]),
        ]),
        
        # TAB 2: DIMENSIONAMIENTO SOLAR
        dbc.Tab(label="☀️ Proyecto Solar", tab_id="tab-solar", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("⚡ Capacidad Instalada por JMAS")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-capacidad-solar')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("📐 Área Requerida por JMAS (hectáreas)")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-area-requerida')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=6),
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("☀️ Producción Energética Solar Mensual")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-produccion-solar')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=12),
            ]),
        ]),
        
        # TAB 3: ANÁLISIS FINANCIERO
        dbc.Tab(label="💰 Análisis Financiero", tab_id="tab-financiero", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("💼 Estructura de Inversión (CAPEX)")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-capex')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("🏦 Estructura de Financiamiento")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-financiamiento')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=6),
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("📈 Proyección Financiera (15 años)")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-proyeccion-financiera')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=12),
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("💵 Flujo de Caja Acumulado")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-flujo-caja')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=12),
            ]),
        ]),
        
        # TAB 4: COMPARATIVO SIN/CON PROYECTO
        dbc.Tab(label="📈 Comparativo de Escenarios", tab_id="tab-comparativo", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("⚖️ Comparativo: Sin Proyecto vs Con Proyecto")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-comparativo-escenarios')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=12),
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("💰 Ahorro Acumulado en el Tiempo")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-ahorro-acumulado')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=12),
            ]),
        ]),
        
        # TAB 5: IMPACTO AMBIENTAL
        dbc.Tab(label="🌿 Impacto Ambiental", tab_id="tab-ambiental", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("🌱 Reducción de Emisiones CO₂", style={'color': COLORS_DARK['text_secondary']}),
                            html.H2("159,458 ton/año", style={'color': COLORS_DARK['success'], 'fontWeight': 'bold'}),
                            html.P("Equivalente a plantar 7.3 millones de árboles", className="mb-0", style={'color': COLORS_DARK['text']})
                        ])
                    ], className="shadow-lg", style={'borderLeft': f'4px solid {COLORS_DARK["success"]}'})
                ], width=4),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("⚡ Energía Limpia Generada", style={'color': COLORS_DARK['text_secondary']}),
                            html.H2("318.9 GWh/año", style={'color': COLORS_DARK['info'], 'fontWeight': 'bold'}),
                            html.P("100% del consumo operativo", className="mb-0", style={'color': COLORS_DARK['text']})
                        ])
                    ], className="shadow-lg", style={'borderLeft': f'4px solid {COLORS_DARK["info"]}'})
                ], width=4),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("🌍 Contribución NDC México", style={'color': COLORS_DARK['text_secondary']}),
                            html.H2("100%", style={'color': COLORS_DARK['accent'], 'fontWeight': 'bold'}),
                            html.P("Alineado con Acuerdo de París", className="mb-0", style={'color': COLORS_DARK['text']})
                        ])
                    ], className="shadow-lg", style={'borderLeft': f'4px solid {COLORS_DARK["accent"]}'})
                ], width=4),
            ], className="mt-3 mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("🌱 Reducción de Emisiones CO₂ por JMAS")),
                        dbc.CardBody([
                            dcc.Graph(id='grafico-emisiones-co2')
                        ])
                    ], className="shadow-lg mt-3")
                ], width=12),
            ]),
        ]),
        
    ], id="tabs", active_tab="tab-diagnostico", className="mb-3"),
    
    # FOOTER
    html.Hr(style={'borderColor': COLORS_DARK['grid']}),
    html.Footer([
        html.Div([
            html.P("🌟 Dashboard Ejecutivo - Proyecto JCAS Chihuahua | Enero 2026 | Modo Oscuro Activado", 
                   className="text-center mb-2",
                   style={'color': COLORS_DARK['text_secondary'], 'fontSize': '0.95rem'}),
            html.P([
                html.Span("Powered by ", style={'color': COLORS_DARK['text_secondary']}),
                html.A(
                    html.Strong("pai-b", style={'color': COLORS_DARK['primary'], 'fontWeight': 'bold'}),
                    href="https://www.pai-b.com/",
                    target="_blank",
                    style={
                        'textDecoration': 'none',
                        'color': COLORS_DARK['primary'],
                        'transition': 'all 0.3s ease'
                    },
                    className="pai-b-link"
                ),
                html.Span(" (", style={'color': COLORS_DARK['text_secondary']}),
                html.Em("your Private Artificial Intelligence For Business", 
                       style={'color': COLORS_DARK['accent'], 'fontStyle': 'italic'}),
                html.Span(")", style={'color': COLORS_DARK['text_secondary']}),
                html.Br(),
                html.Span("© Todos los derechos reservados 2026", 
                         style={'color': COLORS_DARK['text_secondary'], 'fontSize': '0.85rem'})
            ], className="text-center mb-0")
        ])
    ])
    
], fluid=True, style={'backgroundColor': COLORS_DARK['background'], 'padding': '20px', 'minHeight': '100vh'})

# ============================================================================
# CALLBACKS - CORREGIDOS
# ============================================================================

@app.callback(
    Output('grafico-energia-mensual', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_energia_mensual(jmas_seleccionado):
    df = datos['energia_kwh']
    
    fig = go.Figure()
    
    if jmas_seleccionado == 'Todas':
        for jmas in jmas_list:
            fila = df[df.iloc[:, 0] == jmas]
            if not fila.empty:
                valores = fila.iloc[0, 1:13].values
                fig.add_trace(go.Bar(
                    name=f'JMAS {jmas}',
                    x=meses,
                    y=valores,
                ))
    else:
        fila = df[df.iloc[:, 0] == jmas_seleccionado]
        if not fila.empty:
            valores = fila.iloc[0, 1:13].values
            fig.add_trace(go.Bar(
                x=meses,
                y=valores,
                marker_color=COLORS_DARK['secondary'],
                name=f'JMAS {jmas_seleccionado}'
            ))
    
    fig.update_layout(
        title=f"Consumo Energético Mensual - {jmas_seleccionado}",
        xaxis_title="Mes",
        yaxis_title="kWh",
        hovermode='x unified',
        barmode='group'
    )
    
    return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-costo-mensual', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_costo_mensual(jmas_seleccionado):
    df = datos['costo_energia']
    
    fig = go.Figure()
    
    if jmas_seleccionado == 'Todas':
        for jmas in jmas_list:
            fila = df[df.iloc[:, 0] == jmas]
            if not fila.empty:
                valores = fila.iloc[0, 1:13].values / 1_000_000
                fig.add_trace(go.Scatter(
                    name=f'JMAS {jmas}',
                    x=meses,
                    y=valores,
                    mode='lines+markers',
                    line=dict(width=3)
                ))
    else:
        fila = df[df.iloc[:, 0] == jmas_seleccionado]
        if not fila.empty:
            valores = fila.iloc[0, 1:13].values / 1_000_000
            fig.add_trace(go.Scatter(
                x=meses,
                y=valores,
                mode='lines+markers',
                line=dict(color=COLORS_DARK['danger'], width=3),
                marker=dict(size=8),
                name=f'JMAS {jmas_seleccionado}'
            ))
    
    fig.update_layout(
        title=f"Costo de Energía Mensual - {jmas_seleccionado}",
        xaxis_title="Mes",
        yaxis_title="Millones MXN",
        hovermode='x unified'
    )
    
    return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-volumen-agua', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_volumen_agua(jmas_seleccionado):
    df = datos['volumen_h2o']
    
    fig = go.Figure()
    
    if jmas_seleccionado == 'Todas':
        for jmas in jmas_list:
            fila = df[df.iloc[:, 0] == jmas]
            if not fila.empty:
                valores = fila.iloc[0, 1:13].values / 1_000_000
                fig.add_trace(go.Bar(
                    name=f'JMAS {jmas}',
                    x=meses,
                    y=valores,
                ))
    else:
        fila = df[df.iloc[:, 0] == jmas_seleccionado]
        if not fila.empty:
            valores = fila.iloc[0, 1:13].values / 1_000_000
            fig.add_trace(go.Bar(
                x=meses,
                y=valores,
                marker_color=COLORS_DARK['info'],
                name=f'JMAS {jmas_seleccionado}'
            ))
    
    fig.update_layout(
        title=f"Volumen de Agua Procesada - {jmas_seleccionado}",
        xaxis_title="Mes",
        yaxis_title="Millones m³",
        hovermode='x unified',
        barmode='group'
    )
    
    return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-eficiencia', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_eficiencia(jmas_seleccionado):
    df_kwh = datos['energia_kwh']
    df_vol = datos['volumen_h2o']
    
    fig = go.Figure()
    
    jmas_a_mostrar = jmas_list if jmas_seleccionado == 'Todas' else [jmas_seleccionado]
    
    categorias = []
    eficiencias = []
    colores_barras = []
    
    for jmas in jmas_a_mostrar:
        fila_kwh = df_kwh[df_kwh.iloc[:, 0] == jmas]
        fila_vol = df_vol[df_vol.iloc[:, 0] == jmas]
        
        if not fila_kwh.empty and not fila_vol.empty and len(fila_kwh.columns) > 14 and len(fila_vol.columns) > 14:
            kwh_anual = fila_kwh.iloc[0, 14]
            m3_anual = fila_vol.iloc[0, 14]
            
            if pd.notna(kwh_anual) and pd.notna(m3_anual) and m3_anual != 0:
                eficiencia = float(kwh_anual) / float(m3_anual)
                
                categorias.append(f'JMAS {jmas}')
                eficiencias.append(eficiencia)
                
                if eficiencia < 1.0:
                    colores_barras.append(COLORS_DARK['success'])
                elif eficiencia < 1.5:
                    colores_barras.append(COLORS_DARK['warning'])
                else:
                    colores_barras.append(COLORS_DARK['danger'])
    
    if categorias and eficiencias:
        fig.add_trace(go.Bar(
            x=categorias,
            y=eficiencias,
            marker_color=colores_barras,
            text=[f'{e:.3f}' for e in eficiencias],
            textposition='outside'
        ))
    
    fig.update_layout(
        title="Eficiencia Energética (menor es mejor)",
        xaxis_title="JMAS",
        yaxis_title="kWh por m³ de agua",
        showlegend=False
    )
    
    return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-capacidad-solar', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_capacidad_solar(jmas_seleccionado):
    capacidades = {
        'Juarez': 65.37,
        'Chihuahua': 61.39,
        'Cuauhtemoc': 13.83,
        'Parral': 9.66
    }
    
    if jmas_seleccionado == 'Todas':
        fig = go.Figure(data=[
            go.Bar(
                x=list(capacidades.keys()),
                y=list(capacidades.values()),
                marker_color=[COLORS_DARK['accent'], COLORS_DARK['secondary'], COLORS_DARK['info'], COLORS_DARK['success']],
                text=[f'{v:.2f} MWp' for v in capacidades.values()],
                textposition='outside'
            )
        ])
    else:
        fig = go.Figure(data=[
            go.Bar(
                x=[jmas_seleccionado],
                y=[capacidades[jmas_seleccionado]],
                marker_color=COLORS_DARK['accent'],
                text=[f'{capacidades[jmas_seleccionado]:.2f} MWp'],
                textposition='outside',
                width=0.4
            )
        ])
    
    fig.update_layout(
        title="Capacidad Solar Instalada por JMAS",
        xaxis_title="JMAS",
        yaxis_title="Megawatts Pico (MWp)",
        showlegend=False
    )
    
    return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-area-requerida', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_area_requerida(jmas_seleccionado):
    areas = {
        'Juarez': 76.69,
        'Chihuahua': 72.01,
        'Cuauhtemoc': 16.22,
        'Parral': 11.33
    }
    
    if jmas_seleccionado == 'Todas':
        labels = list(areas.keys())
        values = list(areas.values())
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.4,
            marker=dict(colors=[COLORS_DARK['accent'], COLORS_DARK['secondary'], COLORS_DARK['info'], COLORS_DARK['success']]),
            textinfo='label+value',
            texttemplate='%{label}<br>%{value:.2f} ha'
        )])
        
        fig.update_layout(
            title="Distribución de Área Requerida",
            paper_bgcolor=COLORS_DARK['plot_paper'],
            font={'color': COLORS_DARK['text']}
        )
    else:
        fig = go.Figure(data=[
            go.Bar(
                x=[jmas_seleccionado],
                y=[areas[jmas_seleccionado]],
                marker_color=COLORS_DARK['info'],
                text=[f'{areas[jmas_seleccionado]:.2f} ha'],
                textposition='outside',
                width=0.4
            )
        ])
        
        fig.update_layout(
            title=f"Área Requerida - JMAS {jmas_seleccionado}",
            xaxis_title="JMAS",
            yaxis_title="Hectáreas",
            showlegend=False
        )
    
    return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-produccion-solar', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_produccion_solar(jmas_seleccionado):
    df = datos['produccion']
    
    if not df.empty and len(df.columns) > 5:
        meses_prod = df.iloc[:, 0].values
        # Convertir correctamente a número
        grid_kwh_raw = df.iloc[:, 5].values
        grid_kwh = []
        
        for val in grid_kwh_raw:
            try:
                grid_kwh.append(float(val) / 1000)  # Convertir a MWh
            except (ValueError, TypeError):
                grid_kwh.append(0)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=meses_prod,
            y=grid_kwh,
            mode='lines+markers',
            name='Producción Solar',
            line=dict(color=COLORS_DARK['warning'], width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor=f'rgba(255, 214, 10, 0.2)'
        ))
    else:
        fig = go.Figure()
    
    fig.update_layout(
        title="Producción Mensual de Energía Solar (1 MWp)",
        xaxis_title="Mes",
        yaxis_title="MWh",
        hovermode='x unified'
    )
    
    return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-capex', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_capex(jmas_seleccionado):
    categorias = ['Paneles Solares', 'Inversores y BOP', 'BESS (Baterías)', 
                  'Infraestructura Eléctrica', 'Desarrollo y EPC']
    valores = [1727.8, 434.5, 328.6, 106.3, 70.8]
    colores = [COLORS_DARK['warning'], COLORS_DARK['accent'], COLORS_DARK['success'], COLORS_DARK['info'], COLORS_DARK['danger']]
    
    fig = go.Figure(data=[go.Pie(
        labels=categorias,
        values=valores,
        hole=.5,
        marker=dict(colors=colores),
        textinfo='label+percent',
        texttemplate='%{label}<br>$%{value:.1f}M<br>%{percent}'
    )])
    
    fig.update_layout(
        title="Distribución de CAPEX (Total: $2,616 M MXN)",
        annotations=[dict(text='CAPEX<br>Total', x=0.5, y=0.5, font_size=16, showarrow=False, font_color=COLORS_DARK['primary'])]
    )
    
    return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-financiamiento', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_financiamiento(jmas_seleccionado):
    categorias = ['Capital Propio (30%)', 'Deuda Bancaria (70%)']
    valores = [784.8, 1831.2]
    
    fig = go.Figure(data=[go.Pie(
        labels=categorias,
        values=valores,
        hole=.4,
        marker=dict(colors=[COLORS_DARK['success'], COLORS_DARK['danger']]),
        textinfo='label+value',
        texttemplate='%{label}<br>$%{value:.1f}M MXN'
    )])
    
    fig.update_layout(
        title="Estructura de Financiamiento"
    )
    
    return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-proyeccion-financiera', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_proyeccion_financiera(jmas_seleccionado):
    años = list(range(1, 16))
    
    ingresos_base = 36.04
    tasa_crecimiento = 0.06
    
    ingresos = [ingresos_base * (1 + tasa_crecimiento) ** (i-1) for i in años]
    egresos = [21.97 - (i * 0.5) for i in años]
    utilidad = [ing - egr for ing, egr in zip(ingresos, egresos)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=años, y=ingresos,
        name='Ingresos (Ahorro)',
        line=dict(color=COLORS_DARK['success'], width=3),
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=años, y=egresos,
        name='Egresos (Deuda+OPEX)',
        line=dict(color=COLORS_DARK['danger'], width=3),
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=años, y=utilidad,
        name='Utilidad Neta',
        line=dict(color=COLORS_DARK['accent'], width=3),
        mode='lines+markers',
        fill='tozeroy',
        fillcolor=f'rgba(144, 224, 239, 0.2)'
    ))
    
    fig.update_layout(
        title="Proyección Financiera (15 años)",
        xaxis_title="Año",
        yaxis_title="Millones MXN",
        hovermode='x unified'
    )
    
    return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-flujo-caja', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_flujo_caja(jmas_seleccionado):
    años = list(range(1, 16))
    utilidad_anual = [14.07, 15.80, 17.55, 19.34, 21.16, 23.01, 24.89, 26.81, 28.76, 30.75, 32.77, 34.84, 36.94, 39.08, 41.26]
    utilidad_acumulada = []
    acumulado = 0
    
    for util in utilidad_anual:
        acumulado += util
        utilidad_acumulada.append(acumulado)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=años,
        y=utilidad_acumulada,
        mode='lines+markers',
        name='Utilidad Acumulada',
        line=dict(color=COLORS_DARK['success'], width=4),
        marker=dict(size=10),
        fill='tozeroy',
        fillcolor=f'rgba(6, 255, 165, 0.2)'
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS_DARK['danger'], 
                  annotation_text="Break-even", annotation_position="right")
    
    fig.update_layout(
        title="Flujo de Caja Acumulado (Utilidad)",
        xaxis_title="Año",
        yaxis_title="Millones MXN",
        hovermode='x unified'
    )
    
    return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-comparativo-escenarios', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_comparativo_escenarios(jmas_seleccionado):
    años = list(range(1, 16))
    
    costo_base_cfe = 792.7
    sin_proyecto = [costo_base_cfe * (1.06 ** (i-1)) for i in años]
    sin_proyecto_acum = []
    acum = 0
    for costo in sin_proyecto:
        acum += costo
        sin_proyecto_acum.append(acum)
    
    con_proyecto_anual = [21.97 - (i * 0.5) + 2.62 for i in años]
    con_proyecto_acum = [2616]
    for gasto in con_proyecto_anual:
        con_proyecto_acum.append(con_proyecto_acum[-1] + gasto)
    con_proyecto_acum = con_proyecto_acum[1:]
    
    ahorro = [sp - cp for sp, cp in zip(sin_proyecto_acum, con_proyecto_acum)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=años, y=sin_proyecto_acum,
        name='Sin Proyecto (Pago a CFE)',
        line=dict(color=COLORS_DARK['danger'], width=3, dash='dash'),
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=años, y=con_proyecto_acum,
        name='Con Proyecto (CAPEX+OPEX)',
        line=dict(color=COLORS_DARK['info'], width=3),
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=años, y=ahorro,
        name='Ahorro Neto',
        line=dict(color=COLORS_DARK['success'], width=4),
        mode='lines+markers',
        fill='tozeroy',
        fillcolor=f'rgba(6, 255, 165, 0.2)'
    ))
    
    fig.update_layout(
        title="Comparativo de Escenarios: Sin Proyecto vs Con Proyecto (Acumulado)",
        xaxis_title="Año",
        yaxis_title="Millones MXN Acumulados",
        hovermode='x unified'
    )
    
    return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-ahorro-acumulado', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_ahorro_acumulado(jmas_seleccionado):
    try:
        años = list(range(1, 16))
        ahorro_anual = [50, 120, 250, 420, 640, 910, 1230, 1600, 2020, 2490, 3010, 3580, 4200, 4870, 5590]
        
        fig = go.Figure()
        
        # Simplificar el colorscale para evitar problemas
        fig.add_trace(go.Bar(
            x=años,
            y=ahorro_anual,
            marker=dict(
                color=COLORS_DARK['success'],
                line=dict(color=COLORS_DARK['accent'], width=1)
            ),
            text=[f'${a}M' for a in ahorro_anual],
            textposition='outside',
            textfont={'color': COLORS_DARK['text']}
        ))
        
        fig.update_layout(
            title="Ahorro Neto Acumulado por Año",
            xaxis_title="Año",
            yaxis_title="Ahorro Acumulado (Millones MXN)",
            showlegend=False
        )
        
        return aplicar_tema_oscuro(fig)
    except Exception as e:
        print(f"ERROR en grafico-ahorro-acumulado: {e}")
        import traceback
        traceback.print_exc()
        # Retornar figura vacía en caso de error
        fig = go.Figure()
        fig.update_layout(title="Error al cargar gráfico")
        return aplicar_tema_oscuro(fig)

@app.callback(
    Output('grafico-emisiones-co2', 'figure'),
    Input('jmas-selector', 'value')
)
def actualizar_emisiones_co2(jmas_seleccionado):
    # CORREGIDO: emisiones en lugar de emisiones
    emisiones = {
        'Juarez': 69200,
        'Chihuahua': 64950,
        'Cuauhtemoc': 14630,
        'Parral': 10678
    }
    
    if jmas_seleccionado == 'Todas':
        fig = go.Figure(data=[
            go.Bar(
                x=list(emisiones.keys()),
                y=list(emisiones.values()),
                marker_color=[COLORS_DARK['success'], COLORS_DARK['info'], COLORS_DARK['accent'], COLORS_DARK['warning']],
                text=[f'{v:,} ton' for v in emisiones.values()],
                textposition='outside',
                textfont={'color': COLORS_DARK['text']}
            )
        ])
        
        total = sum(emisiones.values())
        fig.add_annotation(
            text=f'<b>Total: {total:,} toneladas CO₂/año</b>',
            xref='paper', yref='paper',
            x=0.5, y=1.1,
            showarrow=False,
            font=dict(size=14, color=COLORS_DARK['success'])
        )
    else:
        fig = go.Figure(data=[
            go.Bar(
                x=[jmas_seleccionado],
                y=[emisiones[jmas_seleccionado]],
                marker_color=COLORS_DARK['success'],
                text=[f'{emisiones[jmas_seleccionado]:,} ton'],
                textposition='outside',
                textfont={'color': COLORS_DARK['text']},
                width=0.4
            )
        ])
    
    fig.update_layout(
        title="Reducción Anual de Emisiones CO₂ por JMAS",
        xaxis_title="JMAS",
        yaxis_title="Toneladas CO₂/año",
        showlegend=False
    )
    
    return aplicar_tema_oscuro(fig)

# ============================================================================
# EJECUTAR APLICACIÓN
# ============================================================================

# Exponer el servidor para Vercel
server = app.server

if __name__ == '__main__':
    print("\n" + "="*80)
    print("INICIANDO DASHBOARD EJECUTIVO JCAS CHIHUAHUA - MODO OSCURO")
    print("="*80)
    print("\nDashboard disponible en: http://localhost:8050")
    print("\nCaracteristicas:")
    print("   - Modo Oscuro Profesional Activado")
    print("   - Analisis interactivo por JMAS")
    print("   - Diagnostico operativo completo")
    print("   - Dimensionamiento del proyecto solar")
    print("   - Proyecciones financieras")
    print("   - Comparativo de escenarios")
    print("   - Impacto ambiental")
    print("\nPresiona Ctrl+C para detener el servidor")
    print("="*80 + "\n")
    
    # Usar variables de entorno para configuración
    import os
    port = int(os.environ.get('PORT', 8050))
    debug = os.environ.get('DEBUG', 'False') == 'True'
    
    app.run(debug=debug, port=port, host='0.0.0.0')
