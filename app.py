from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

style = ['style.css']

df_nyc = pd.read_csv(
    'https://raw.githubusercontent.com/rafaelnduarte/eds_outliers/master/nyc.csv', index_col=0)

app = Dash(__name__, external_stylesheets=style)

fig = px.scatter(df_nyc, x='longitude', y='latitude',
                 size='price', color='price',
                 )
fig = fig.update_layout(
    paper_bgcolor='rgb(38, 36, 36)',
    font_color="white",
    title_font_color="white",
    legend_title_font_color="white"
)

app.layout = html.Div(
    children=[
        html.H1(children='NYC Airbnb Listings'),
        html.H3(children='Price range'),
        dcc.Input(
            id="input_beggining",
            type='number',
            placeholder="Beginning price",
            value=0,
        ),
        dcc.Input(
            id="input_end",
            type='number',
            placeholder="End price",
            value=10000,
        ),

        dcc.Graph(id='NYC Airbnb', figure=fig),
    ],
)


@app.callback(
    Output(component_id='NYC Airbnb', component_property='figure'),
    Input(component_id='input_beggining', component_property='value'),
    Input(component_id='input_end', component_property='value'),
)
def update_figure(input_beggining, input_end):
    fig = px.scatter(df_nyc.query(f'{input_beggining} < price < {input_end}'),
                     x='longitude', y='latitude',
                     size='price', color='price')

    fig = fig.update_layout(
        paper_bgcolor='rgb(38, 36, 36)',
        font_color="white",
        title_font_color="white",
        legend_title_font_color="white"
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
