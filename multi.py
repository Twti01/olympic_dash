import dash 
from dash import html, dcc, Output, Input, dash_table, callback_context, ALL
from data_proc import dfs, medal_tally, medal_tally_heat, ath 
from plot_fun import olympic_hosts_map, medal_map_figure, medal_heatmap_figure, gauge_figure, empty_figure
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

        html.Div([html.H1("Olympic Games", style={"display": "inline-block", "fontSize": "50px", 'color': 'black', 'fontWeight': 'bold', "margin-bottom": "30px", 'height': "60px", "width": "80%"}),
                  html.Div(dcc.Link(html.Button("Go to Dashboard 2", id="button-secondary-dashboard", style={"fontSize": "20px", "height": "40px", "backgroundColor": "#EECEB9", "float": "right", "margin-right": "5px", "border": "none", "border-radius": "30px", "cursor": "pointer", "fontWeight": "bold"}), href="/dashboard2")
                           , style={"float": "right", "display": "inline-block", "width": "20%", "vertical-align": "top"})],
                 style={"display": "flex", 'backgroundColor': '#BB9AB1', "alignItems": "center", "justifyContent": "space-between", "width": "100%", "height": "60px"}),
html.Div([
        dcc.Dropdown(id="slct_game_season",
                     options=[{'label': "Select season", "value": "All"}]+[{"label": season, "value": season} for season in seasons],
                     multi=False,
                     value="All",
                     style={"width": "280px", "display": "inline-block", "margin-right": "10px" ,"color": "white", "backgroundColor": "#EECEB9"}),
        
        dcc.Dropdown(id="slct_sport",
                     options=[{"label": "Select sport", "value": "All"}]+[{"label": sport, "value": sport} for sport in sports],
                     multi=False,
                     value="All",
                     style={"width": "280px", "display": "inline-block", "margin-right": "10px" ,"color": "white", "backgroundColor": "#EECEB9"}
                     ),

        dcc.Dropdown(id="slct_game",
                     options=[{"label": "Select olympic Game", "value": "All"}]+[{"label": game, "value": game} for game in games],
                     multi=False,
                     value="All",
                     style={"width": "280px", "display": "inline-block", "margin-right": "10px" ,"color": "white", "backgroundColor": "#EECEB9"}
                     ),

        dcc.Dropdown(id="slct_sex",
                     options=[{"label": "Select sex", "value": "All"}]+[{"label": sex, "value": sex} for sex in sexes],
                     multi=False,
                     value="All",
                     style={"width": "280px", "display": "inline-block", "color": "white", "margin-right": "10px", "backgroundColor": "#EECEB9"}
                     ),
        dcc.Dropdown(id="slct_country",
                     options=[{"label": "Select country", "value": "All"}]+[{"label": country, "value": country} for country in countries],
                     multi=False,
                     value="All",
                     style={"width": "280px", "display": "inline-block", "margin-right": "10px", "margin-left": "auto" ,"color": "white", "backgroundColor": "#EECEB9"}
                     ),
        ], style={"display": "flex", "justify-content": "center", "align-items": "center","text-allign": "center", "margin-bottom": "10px", "gap": "10px", "margin-top": "10px"}),


        html.Div([
            html.Div([
                html.H2("Medal Table", style={"color": "black", "backgroundColor": "BB9AB1", "fontWeight": "bold", "fontSize": "26px", "text-align": "center", "margin-top": "10px", "margin-bottom": "4px"}),
                dash_table.DataTable(id='medal_table', 
                                     columns=[{"name": i, "id": i} for i in ["Platzierung","Country", "Gold", "Silber", "Bronze", "Total"]],
                                     data=df2[:10].to_dict("records"),
                                     style_table={'height': '400px', 'overflowY': 'auto', 'fontWeight': 'bold', "display": "block"},
                                     style_header={'backgroundColor': '#BB9AB1', 'color': 'black', "fontWeight": "bold", "fontSize": "18px", "position": "sticky", "top": 0, "zIndex": 2},
                                     style_data={'backgroundColor': '#FEFBD8', 'color': 'black'},
                                     style_cell_conditional=[
                                         {'if': {'column_id': 'Platzierung'},
                                          'width': '10%'},
                                         {'if': {'column_id': 'Country'},
                                          'width': '30%'},
                                         {'if': {'column_id': 'Gold'},
                                          'width': '15%'},
                                         {'if': {'column_id': 'Silber'},
                                          'width': '15%'},
                                         {'if': {'column_id': 'Bronze'},
                                          'width': '15%'},
                                         {'if': {'column_id': 'Total'},
                                          'width': '15%'}])
                                         ], style={"width": "48%", "display": "inline-block", "vertical-align": "top", "overflow": "hidden"}),
            html.Div([
                dcc.Graph(id="medal_heat", figure={}, style={"width": "100%", "display": "inline-block", "vertical-align": "top"})
                ], style={"width": "48%", "display": "inline-block", "vertical-align": "top", "backgroundColor": "#EECEB9", "margin-left": "4%"}),
            html.Div([
                dcc.Graph(id="medal_map", figure={}, style={"width": "44%", "display": "inline-block", "vertical-align": "top", "margin-left": "2%"}),
                dcc.Graph(id='olympic_hosts', figure={}, style={"width": "44%", "display": "inline-block", "vertical-align": "top", "margin-left": "9%"})
                ], style={"width": "100%", "display": "inline-block", "vertical-align": "top", "backgroundColor": "#B6B6B6", "margin-top": "0.8%"}),         
        ]) 

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
     Input(component_id="slct_game_season", component_property="value")] 
        )
def update_medal_table(selected_sport, selected_game, selected_sex, selected_season):
     filtered_df = medal_tally(df2, sport=selected_sport, game=selected_game, sex=selected_sex, season=selected_season)
     return filtered_df.to_dict("records")

@app.callback(
        Output(component_id="medal_map", component_property="figure"),
        [Input(component_id='slct_sport', component_property='value'),
         Input(component_id='slct_game', component_property='value'),
         Input(component_id="slct_sex", component_property="value"),
         Input(component_id="slct_game_season", component_property="value")] 
        )

def update_medal_map(sport, game, sex, season):

    medal_tally_map = medal_tally(df2, sport=sport, game=game, sex=sex, season=season)

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
        athlete_html = html.Div([
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
        return empty_figure("Bitte geben Sie einen Namen ein, um zu suchen.")

    filtered_df = query_athlete_data(ath_name)

    if filtered_df.empty:
        return empty_figure("Kein Athlet gefunden.")

    fig = gauge_figure(filtered_df, ath_name)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
