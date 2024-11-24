
#This part is code for visualization with dropdown component
#Chart including:
#1.Time-series plots to show trends in bookings over months;
#2.Bar charts to compare the share of local vs. international guests; 
#3.Pie charts to further compare the share of local vs. international guests;
#4.Heatmaps to visualize the concentration of short-stay accommodations by region;
#5.Top 10 popular destination analysis by mutiple geo layer;
#6.Animations to show changes over time.
import pandas as pd  # Import pandas for data manipulation
import plotly.express as px  # Import Plotly for visualizations
import dash  # Import Dash framework
from dash import dcc, html

from dash.dependencies import Input, Output
import json  # For working with GeoJSON files

# Load your data
summary_df = pd.read_csv('data/dataset.csv')  # Replace with the actual path to your summary data file
long_df = pd.read_csv('data/long_df_flask.csv')  # Replace with the actual path to your detailed data file

# Load GeoJSON data
with open('data/NUTS_RG_60M_2024_4326.geojson') as f:
    nuts_geojson = json.load(f)

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import json

# Convert the month column to a category type and specify the order of the categories
month_order = [f"M{str(i).zfill(2)}" for i in range(1, 13)]
summary_df['month'] = pd.Categorical(summary_df['month'], categories=month_order, ordered=True)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Charts"),

    # Line chart controls
    html.H2("Line Chart Controls"),
    dcc.Dropdown(
        id='geo_layer-dropdown',
        options=[{'label': geo_layer, 'value': geo_layer} for geo_layer in summary_df['geo_layer'].unique()],
        value=summary_df['geo_layer'].unique()[0]
    ),
    dcc.Dropdown(
        id='indic_to-dropdown',
        options=[
            {'label': 'Length of Stay', 'value': 'LSTY'},
            {'label': 'Stay', 'value': 'STY'},
            {'label': 'Night Spent', 'value': 'NGT_SP'}
        ],
        value='LSTY'  
    ),
    dcc.Dropdown(
        id='c_resid-dropdown',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': c_resid, 'value': c_resid} for c_resid in summary_df['c_resid'].unique()],
        value='All'
    ),
    dcc.Graph(id='line-chart'),

    # Bar chart controls
    html.H2("Bar Chart Controls"),
    dcc.Dropdown(
        id='indic_to_filter',
        options=[
            {'label': 'Length of Stay', 'value': 'LSTY'},
            {'label': 'Stay', 'value': 'STY'},
            {'label': 'Night Spent', 'value': 'NGT_SP'}
        ],
        value='LSTY',  
        multi=False,
        placeholder="Select Indicator"
    ),
    dcc.Dropdown(
        id='year_filter',
        options=[{'label': year, 'value': year} for year in summary_df['Year'].unique()],
        value=summary_df['Year'].unique()[0],
        multi=False,
        placeholder="Select Year"
    ),
    dcc.Dropdown(
        id='geo_layer_filter',
        options=[{'label': geo, 'value': geo} for geo in summary_df['geo_layer'].unique()],
        value=summary_df['geo_layer'].unique()[0],
        multi=False,
        placeholder="Select Geographical Layer"
    ),
    dcc.Graph(id='bar_chart'),

    # New Pie Chart Controls
    html.H2("Pie Chart Controls"),
    dcc.Dropdown(
        id='pie_chart_indic_to',
        options=[
            {'label': 'Length of Stay', 'value': 'LSTY'},
            {'label': 'Stay', 'value': 'STY'},
            {'label': 'Night Spent', 'value': 'NGT_SP'}
        ],
        value='LSTY'  
    ),
    dcc.Dropdown(
        id='pie_chart_geo_layer',
        options=[{'label': geo_layer, 'value': geo_layer} for geo_layer in summary_df['geo_layer'].unique()],
        value=summary_df['geo_layer'].unique()[0],
        multi=False,
        placeholder="Select Geographical Layer"
    ),
    dcc.Dropdown(
        id='pie_chart_year',
        options=[{'label': year, 'value': year} for year in summary_df['Year'].unique()],
        value=summary_df['Year'].unique()[0],
        multi=False,
        placeholder="Select Year"
    ),
 
    dcc.Dropdown(
        id='pie_chart_month',
        options=[
            {'label': 'All', 'value': 'All'}  
        ] + [{'label': month, 'value': month} for month in summary_df['month'].unique()],  # Remaining month options
        value='All',  # All is checked by default
        multi=False,
        placeholder="Select Month"
    ),
    dcc.Graph(id='pie_chart'),# New graph for the pie chart

    # New heatmap control
    html.H2("Geographical Heatmap Controls"),
    dcc.Dropdown(
        id='heatmap_indic_to',
        options=[
            {'label': 'Length of Stay', 'value': 'LSTY'},
            {'label': 'Stay', 'value': 'STY'},
            {'label': 'Night Spent', 'value': 'NGT_SP'}
        ],
        value='LSTY',  
        multi=False,
        placeholder="Select Indicator"
    ),
    dcc.Dropdown(
        id='heatmap_year',
        options=[{'label': year, 'value': year} for year in long_df['Year'].unique()],
        value='2023',
        multi=False,
        placeholder="Select Year"
    ),
    dcc.Dropdown(
        id='heatmap_c_resid',
        options=[{'label': c_resid, 'value': c_resid} for c_resid in long_df['c_resid'].unique()],
        value='DOM',  
        multi=False,
        placeholder="Select Residency"
    ),
    dcc.Dropdown(
        id='heatmap_month',
        options=[{'label': month, 'value': month} for month in long_df['month'].unique()],
        value='M01',  
        multi=False,
        placeholder="Select Month"
    ),
    dcc.Dropdown(
        id='heatmap_geo_layer',
        options=[{'label': geo_layer, 'value': geo_layer} for geo_layer in long_df['geo_layer'].unique()],
        value=long_df['geo_layer'].unique()[0],
        multi=False,
        placeholder="Select geo_layer"
    ),    
    dcc.Graph(id='geo_heatmap'),  # Components for displaying heat maps
    # Add Top 10 Controls
    html.H2("Top 10 Popular Tourist Destinations"),
    dcc.Dropdown(
        id='top10_geo_layer',
        options=[{'label': geo_layer, 'value': geo_layer} for geo_layer in long_df['geo_layer'].unique()],
        value=long_df['geo_layer'].unique()[0],
        multi=False,
        placeholder="Select Geographical Layer"
    ),
    dcc.Dropdown(
        id='top10_year',
        options=[{'label': year, 'value': year} for year in long_df['Year'].unique()],
        value=long_df['Year'].unique()[0],
        multi=False,
        placeholder="Select Year"
    ),
    dcc.Dropdown(
        id='top10_c_resid',
        options=[{'label': c_resid, 'value': c_resid} for c_resid in long_df['c_resid'].unique()],
        value=long_df['c_resid'].unique()[0],
        multi=False,
        placeholder="Select Residency"
    ),
    dcc.Dropdown(
        id='top10_month',
        options=[{'label': month, 'value': month} for month in long_df['month'].unique()],
        value=long_df['month'].unique()[0],
        multi=False,
        placeholder="Select Month"
    ),
    dcc.Graph(id='top10_chart'),  # Graph for Top 10 Popular Tourist Destinations
    # Animated Chart Controls
    html.H2("Animated Change Over Time"),
    dcc.Dropdown(
        id='anim_geo_layer',
        options=[{'label': geo_layer, 'value': geo_layer} for geo_layer in long_df['geo_layer'].unique()],
        value=long_df['geo_layer'].unique()[0],
        multi=False,
        placeholder="Select Geographical Layer"
    ),
    dcc.Dropdown(
        id='anim_indic_to',
        options=[
            {'label': 'Length of Stay', 'value': 'LSTY'},
            {'label': 'Stay', 'value': 'STY'},
            {'label': 'Night Spent', 'value': 'NGT_SP'}
        ],
        value='LSTY', 
        multi=False,
        placeholder="Select Indicator"
    ),
    dcc.Graph(id='animated_chart'),  # Graph for animated changes over time
])
@app.callback(
    Output('line-chart', 'figure'),
    [Input('geo_layer-dropdown', 'value'),
     Input('indic_to-dropdown', 'value'),
     Input('c_resid-dropdown', 'value')]
)
def update_line_chart(selected_geo_layer, selected_indic_to, selected_c_resid):
    if selected_c_resid == 'All':
        filtered_df = summary_df[
            (summary_df['geo_layer'] == selected_geo_layer) &
            (summary_df['indic_to'] == selected_indic_to)
        ].groupby(['month', 'Year']).sum().reset_index()
    else:
        filtered_df = summary_df[
            (summary_df['geo_layer'] == selected_geo_layer) &
            (summary_df['indic_to'] == selected_indic_to) &
            (summary_df['c_resid'] == selected_c_resid)
        ]
    
    fig = px.line(
        filtered_df, x='month', y='Value', color='Year', 
        title=f"Evolution of Short Stay over the Months",
        labels={'month': 'Month', 'Value': f'Total Number'}
    )
    return fig

