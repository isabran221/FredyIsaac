import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px

# Datos del proyecto (ajustados según la información proporcionada)
usuarios = [
    {"Tipo": "Candidatos", "Registrados": 1500, "Activos": 1200, "Postulaciones": 4500},
    {"Tipo": "Empresas", "Registradas": 50, "Activas": 40, "Ofertas Publicadas": 200}
]

flujos_contratacion = [
    {"Etapa": "Postulación", "Candidatos": 4500, "Progreso": 100},
    {"Etapa": "Revisión CV", "Candidatos": 3000, "Progreso": 66.67},
    {"Etapa": "Entrevista", "Candidatos": 1000, "Progreso": 22.22},
    {"Etapa": "Contratación", "Candidatos": 500, "Progreso": 11.11}
]

# Presupuesto ajustado a $50,000 USD
presupuesto = [
    {"Rubro": "Servidores", "Presupuesto": 15000, "Gastos": 14000},
    {"Rubro": "Desarrollo", "Presupuesto": 20000, "Gastos": 18000},
    {"Rubro": "Seguridad", "Presupuesto": 10000, "Gastos": 9000},
    {"Rubro": "Diseño UI/UX", "Presupuesto": 5000, "Gastos": 4000}
]

# Verificar que el presupuesto total no exceda $50,000 USD
total_presupuesto = sum(item["Presupuesto"] for item in presupuesto)
if total_presupuesto > 50000:
    print("Error: El presupuesto total excede los $50,000 USD.")
else:
    print(f"Presupuesto total: ${total_presupuesto} USD (dentro del límite).")

# Crear DataFrames
df_usuarios = pd.DataFrame(usuarios)
df_flujos = pd.DataFrame(flujos_contratacion)
df_presupuesto = pd.DataFrame(presupuesto)

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout del dashboard
app.layout = html.Div(children=[
    html.H1("KPI Dashboard - Plataforma de Contratación Inteligente", style={"textAlign": "center"}),
    html.Div([
        html.H2("Resumen de Usuarios"),
        dcc.Graph(
            id="resumen-usuarios",
            figure={
                "data": [
                    {"x": df_usuarios["Tipo"], "y": df_usuarios["Registrados"], "type": "bar", "name": "Registrados"},
                    {"x": df_usuarios["Tipo"], "y": df_usuarios["Activos"], "type": "bar", "name": "Activos"}
                ],
                "layout": {"title": "Usuarios Registrados y Activos"}
            }
        )
    ]),
    html.Div([
        html.H2("Flujos de Contratación"),
        dcc.Graph(
            id="flujos-contratacion",
            figure=px.bar(df_flujos, x="Etapa", y="Candidatos", title="Candidatos por Etapa de Contratación", color="Etapa")
        )
    ]),
    html.Div([
        html.H2("Progreso de Flujos de Contratación"),
        dcc.Graph(
            id="progreso-flujos",
            figure=px.line(df_flujos, x="Etapa", y="Progreso", title="Progreso de Flujos de Contratación", markers=True)
        )
    ]),
    html.Div([
        html.H2("Presupuesto vs Gastos"),
        dcc.Graph(
            id="presupuesto-gastos",
            figure={
                "data": [
                    {"x": df_presupuesto["Rubro"], "y": df_presupuesto["Presupuesto"], "type": "bar", "name": "Presupuesto"},
                    {"x": df_presupuesto["Rubro"], "y": df_presupuesto["Gastos"], "type": "bar", "name": "Gastos"}
                ],
                "layout": {"title": "Presupuesto vs Gastos por Rubro"}
            }
        )
    ]),
    html.Div([
        html.H2("Tabla de Flujos de Contratación"),
        html.Table(
            # Encabezados de la tabla
            [html.Tr([html.Th(col) for col in df_flujos.columns])] +
            # Filas de la tabla
            [html.Tr([html.Td(df_flujos.iloc[i][col]) for col in df_flujos.columns]) for i in range(len(df_flujos))]
        )
    ]),
    html.Div([
        html.H2("Tabla de Presupuesto"),
        html.Table(
            # Encabezados de la tabla
            [html.Tr([html.Th(col) for col in df_presupuesto.columns])] +
            # Filas de la tabla
            [html.Tr([html.Td(df_presupuesto.iloc[i][col]) for col in df_presupuesto.columns]) for i in range(len(df_presupuesto))]
        )
    ])
])

# Ejecutar el servidor
if __name__ == "__main__":
    app.run_server(debug=True)
