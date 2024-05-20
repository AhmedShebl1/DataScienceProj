from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

# Loading data
df = pd.read_csv('Student Attitude and Behavior.csv')

# Initializing the Dash app
app = Dash(__name__)

# Defining the app layout
app.layout = html.Div([
    html.H1("Student Attitude and Behavior Dashboard"),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Histogram - Marks', 'value': 'Histogram'},
            {'label': 'Pie Chart - Hobbies', 'value': 'pie_hobbies'},
            {'label': 'Pie Chart - Part-Time Jobs', 'value': 'pie_jobs'},
            {'label': 'Pie Chart - Gender', 'value': 'pie_gender'},
            {'label': 'Pie Chart - Stress Levels', 'value': 'pie_stress'},
            {'label': '3D Scatter Plot - Stress Level vs Marks', 'value': 'scatter_3d_stress'},
            {'label': '3D Scatter Plot - Hobbies vs Marks', 'value': 'scatter_3d_hobbies'},
            {'label': '3D Scatter Plot - Financial Status vs Marks', 'value': 'scatter_3d_financial'},
            {'label': '3D Scatter Plot - Part-Time Job vs Marks', 'value': 'scatter_3d_job'}
        ],
        value='histogram'
    ),
    dcc.Graph(id='graph')
])


# Defining the callback to update the graph
@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value')]
)
def update_figure(selected_value):  # Function to update the graph based on the selected value
    global fig
    if selected_value == 'Histogram':
       fig = make_subplots(rows=1, cols=3)
       fig.add_trace(go.Histogram(x=df['10th Mark'], nbinsx=20, name='10th Mark'), row=1, col=1)
       fig.add_trace(go.Histogram(x=df['12th Mark'], nbinsx=20, name='12th Mark'), row=1, col=2)
       fig.add_trace(go.Histogram(x=df['college mark'], nbinsx=20, name='college mark'), row=1, col=3)
       fig.update_layout(title_text="Distribution of Marks Across Different Levels", bargap=0.1)
    elif selected_value == 'pie_hobbies':
        fig = px.pie(df, names='hobbies', title='Students\' Hobbies')
    elif selected_value == 'pie_jobs':
        fig = px.pie(df, names='part-time job', title='Students With Part-Time Jobs', color='part-time job',
                     color_discrete_map={'Yes': 'green', 'No': 'red'})
    elif selected_value == 'pie_gender':
        fig = px.pie(df, names='Gender', title='Gender Distribution', color='Gender',
                     color_discrete_map={'Male': 'blue', 'Female': 'pink'})
    elif selected_value == 'pie_stress':
        fig = px.pie(df, names='Stress Level ', title='Stress Levels', color='Stress Level ',
                     color_discrete_map={'Good': 'green', 'Bad': 'orange', 'Awful': 'red', 'fabulous': 'blue'},)
    elif selected_value == 'scatter_3d_stress':
        fig = px.scatter_3d(df, x='10th Mark', y='12th Mark', z='college mark', color='Stress Level ',
                            color_discrete_map={'Good': 'green', 'Bad': 'orange', 'Awful': 'red', 'fabulous': 'blue'})
    elif selected_value == 'scatter_3d_hobbies':
        fig = px.scatter_3d(df, x='10th Mark', y='12th Mark', z='college mark', color='hobbies')
    elif selected_value == 'scatter_3d_financial':
        fig = px.scatter_3d(df, x='10th Mark', y='12th Mark', z='college mark', color='Financial Status',
                            color_discrete_map={'good': 'green', 'Bad': 'orange', 'Awful': 'red', 'Fabulous': 'blue'})
    elif selected_value == 'scatter_3d_job':
        fig = px.scatter_3d(df, x='10th Mark', y='12th Mark', z='college mark', color='part-time job',
                            color_discrete_map={'Yes': 'green', 'No': 'red'})
    else:
        fig = go.Figure()  # Default plot if no option is selected
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