@app.callback(
    Output('bar_chart', 'figure'),
    Input('indic_to_filter', 'value'),
    Input('year_filter', 'value'),
    Input('geo_layer_filter', 'value')
)
def update_bar_chart(selected_indicator, selected_year, selected_geo_layer):
    
    filtered_df = summary_df[
        (summary_df['indic_to'] == selected_indicator) &
        (summary_df['Year'] == selected_year) &
        (summary_df['geo_layer'] == selected_geo_layer)
    ].copy()
    # Update the labels in the DataFrame
    filtered_df['c_resid'] = filtered_df['c_resid'].replace({'FOR': 'Foreigners', 'DOM': 'Residents'})
    total_value = filtered_df['Value'].sum()
    filtered_df['Percentage'] = (filtered_df['Value'] / total_value * 100).round(2).astype(str) + '%'


        # Create a bar chart, using c_resid as the color classification
    fig = px.bar(
        filtered_df,
        x='month',
        y='Value',
        color='c_resid',
        title='% of Domestic and foreign tourists per month in a year',
        labels={'month': 'Month', 'Value': f'Total Number'},
        text='Percentage'  # Percentage displayed on bar
    )

    # Update display settings for data labels
    fig.update_traces(textposition='outside', textfont=dict(size=12))
    # Change the legend title
    fig.update_layout(legend_title_text='Type')
    return fig

