import dash
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Load your data
df= pd.read_csv('student_life_dataWrangled.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Student Perfomance Dashboard"),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Frequency of Values in Categorical Field', 'value': 'bar plot one'},
            {'label': 'Violin Plot of Categorical Variables', 'value': 'violin plot'},
            {'label': 'Relationship between Avg_Attendance and GPA-Heat map', 'value': 'heat map'},
            {'label': 'Relationship between Avg_Attendance and GPA-Bar chart', 'value': 'bar chart'},
            {'label': 'Workout-Pie chart', 'value': 'pie chart'}
        ],
        #value='histogram'
    ),
    dcc.Graph(id='graph')
])


# Define the callback to update the graph
@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value')]
)
def update_figure(selected_value):
    global fig
    if selected_value == 'bar plot one':
        fig = px.bar(df['University'].value_counts(), x=df['University'].value_counts().index, y=df['University'].value_counts().values,
             labels={'x':'University', 'y':'Frequency'},
             title='Frequency of Universities')
        fig.update_layout(
            width=1000,
            height=800,
        )

    elif selected_value == 'violin plot':
        fig = px.violin(df, x='Degree', y='Avg_sleep_time')

    elif selected_value == 'heat map':
        cross_tab = pd.crosstab(df['Avg_Attendance'], df['GPA'])
        fig = px.imshow(cross_tab)
    elif selected_value == 'bar chart':
        low_counts = df[df['Avg_Attendance'] == 'Below 60%']['GPA'].value_counts().reindex(df['GPA'].unique(),
                                                                                           fill_value=0)

        # Filtering medium attendance range
        medium_counts = df[df['Avg_Attendance'].isin(['60%-70%', '70%-80%'])]['GPA'].value_counts().reindex(
            df['GPA'].unique(), fill_value=0)

        # Filtering high attendance range
        high_counts = df[df['Avg_Attendance'].isin(['80%-90%', '90% - 100%'])]['GPA'].value_counts().reindex(
            df['GPA'].unique(), fill_value=0)
        trace1 = go.Bar(x=df['GPA'].unique(), y=low_counts, name='Below 60% Avg_Attendance')
        trace2 = go.Bar(x=df['GPA'].unique(), y=medium_counts, name='60%-80% Avg_Attendance')
        trace3 = go.Bar(x=df['GPA'].unique(), y=high_counts, name='Above 80% Avg_Attendance')

        layout = go.Layout(
            barmode='group',
            title='Relationship between Avg_Attendance and GPA',
            xaxis=dict(title='GPA'),
            yaxis=dict(title='Frequency')
        )
        fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
    elif selected_value == 'pie chart':
        fig = px.pie(df,  names='Workout', title='Workout')

    else:
        fig =  px.bar(df['University'].value_counts(), x=df['University'].value_counts().index, y=df['University'].value_counts().values,
             labels={'x':'University', 'y':'Frequency'},
             title='Frequency of Universities')
        fig.update_layout(
            width=1000,
            height=800,
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

