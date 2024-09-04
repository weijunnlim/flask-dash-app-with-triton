from main_app.dash_shared import shared_dash_nav_links
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px

df = pd.read_csv('/home/dxd_wj/model_serving/flask-dash-app/main_app/stroke_predictor/healthcare-dataset-stroke-data.csv')

summary_stats = df.describe().transpose()
summary_stats = summary_stats.reset_index()  # Reset index to get column names as a column
summary_stats.rename(columns={"index": "Feature"}, inplace=True)  # Rename the index column to "Feature"

#Visualizations for categorical variables
gender_distribution = px.pie(df, names='gender', title='Gender Distribution')
work_type_distribution = px.pie(df, names='work_type', title='Work Type Distribution')
residence_type_distribution = px.pie(df, names='Residence_type', title='Residence Type Distribution')
smoking_status_distribution = px.pie(df, names='smoking_status', title='Smoking Status Distribution')
stroke_distribution = px.pie(df, names='stroke', title='Stroke Distribution')

# Layout
layout = html.Div([
    shared_dash_nav_links(),
    html.H2("Dataset Preview"),
    
    # Dataset preview table with filtering enabled
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.head(10).to_dict('records'),
        #filter_action='native',  # Enable filtering
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'age'}, 'textAlign': 'right'},
        ],
        style_data_conditional=[
            {
                'if': {'filter_query': '{stroke} = 1', 'column_id': 'stroke'},
                'backgroundColor': 'tomato',
                'color': 'white',
            }
        ],
    ),
    
    html.Hr(),
    
    # Summary statistics with feature names included
    html.H3("Summary Statistics"),
    dash_table.DataTable(
        id='summary-table',
        columns=[{"name": i, "id": i} for i in summary_stats.columns],
        data=summary_stats.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    ),
    
    html.Hr(),
    
    # Visualizations
    dcc.Graph(
        id='gender-pie-chart',
        figure=gender_distribution
    ),
    
    dcc.Graph(
        id='work-type-pie-chart',
        figure=work_type_distribution
    ),
    
    dcc.Graph(
        id='residence-type-pie-chart',
        figure=residence_type_distribution
    ),
    
    dcc.Graph(
        id='smoking-status-pie-chart',
        figure=smoking_status_distribution
    ),
    
    dcc.Graph(
        id='stroke-pie-chart',
        figure=stroke_distribution
    ),
    
    html.Hr(),
    
    # Add more visualizations and features as needed
])