@app.callback(
    Output('pie_chart', 'figure'),
    [Input('pie_chart_indic_to', 'value'),
     Input('pie_chart_geo_layer', 'value'),
     Input('pie_chart_year', 'value'),
     Input('pie_chart_month', 'value')]
)
def update_pie_chart(selected_indicator, selected_geo_layer, selected_year, selected_month):
    # Data filtering
    filtered_df = summary_df[
        (summary_df['indic_to'] == selected_indicator) &
        (summary_df['geo_layer'] == selected_geo_layer) &
        (summary_df['Year'] == selected_year)
    ].copy()

    # Check month selection
    if selected_month == 'All':  # If the choice is “All” 
        # Update the labels in the DataFrame
        filtered_df['c_resid'] = filtered_df['c_resid'].replace({'FOR': 'Foreigners', 'DOM': 'Residents'})
        # Group and sum all months
        filtered_df = filtered_df.groupby(['c_resid'], as_index=False).agg({'Value': 'sum'})
        
        
    else:
        # Filter only selected months
        filtered_df = filtered_df[filtered_df['month'] == selected_month]

    # Create pie charts
    pie_fig = px.pie(
        filtered_df,
        names='c_resid',
        values='Value',
        title=f'Short Stay Residents vs Foreigners in {selected_year}'
    )

    return pie_fig


@app.callback(
    Output('geo_heatmap', 'figure'),
    [Input('heatmap_indic_to', 'value'),
     Input('heatmap_year', 'value'),
     Input('heatmap_c_resid', 'value'),
     Input('heatmap_month', 'value'),
    Input('heatmap_geo_layer', 'value')]
)


