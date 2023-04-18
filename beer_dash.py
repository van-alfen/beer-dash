
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc


# url for data
url = 'https://raw.githubusercontent.com/plotly/datasets/master/beers.csv'
df = pd.read_csv(url)
df

# make a table just for breweries
# counts the number of beers per brewery
# and the average abv
breweries_df = df.groupby('brewery').agg(
	num_beers=('beer', 'count'),
	avg_abv=('abv', 'mean')
)
breweries_df.reset_index(inplace=True)
# rename columns
breweries_df.rename(
	columns={
		'num_beers': 'Number of Beers',
		'avg_abv': 'Average ABV'
	},
	inplace=True
)
breweries_df

# make a list of breweries for the dropdown
breweries = breweries_df['brewery'].unique().tolist()
breweries



# instantiate app
app = Dash( __name__, external_stylesheets=[dbc.themes.FLATLY] )
app.title = 'Beer'


# the dropdown element
the_dropdown = dcc.Dropdown(
	id='brewery-dropdown',
	options=[
		{'label': brewery, 'value': brewery}
		for brewery in breweries
	],
	multi=True,
	value=['Big Muddy Brewing', 'Moab Brewery']
)

# the radio items element
the_radio_items = dbc.RadioItems(
	id='variable-radio',
	options=[
		{'label': 'Number of Beers', 'value': 'Number of Beers'},
		{'label': 'Average ABV', 'value': 'Average ABV'}
	],
	value='Number of Beers',
	class_name='mt-3'
)


# the bar chart column
bar_chart_column = dbc.Col(
	dcc.Graph(id='bar-graph'),
	width={'size': 6, 'offset': 1}
)

# the interactions column (components)
interactions_col = dbc.Col(
	children=[
		# the dropdown
		the_dropdown,

		# the radio items
		the_radio_items,
	],
	width=3,
	align='center',
)



# the app layout
app.layout = dbc.Container(
	children=[
		html.H1('Breweries'),

		# my row with two cols
		dbc.Row(
			children=[
				# the bar chart column
				bar_chart_column,

				# the interactions column
				interactions_col,
			],
		),		
	],
	fluid=True,
)


@app.callback(
	Output('bar-graph', 'figure'),
	Input('brewery-dropdown', 'value'),
	Input('variable-radio', 'value')
)
def update_bar_chart(breweries, variable):
	# filter the breweries
	brew_filter = breweries_df['brewery'].isin(breweries)
	filtered_df = breweries_df[brew_filter]

	# make the figure
	fig = px.bar(
		data_frame=filtered_df,
		x=variable,
		y='brewery',
		orientation='h',
	)
	# remove y axis title
	fig.update_yaxes(title_text='')

	# return the figure
	return fig


# run the app
if __name__ == '__main__':
	app.run_server(debug=True)


