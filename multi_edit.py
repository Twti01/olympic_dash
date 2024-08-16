import dash 
from dash import html, dcc, Output, Input, dash_table, callback_context, ALL
from data_proc import dfs, medal_tally, medal_tally_heat, ath, medal_tally_bar 
from plot_fun import olympic_hosts_map, medal_map_figure, medal_heatmap_figure, gauge_figure, empty_figure, medal_bar_figure
import plotly.io as pio
from flask import Flask
from ath import create_app2_layout
import pandas as pd
from flask_caching import Cache
import plotly.graph_objects as go

server = Flask(__name__)

app = dash.Dash(__name__,server=server, suppress_callback_exceptions=True)

df, df2 = dfs()

ath = ath()

cache = Cache(app.server, config={"CACHE_TYPE": "simple"})

@cache.memoize(timeout=60)
def query_athlete_data(input):
    filtered_df = ath[ath['athlete_full_name'].str.contains(input, case=False, na=False)]
    return filtered_df


def create_main_layout():

    df, df2 = dfs()

    pio.templates.default = "custom"

    df2['year'] = df2['slug_game'].str.extract(r'(\d{4})').astype(int)

    df2 = df2.sort_values(by='year', ascending=False).reset_index(drop=True)

    df2 = df2.drop(columns='year')

    sports = sorted(df2["discipline_title"].unique())
    games = df2["slug_game"].unique()
    sexes = sorted(df2["event_gender"].unique())
    seasons = sorted(df2["game_season"].unique())
    countries = sorted(df2["country_name"].unique())

    return html.Div([

    html.Div([
        html.H1("Olympic Games", style={"display": "inline-block", "fontSize": "50px", 'color': 'black', 'fontWeight': 'bold', "margin-bottom": "30px", 'height': "60px", "width": "80%", "margin-left": "1%"}),
        html.Div(
            dcc.Link(
                html.Button(
                    "Go to Dashboard 2",
                    id="button-secondary-dashboard",
                    style={"fontSize": "20px", "height": "40px", "backgroundColor": "#EECEB9", "float": "right", "margin-right": "1%", "border": "none", "border-radius": "30px", "cursor": "pointer", "fontWeight": "bold"}
                ),
                href="/dashboard2"
            ),
            style={"float": "right", "display": "inline-block", "width": "20%", "vertical-align": "top", "margin-right": "1%"}
        )
    ],
    style={"display": "flex", 'backgroundColor': '#BB9AB1', "alignItems": "center", "justifyContent": "space-between", "width": "100%", "height": "60px"}),

    html.Div([
        dcc.Dropdown(
            id="slct_game_season",
            options=[{'label': "Select season", "value": "All"}] + [{"label": season, "value": season} for season in seasons],
            multi=False,
            value="All",
            style={"flex": "0.8", "min-width": "160px", "color": "white", "backgroundColor": "#EECEB9", "margin-left": "1%"}
        ),
        dcc.Dropdown(
            id="slct_sport",
            options=[{"label": "Select sport", "value": "All"}] + [{"label": sport, "value": sport} for sport in sports],
            multi=False,
            value="All",
            style={"flex": "0.8", "min-width": "160px", "color": "white", "backgroundColor": "#EECEB9", "margin-left": "1%"}
        ),
        dcc.Dropdown(
            id="slct_game",
            options=[{"label": "Select olympic Game", "value": "All"}] + [{"label": game, "value": game} for game in games],
            multi=False,
            value="All",
            style={"flex": "0.8", "min-width": "160px", "margin-left": "1%", "color": "white", "backgroundColor": "#EECEB9"}
        ),
        dcc.Dropdown(
            id="slct_sex",
            options=[{"label": "Select sex", "value": "All"}] + [{"label": sex, "value": sex} for sex in sexes],
            multi=False,
            value="All",
            style={"flex": "0.8", "min-width": "160px", "color": "white", "margin-left": "1%", "backgroundColor": "#EECEB9"}
        ),
        dcc.Dropdown(
            id="slct_country",
            options=[{"label": "Select country", "value": "All"}] + [{"label": country, "value": country} for country in countries],
            multi=False,
            value="All",
            style={"flex": "0.8", "min-width": "160px", "margin-right": "1%", "margin-left": "1%", "color": "white", "backgroundColor": "#EECEB9"}
        )
    ], style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center", "align-items": "center", "text-align": "center", "margin-bottom": "0.4%", "gap": "10px", "margin-top": "10px"}),

    html.Div([
        html.Div([
            html.H2("Medal Table", style={"color": "black", "backgroundColor": "#FEFBD8", "fontWeight": "bold", "fontSize": "26px", "text-align": "center", "margin-top": "10px", "margin-bottom": "4px"}),
            dash_table.DataTable(
                id='medal_table',
                columns=[{"name": i, "id": i} for i in ["Platzierung", "Country", "Gold", "Silber", "Bronze", "Total"]],
                data=df2[:10].to_dict("records"),
                style_table={'height': '45vh', 'overflowY': 'auto', 'fontWeight': 'bold', "display": "block"},
                style_header={'backgroundColor': '#BB9AB1', 'color': 'black', "fontWeight": "bold", "fontSize": "18px", "position": "sticky", "top": 0, "zIndex": 2},
                style_data={'backgroundColor': '#e0dec8', 'color': 'black'},
                style_cell_conditional=[
                    {'if': {'column_id': 'Platzierung'}, 'width': '10%'},
                    {'if': {'column_id': 'Country'}, 'width': '30%'},
                    {'if': {'column_id': 'Gold'}, 'width': '15%', "backgroundColor": "#FFD700"},
                    {'if': {'column_id': 'Silber'}, 'width': '15%'},
                    {'if': {'column_id': 'Bronze'}, 'width': '15%'},
                    {'if': {'column_id': 'Total'}, 'width': '15%'}
                ],
                style_data_conditional=[
                    {"if": {"column_id": "Gold"}, "backgroundColor": "#694F8E"},
                    {"if": {"column_id": "Silber"}, "backgroundColor": "#B692C2"},
                    {"if": {"column_id": "Bronze"}, "backgroundColor": "#E3A5C7"}
                    ]
            )
            ], style={"width": "45%", "display": "inline-block","flex-wrap": "wrap", "vertical-align": "top", "margin-left": "1%", "margin-top": "20px", "backgroundColor": "#FEFBD8"}),

        html.Div([
            dcc.Graph(id="medal_map", figure={}, style={"width": "100%", "display": "block", "margin-top": "1%", "height": "50vh"}),
        ], style={"width": "54%", "display": "inline-block", "vertical-align": "top", "margin-left": "2%", "height": "50vh", "margin-top": "1%"})
        ], style={"width": "98%", "display": "flex", "flex-grow": "1", "flex-shrink": "1", "height": "50vh", "justify-content": "space-between", "margin-bottom": "2%"}),

    html.Div([
        html.Div([
            dcc.Graph(id="medal_heat", figure={}, style={"width": "100%", "display": "block", "vertical-align": "top", "height": "32vh"})
            ], style={"width": "36%", "height": "32vh","display": "inline-block", "vertical-align": "top", "margin-left": "1%", "backgroundColor": "#FEFBD8"}),

        html.Div([
            dcc.Graph(id='olympic_hosts', figure={}, style={"width": "30%", "height": "32vh", "display": "inline-block", "vertical-align": "top", "margin-right": "6%"}),
            dcc.Graph(id='medal_bar', figure={}, style={"width": "64%", "height": "32vh", "display": "inline-block", "vertical-align": "top"})
        ], style={"width": "63%", "display": "inline-block", "vertical-align": "top", "backgroundColor": "#FEFBD8", "margin-top": "5px", "margin-left": "2%"})
    ], style={"display": "flex", "justify-content": "space-between", "height": "40vh"})
])

@app.callback(
        Output(component_id='olympic_hosts', component_property='figure'),
         [Input(component_id='slct_game_season', component_property='value'),
          Input(component_id='slct_game', component_property="value")]
         )
def update_graph(option_slct, game):
    print(option_slct)
    print(type(option_slct))

    fig = olympic_hosts_map(df, option_slct, game)

    return fig

@app.callback(
       Output(component_id='medal_table', component_property='data'),
    [Input(component_id='slct_sport', component_property='value'),
     Input(component_id='slct_game', component_property='value'),
     Input(component_id="slct_sex", component_property="value"),
     Input(component_id="slct_game_season", component_property="value"),
     Input(component_id="slct_country", component_property="value")] 
        )
def update_medal_table(selected_sport, selected_game, selected_sex, selected_season, selected_country):
     filtered_df = medal_tally(df2, sport=selected_sport, game=selected_game, sex=selected_sex, season=selected_season, country=selected_country)
     return filtered_df.to_dict("records")

@app.callback(
        Output(component_id="medal_map", component_property="figure"),
        [Input(component_id='slct_sport', component_property='value'),
         Input(component_id='slct_game', component_property='value'),
         Input(component_id="slct_sex", component_property="value"),
         Input(component_id="slct_game_season", component_property="value"),
         Input(component_id="slct_country", component_property="value")] 
        )

def update_medal_map(sport, game, sex, season, country):

    medal_tally_map = medal_tally(df2, sport=sport, game=game, sex=sex, season=season, country=country)

    fig = medal_map_figure(medal_tally_map)

    return fig 


@app.callback(
        Output(component_id="medal_heat", component_property="figure"),
        [Input(component_id='slct_sport', component_property='value'),
         Input(component_id='slct_game', component_property='value'),
         Input(component_id="slct_sex", component_property="value"),
         Input(component_id="slct_game_season", component_property="value"),
         Input(component_id="slct_country", component_property="value")] 
        )

def update_medal_heat(selected_sport, selected_game, selected_sex, selected_season, selected_country):
    medal_tally_heat_map = medal_tally_heat(df2, sport=selected_sport, game=selected_game, sex=selected_sex, season=selected_season, country=selected_country)

    fig = medal_heatmap_figure(medal_tally_heat_map)

    return fig

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
        )
