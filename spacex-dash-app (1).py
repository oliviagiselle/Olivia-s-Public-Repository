print("✅ Script is running...")


# Import libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
min_payload = int(spacex_df['Payload Mass (kg)'].min())
max_payload = int(spacex_df['Payload Mass (kg)'].max())


# Create dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[
   html.H1('SpaceX Launch Records Dashboard',
           style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
  
   # TASK 1: Add a dropdown list to enable Launch Site selection
   dcc.Dropdown(
       id='site-dropdown',
       options=[
           {'label': 'All Sites', 'value': 'ALL'},
           {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
           {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
           {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
           {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
       ],
       value='ALL',
       placeholder="All Sites",
       searchable=True
   ),
   html.Br(),


   # TASK 2: Add a pie chart to show the total successful launches count for all sites
   html.Div(dcc.Graph(id='success-pie-chart')),
   html.Br(),


   # TASK 3: Add a slider to select payload range
   html.P("Payload range (Kg):"),
   dcc.RangeSlider(
       id='payload-slider',
       min=min_payload,
       max=max_payload,
       step=1000,
       marks={i: f'{i}' for i in range(0, int(max_payload) + 1, 2500)},
       value=[min_payload, max_payload]
   ),
   html.Br(),


   # TASK 4: Add a scatter chart to show the correlation between payload and launch success
   html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])




# Callback for Pie Chart (TASK 2)
@app.callback(
   Output(component_id='success-pie-chart', component_property='figure'),
   Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
   if entered_site == 'ALL':
       # For all sites, group by Launch Site and count the number of successful launches (class=1)
       filtered_df = spacex_df[spacex_df['class'] == 1]
       fig = px.pie(
           filtered_df,
           names='Launch Site',
           title='Total Successful Launches by Site'
       )
       return fig
   else:
       # Filter dataframe for the selected site
       site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
       # Count number of successes and failures
       site_counts = site_df['class'].value_counts().reset_index()
       site_counts.columns = ['Outcome', 'Count']
       site_counts['Outcome'] = site_counts['Outcome'].map({1: 'Success', 0: 'Failure'})
      
       fig = px.pie(
           site_counts,
           values='Count',
           names='Outcome',
           title=f'Success vs Failure for site {entered_site}'
       )
       return fig




# Callback for Scatter Plot (TASK 4)
@app.callback(
   Output(component_id='success-payload-scatter-chart', component_property='figure'),
   [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
   low, high = payload_range
   payload_filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                                   (spacex_df['Payload Mass (kg)'] <= high)]
  
   if selected_site == 'ALL':
       fig = px.scatter(
           payload_filtered_df,
           x='Payload Mass (kg)',
           y='class',
           color='Booster Version Category',
           title='Correlation between Payload and Success for All Sites'
       )
   else:
       site_df = payload_filtered_df[payload_filtered_df['Launch Site'] == selected_site]
       fig = px.scatter(
           site_df,
           x='Payload Mass (kg)',
           y='class',
           color='Booster Version Category',
           title=f'Correlation between Payload and Success for {selected_site}'
       )
  
   return fig


print("🚀 Loaded Data:")
print(spacex_df.head())
print("🧩 Columns:", spacex_df.columns.tolist())
print("📍 Unique Launch Sites:", spacex_df['Launch Site'].unique())


# Run the app
if __name__ == '__main__':
   app.run(debug=True)