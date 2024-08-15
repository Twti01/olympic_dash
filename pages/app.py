import dash 
from dash import html, dcc, Output, Input, dash_table
from pandas._libs.algos import backfill
from data_proc import dfs, medal_tally, medal_tally_heat
from plot_fun import olympic_hosts_map, medal_map_figure, medal_heatmap_figure
import plot_fun
import plotly.io as pio

app = dash.Dash(__name__)

df, df2 = dfs()

pio.templates.default = "custom"

sports = df2["discipline_title"].unique()
games = df2["slug_game"].unique()
sexes = df2["event_gender"].unique()
seasons = df2["game_season"].unique()
countries = df2["country_name"].unique()

app.layout = html.Div([

    html.H1("Olympic Games", style={"fontSize": "50px", 'color': 'black', 'backgroundColor': '#BB9AB1', 'fontWeight': 'bold','margin-top': "0px", 'height': "60px", "margin-bottom": "20px"}),

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
    ], style={"display": "flex", "justify-content": "center", "align-items": "center","text-allign": "center", "margin-bottom": "20px", "gap": "10px"}),


    html.Div([
        html.Div([
            html.H2("Medal Table", style={"color": "black", "backgroundColor": "BB9AB1", "fontWeight": "bold", "fontSize": "26px", "text-align": "center", "margin-top": "10px", "margin-bottom": "4px"}),
            dash_table.DataTable(id='medal_table', 
                                 columns=[{"name": i, "id": i} for i in ["Platzierung","Country", "Gold", "Silber", "Bronze", "Total"]],
                                 data=df2[:10].to_dict("records"),
                                 style_table={'height': '400px', 'overflowY': 'auto', 'fontWeight': 'bold'},
                                 style_header={'backgroundColor': '#BB9AB1', 'color': 'black', "fontWeight": "bold", "fontSize": "18px"},
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
                                     ], style={"width": "48%", "display": "inline-block", "vertical-align": "top"}),
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

if __name__ == "__main__":
    app.run_server(debug=True)