def update_geo_heatmap(selected_indicator, selected_year, selected_c_resid, selected_month,selected_geo_layer):
    # Data filtering
    filtered_heatmap_df = long_df[
        (long_df['indic_to'] == selected_indicator) &
        (long_df['Year'] == selected_year) &
        (long_df['c_resid'] == selected_c_resid) &
        (long_df['month'] == selected_month)&
        (long_df['geo_layer'] == selected_geo_layer)
    ].copy()

    # If there is no data, you can return an empty chart or a hint
    if filtered_heatmap_df.empty:
        return px.choropleth()  # You can insert an empty chart, or create a text marking data not found

    # create plot
    fig = px.choropleth(
        filtered_heatmap_df,
        geojson=nuts_geojson,
        locations='geo',  # geographic identifiers, make sure this matches the regions supported by Plotly
        featureidkey='properties.NUTS_ID',
        color='Value',  # Values plotted
        hover_name='geo',  #Information displayed on mouse hover
        title=f'Concentration of Short Stay per country in {selected_month} {selected_year}',
        #color_continuous_scale=px.colors.sequential.Plasma  # Choose a color scheme
        color_continuous_scale=px.colors.sequential.Plasma[::-1]
    )
    # Change legend label
    fig.update_layout(coloraxis_colorbar_title='Total Number')
    return fig

# Add callback for Top 10 chart
@app.callback(
    Output('top10_chart', 'figure'),
    [Input('top10_geo_layer', 'value'),
     Input('top10_year', 'value'),
     Input('top10_c_resid', 'value'),
     Input('top10_month', 'value')]
)
def update_top10_chart(selected_geo_layer, selected_year, selected_c_resid, selected_month):
    filtered_top10_df = long_df[
        (long_df['geo_layer'] == selected_geo_layer) &
        (long_df['Year'] == selected_year) &
        (long_df['c_resid'] == selected_c_resid) &
        (long_df['month'] == selected_month)
    ]

    # Group and sum values for each geographical code
    top10 = filtered_top10_df.groupby('geo')['Value'].sum().reset_index()

    
    # Sort by Value and select top 10
    top10 = top10.sort_values(by='Value', ascending=False).head(10)
    # Create bar chart for top 10 destinations
    fig = px.bar(
        top10,
        x='Value',
        y='geo',
        title=f'Top 10 Tourist Destinations in {selected_month} {selected_year}',
        labels={'geo': 'Country/NUTS Code', 'Value': 'Total Number'},
        orientation='h',
        category_orders={'geo': top10['geo'].tolist()}
    )

    return fig


@app.callback(
    Output('animated_chart', 'figure'),
    [Input('anim_geo_layer', 'value'),
     Input('anim_indic_to', 'value')]
)
def update_animated_chart(selected_geo_layer, selected_indicator):
    filtered_anim_df = long_df[
        (long_df['geo_layer'] == selected_geo_layer) &
        (long_df['indic_to'] == selected_indicator)
    ]
    # Update the labels in the DataFrame
    filtered_anim_df['c_resid'] = filtered_anim_df['c_resid'].replace({'FOR': 'Foreigners', 'DOM': 'Residents'})
    # Aggregate monthly values by Year and c_resid
    monthly_sum = filtered_anim_df.groupby(['Year', 'month', 'c_resid'])['Value'].sum().reset_index()

    # Create an 'All' row by summing FOR and DOM
    all_sum = monthly_sum.groupby(['Year', 'month'])['Value'].sum().reset_index()
    all_sum['c_resid'] = 'All'  # Tag all categories as 'All'

    # Combine the data back to include FOR, DOM, and All
    combined_data = pd.concat([monthly_sum, all_sum], ignore_index=True)

    # Create the animated line chart
    fig = px.line(
        combined_data,
        x='Year',  # x-axis as Year
        y='Value',  # y-axis as aggregated monthly values
        animation_frame='month',  # Use month for animation
        color='c_resid',  # Color by residency category which includes 'All'
        title=f'Short Stay Dynamic Patterns Across Months and Years',
        labels={'Value': 'Total Numbers', 'Year': 'Year'},
        range_y=[0, combined_data['Value'].max() * 1.1]  # Adjust y-axis range for better visibility
    )
    # Change the legend title to "Type"
    fig.update_layout(legend_title=dict(text='Type'))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)