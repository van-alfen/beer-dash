
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc


# beer data
url = 'https://raw.githubusercontent.com/plotly/datasets/master/beers.csv'
df = pd.read_csv(url)
df

# make a table just for the breweries
# counts the number of beers per brewery
# and the average alcohol content of their beers
breweries_df = df.groupby('brewery').agg(
	num_beers=('beer', 'count'),
	avg_abv=('abv', 'mean')
)
breweries_df.reset_index(inplace=True)
# rename better column names
breweries_df.rename(
	columns={
		'num_beers': 'Number of Beers',
		'avg_abv': 'Average ABV',
	},
	inplace=True,
)
breweries_df

# create a column for color based on abv
med_filter = breweries_df['Average ABV'].between(0.05, 0.06)
high_filter = breweries_df['Average ABV'] > 0.06
breweries_df['abv_color'] = 'Low ABV'
breweries_df.loc[med_filter, 'abv_color'] = 'Avg ABV'
breweries_df.loc[high_filter, 'abv_color'] = 'High ABV'
breweries_df

# list of unique breweries for dropdown
brewery_list = df['brewery'].unique().tolist()
brewery_list


# instantiate app
app = Dash( __name__, external_stylesheets=[dbc.themes.FLATLY] )
server = app.server
app.title = 'Beer'


# the dropdown element
the_dropdown = dcc.Dropdown(
	id='brewery-dropdown',
	options=[
		{'label': brewery, 'value': brewery}
		for brewery in brewery_list
	],
	multi=True,
	value=['Big Muddy Brewing', 'Moab Brewery'],
	className='mt-5',
)

# the radio items element
the_radio_items = dbc.RadioItems(
	id='variable-radio',
	options=[
		{'label': 'Number of Beers', 'value': 'Number of Beers'},
		{'label': 'Average ABV', 'value': 'Average ABV'},
	],
	value='Number of Beers',
	class_name='mt-3',
)

# the data description element
the_data_description = dbc.Accordion(
	children=[
		dbc.AccordionItem(
			children=[
				html.P( 'An adequate description of beer.' ),
				html.Img( src='assets/giphy.gif', width='100%' ),
			],
			title='Data Description',
		),
	],
	start_collapsed=True,
	class_name='mt-3',
)

# the column for the first row
first_col = dbc.Col(
	children=[
		# title
		html.H1('Breweries', className='text-center mt-3'),

		dcc.Graph(
			id='bar-chart',
			config={'displayModeBar': False},
		),
	],
	width=8,
)

# the column for the second row
second_col = dbc.Col(
	children=[

		the_dropdown,

		the_radio_items,

		the_data_description,

	],
	width=4,
)


# the app layout
app.layout = dbc.Container(
	children=[

		dbc.Row( first_col, justify='center' ),

		dbc.Row( second_col, justify='center' ),
	],
	fluid=True,
)


@app.callback(
	Output('bar-chart', 'figure'),
	Input('brewery-dropdown', 'value'),
	Input('variable-radio', 'value'),
)
def update_bar_chart(breweries, variable):

	# filter the data
	brew_filter = breweries_df['brewery'].isin(breweries)
	filtered_df = breweries_df[brew_filter]

	# make the bar chart
	fig = px.bar(
		filtered_df,
		x=variable,
		y='brewery',
		orientation='h',
		text='brewery',
		# text_auto=True,
		color='abv_color',
		color_discrete_map={
			'Low ABV': 'DarkRed',
			'Avg ABV': 'DarkOrange',
			'High ABV': 'DarkGreen',
		},
		# category orders, particularly for the legend
		category_orders={
			'abv_color': ['Low ABV', 'Avg ABV', 'High ABV'],
		},
	)

	fig.update_layout(
		# remove the margins
		margin=dict(l=0, r=0, t=0, b=0),
		# remove the title from the legend
		legend_title_text='',
		# move the legend to the top left
		legend_yanchor='bottom',
		legend_y=1,
		legend_xanchor='left',
		legend_x=0,
		# one row legend
		legend_orientation='h',
		# legend style
		legend_bordercolor='black',
		legend_borderwidth=1,
	)

	# no y axis title or ticks
	fig.update_yaxes(
		title_text='',
		showticklabels=False,
		categoryorder='total ascending',
	)

	# increase the font size of the x axis title and ticks
	fig.update_xaxes(
		title_font_size=20,
		tickfont_size=20,
	)

	# update the text details on the bars
	fig.update_traces(
		# textposition='outside',
		textfont_size=20,
	)

	# remove the hover tools


	# return the figure
	return fig


# run the app
if __name__ == '__main__':
	app.run_server(debug=True)