def display_page(pathname):
    if pathname == '/dashboard2':
        return create_app2_layout()
    else:
        return create_main_layout()

@app.callback(
    Output('url', 'pathname'),
    [Input({'type': 'button', 'index': ALL}, "n_clicks")]
)

def go_to_dashboard(n_clicks):
    ctx = callback_context

    if not ctx.triggered:
        return "/"

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == '{"type": "button", "index": "secondary-dashboard"}':
        return '/dashboard2'
    elif button_id == '{"type": "button", "index": "home-page"}':
        return '/'


@app.callback(
    Output("info", "children"),
    [Input("athletes", "value")])

def update_output(input):
    if not input:
        return html.Div("Bitte geben Sie einen Namen ein, um zu suchen.")
    
    filtered_df = query_athlete_data(input)
    
    if filtered_df.empty:
        return html.Div("Keine Athleten gefunden.")
    
    # Baue HTML-Inhalte für jeden gefundenen Athleten
    athletes = []
    for _, row in filtered_df.iterrows():
        ath_name = row["athlete_full_name"]
        athlete_html= html.Div([
            html.H2(ath_name),
            html.P(row['bio']),
            html.A("Mehr erfahren", href=row['athlete_url'], target="_blank"),
            html.Div([
                html.P(f"Gold: {row['Gold']}"),
                html.P(f"Silber: {row['Silber']}"),
                html.P(f"Bronze: {row['Bronze']}"),
                html.P(f"Games participated: {row['games_participations']}"),
                html.P(f"First Game: {row['first_game']}")
            ], style={'margin-top': '10px'})
            ], style={'margin-bottom': '20px', 'border': '1px solid #ddd', 'padding': '10px'})
        
        athletes.append(athlete_html)
    
    return athletes

@app.callback(
        Output("gauche_athlete", "figure"),
        [Input("athletes", "value")])

def update_gauche_figure(ath_name):
    if not ath_name:
        return empty_figure("Diese Grafik basiert auf die Suchanfrage.")

    filtered_df = query_athlete_data(ath_name)

    if filtered_df.empty:
        return empty_figure("Kein Athlet gefunden.")

    fig = gauge_figure(filtered_df, ath_name)

    return fig


@app.callback(
        Output(component_id="medal_bar", component_property="figure"),
        [Input(component_id='slct_sport', component_property='value'),
         Input(component_id='slct_game', component_property='value'),
         Input(component_id="slct_sex", component_property="value"),
         Input(component_id="slct_game_season", component_property="value"),
         Input(component_id="slct_country", component_property="value")])

def update_medal_bar_figure(sport, game, sex, season, country):
    medal_df = medal_tally_bar(df2, sport=sport, game=game, sex=sex, season=season, country=country)

    fig = medal_bar_figure(medal_df)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
