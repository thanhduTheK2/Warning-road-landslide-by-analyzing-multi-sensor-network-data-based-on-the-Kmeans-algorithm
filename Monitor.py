import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import random
from sklearn.cluster import KMeans

# Initialize the Dash app
app = dash.Dash(__name__)

# Sample data
time = np.arange(100)
vibration_data = np.zeros(100)
moisture_data = np.zeros(100)
temperature_data = np.zeros(100)

# Layout of the app
app.layout = html.Div(style={'backgroundColor': '#fff', 'color': '#fff', 'padding': '20px'}, children=[
    html.H1("KHSV2403-HE THONG GIAM SAT VA CANH BAO SAT LO DAT DUONG BO", style={'textAlign': 'center'}),

    # Main chart with increased size
    dcc.Graph(id='main-chart', style={'height': '600px'}, config={'responsive': True}),

    # Status gauge
    dcc.Graph(id='status-gauge', style={'height': '300px'}),

    # K-means clustering chart
    dcc.Graph(id='clustering-chart', style={'height': '400px'}),

    # Warning status
    html.Div(id='warning-status', style={
        'backgroundColor': '#333',
        'padding': '20px',
        'borderRadius': '5px',
        'textAlign': 'center',
        'fontSize': '24px',
        'color': '#fff',
        'marginTop': '20px'
    }),
    # Three equal-sized charts for sensor parameters
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '20px'}, children=[
        dcc.Graph(id='vibration-chart', style={'flex': '1', 'marginRight': '10px'}),
        dcc.Graph(id='moisture-chart', style={'flex': '1', 'marginRight': '10px'}),
        dcc.Graph(id='temperature-chart', style={'flex': '1'})
    ]),

    # Interval component for real-time updates
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # 1 second
        n_intervals=0
    )
])
# Callback to update charts and gauge
@app.callback(
    Output('main-chart', 'figure'),
    Output('status-gauge', 'figure'),
    Output('clustering-chart', 'figure'),
    Output('vibration-chart', 'figure'),
    Output('moisture-chart', 'figure'),
    Output('temperature-chart', 'figure'),
    Output('warning-status', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    global vibration_data, moisture_data, temperature_data

    # Update data with random values
    vibration_data = np.roll(vibration_data, -1)
    moisture_data = np.roll(moisture_data, -1)
    temperature_data = np.roll(temperature_data, -1)

    # Generate random values within specified limits
    vibration_data[-1] = random.uniform(0.4, 0.45)  # Simulating data for vibration
    moisture_data[-1] = random.uniform(0.4, 0.45)  # Simulating data for moisture
    temperature_data[-1] = random.uniform(0.4, 0.45)  # Simulating data for temperature

    # Main chart with custom styling
    main_fig = go.Figure()

    # Main series (e.g., Vibration)
    main_fig.add_trace(go.Scatter(x=time, y=vibration_data, mode='lines', name='Vibration',
                                  line=dict(color='orange', width=2)))

    # Other series (Moisture and Temperature)
    main_fig.add_trace(go.Scatter(x=time, y=moisture_data, mode='lines', name='Moisture',
                                  line=dict(color='blue', width=1.5)))
    main_fig.add_trace(go.Scatter(x=time, y=temperature_data, mode='lines', name='Temperature',
                                  line=dict(color='green', width=1.5)))

    # Set layout for main chart
    main_fig.update_layout(
        title='Real-time Monitoring of Landslide Indicators',
        xaxis_title='Time',
        yaxis_title='Sensor Readings',
        plot_bgcolor='black',
        paper_bgcolor='white',
        font_color='black',
        yaxis=dict(range=[0.39, 0.46])  # Set Y-axis range
    )

    # Create K-means clustering
    data = np.array([vibration_data, moisture_data, temperature_data]).T
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(data)
    labels = kmeans.labels_

    # Create clustering chart
    clustering_fig = go.Figure()
    for i in range(3):
        clustering_fig.add_trace(go.Scatter(
            x=data[labels == i, 0],
            y=data[labels == i, 1],
            mode='markers',
            name=f'Cluster {i + 1}',
            marker=dict(size=10)
        ))

    clustering_fig.update_layout(
        title='Fuzzy & K-means Clustering of Sensor Data',
        xaxis_title='Vibration',
        yaxis_title='Moisture',
        plot_bgcolor='white',
        paper_bgcolor='black',
        font_color='black'
    )

    # Determine warning level
    warning_level = "Normal"
    if np.any(vibration_data > 0.45) or np.any(moisture_data > 0.45) or np.any(temperature_data > 0.45):
        warning_level = "Danger"
    elif np.any(vibration_data < 0.40) or np.any(moisture_data < 0.40) or np.any(temperature_data < 0.40):
        warning_level = "Risk"

    # Create a status gauge
    gauge_value = 0
    if warning_level == "Normal":
        gauge_value = 1  # Bình thường
    elif warning_level == "Risk":
        gauge_value = 2  # Nguy cơ
    elif warning_level == "Danger":
        gauge_value = 3  # Cảnh báo

    status_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gauge_value,
        title={'text': "Trạng thái", 'font': {'size': 24}},
        gauge={'axis': {'range': [0, 3], 'tickvals': [1, 2, 3], 'ticktext': ['Bình thường', 'Nguy cơ', 'Cảnh báo']},
               'bar': {'color': "blue"},
               'steps': [
                   {'range': [0, 1], 'color': "green"},
                   {'range': [1, 2], 'color': "yellow"},
                   {'range': [2, 3], 'color': "red"},
               ]}
    ))
    status_gauge.update_layout(paper_bgcolor='white', font_color='black', height=300)

    # Vibration chart
    vibration_fig = go.Figure(go.Scatter(x=time, y=vibration_data, mode='lines+markers', name='Vibration',
                                         line=dict(color='purple'), marker=dict(color='purple', size=6)))
    vibration_fig.update_layout(title='Vibration Sensor Readings', yaxis_title='Vibration', xaxis_title='Time',
                                plot_bgcolor='white', paper_bgcolor='white', font_color='black')

    # Moisture chart
    moisture_fig = go.Figure(go.Scatter(x=time, y=moisture_data, mode='lines+markers', name='Moisture',
                                        line=dict(color='lightblue'), marker=dict(color='lightblue', size=6)))
    moisture_fig.update_layout(title='Moisture Sensor Readings', yaxis_title='Moisture', xaxis_title='Time',
                               plot_bgcolor='white', paper_bgcolor='white', font_color='black')

    # Temperature chart
    temperature_fig = go.Figure(go.Scatter(x=time, y=temperature_data, mode='lines+markers', name='Temperature',
                                           line=dict(color='red'), marker=dict(color='red', size=6)))
    temperature_fig.update_layout(title='Temperature Sensor Readings', yaxis_title='Temperature', xaxis_title='Time',
                                  plot_bgcolor='white', paper_bgcolor='white', font_color='black')

    return main_fig, status_gauge, clustering_fig, vibration_fig, moisture_fig, temperature_fig, f"Warning Level: {warning_level}"
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
