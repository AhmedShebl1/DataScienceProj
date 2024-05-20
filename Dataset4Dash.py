from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Loading data
df = pd.read_csv('student-por.csv')

# Initializing the Dash app
app = Dash(__name__)

# Defining the app layout
app.layout = html.Div([
    html.H1("Student Performance Dashboard"),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Scatter Plot: G3 vs G2 by Gender', 'value': 'scatter_g3_g1'},
            {'label': 'Scatter Plot: G3 vs G1 by Gender', 'value': 'scatter_g3_g2'},
            {'label': 'Histogram: Absences by Gender', 'value': 'histogram'},
            {'label': 'Violin Plot', 'value': 'violin'},
            {'label': 'Box Plot of Parents education and G3', 'value': 'box'},
            {'label': 'Bar Chart: G3 vs Study Time', 'value': 'bar_g3_studytime'},
            {'label': 'Bar Chart: G3 vs Internet', 'value': 'bar_g3_internet'},
            {'label': 'Box Plot: G3 vs Daily Alcohol Consumption', 'value': 'box_g3_dalc'},
            {'label': 'Box Plot: G3 vs Weekend Alcohol Consumption', 'value': 'box_g3_walc'}
        ],
        value='select'
    ),
    dcc.Graph(id='graph')
])

# Defining the callback to update the graph
@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value')]
)
def update_figure(selected_value):
    if selected_value == 'scatter_g3_g2':
        fig = px.scatter(df, x='G2', y='G3',color='sex', title='Scatter Plot: G3 vs G2 by Gender')
    elif selected_value == 'bar_g3_studytime':
        fig = px.bar(df, x='studytime', y='G3', title='Bar Chart: G3 vs Study Time')
    elif selected_value == 'bar_g3_internet':
        fig = px.bar(df, x='internet', y='G3', title='Bar Chart: G3 vs Internet')
    elif selected_value == 'box_g3_dalc':
        fig = px.box(df, x='Dalc', y='G3', title='Box Plot: G3 vs Daily Alcohol Consumption')
    elif selected_value == 'box_g3_walc':
        fig = px.box(df, x='Walc', y='G3', title='Box Plot: G3 vs Weekend Alcohol Consumption')
    elif selected_value == 'scatter_g3_g1':
        fig = px.scatter(df, x='G1', y='G3', color='sex', title='Scatter Plot: G1 vs G3 by Gender')
    elif selected_value == 'histogram':
        fig = px.histogram(df, x='absences', color='sex', title='Histogram: Absences by Gender')
    elif selected_value == 'violin':
        fig = make_subplots(rows=1, cols=2, subplot_titles=("G3 Distribution by School", "G3 Distribution by Sex"))
        fig.add_trace(px.violin(df, x='school', y='G3', title='Violin Plot: G3 Distribution by School').data[0], row=1, col=1)
        fig.add_trace(px.violin(df, x='sex', y='G3', title='Violin Plot: G3 Distribution by Sex').data[0], row=1, col=2)
    elif selected_value == 'box':
        fig = make_subplots(rows=1, cols=2, subplot_titles=("G3 vs Mother's Education", "G3 vs Father's Education"))
        fig.add_trace(px.box(df, x='Medu', y='G3', title='Box Plot: G3 vs Mother\'s Education').data[0], row=1, col=1)
        fig.add_trace(px.box(df, x='Fedu', y='G3', title='Box Plot: G3 vs Father\'s Education').data[0], row=1, col=2)
    else:
        fig = go.Figure()
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

