from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Loading data
df = pd.read_csv('Campus_Selection.csv')

# Initializing the Dash app
app = Dash(__name__)

# Defining the app layout
app.layout = html.Div([
    html.H1("Student Performance Dashboard"),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Recruitment Status vs Secondary and Higher Secondary Scores--Scatter Plot', 'value': 'scatter'},
            {'label': 'Recruitment Status vs Undergraduate Scores--Histogram', 'value': 'histogram'},
            {'label': 'Recruitment Status vs MBA Score--Violin Plot', 'value': 'violin'},
            {'label': 'Recruitment Status vs Higher Sec. Education Board--Heatmap', 'value': 'heatmap'},
            {'label': 'Recruitment Status vs Employment Test Score--Box Plot', 'value': 'box'},
            {'label': 'Degree Type--Bar Chart', 'value': 'bar'},
            {'label': 'Recruitment Status--Pie Chart', 'value': 'pie'},
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
    if selected_value == 'scatter':
        fig = px.scatter(df, x='ssc_p', y='hsc_p', color='status',
                         title='Recruitment Status vs Secondary and Higher Secondary Scores',
                         labels={'ssc_p': 'Score % in Secondary Ed.', 'hsc_p': 'Score % in Higher Secondary Ed.'})
    elif selected_value == 'histogram':
        fig = px.histogram(df, x='degree_p', color='status', title='Recruitment Status vs Undergraduate Scores',
                           labels={'degree_p': 'Score %'})
    elif selected_value == 'violin':
        fig = px.violin(df, x='status', y='mba_p', box=True, title='Recruitment Status vs MBA Score',
                        labels={'status': 'Recruitment Status', 'mba_p': 'MBA Score %'})
    elif selected_value == 'heatmap':
        cross_tab = pd.crosstab(df['hsc_b'], df['status'])
        fig = px.imshow(cross_tab, labels=dict(x="Recruitment Status", y="HSC Board"),
                        title='Recruitment Status vs Higher Sec. Education Board')
    elif selected_value == 'box':
        fig = px.box(df, x='status', y='etest_p', color='status', title='Recruitment Status vs Employment Test Score',
                     labels={'status': 'Recruitment Status', 'etest_p': 'Employment Test Score %'})
    elif selected_value == 'bar':
        fig = px.bar(df, x='degree_t', color='status', title='Degree Type', labels={'degree_t': 'Degree Type'})
    elif selected_value == 'pie':
        status_counts = df['status'].value_counts()
        fig = px.pie(values=status_counts, names=status_counts.index, title='Recruitment Status')
    else:
        fig = go.Figure()  # Empty figure
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)