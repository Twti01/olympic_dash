import dash
from dash import dash_table, html, dcc
from dash.dash_table.DataTable import DataTable
from data_proc import ath, ath_med, ath_medal_table
from plot_fun import pie_ath_figure

df = ath()

ath_df = ath_med(df)

ath_df2 = ath_medal_table(df)

fig_ath = pie_ath_figure(ath_df)

def create_app2_layout():
    return html.Div([
            # Header mit Titel und Button
            html.Div([
                html.H1(
                    "Olympic Games",
                    style={"display": "inline-block", "fontSize": "50px", 'color': 'black', 'fontWeight': 'bold', "width": "80%", "margin-top": "36px", "margin-left": "1%"}
                ),
                html.Div(
                    dcc.Link(
                        html.Button(
                            "Go to Main Dashboard",
                            id="home-page-button",
                            style={
                                "fontSize": "20px", "height": "40px", "backgroundColor": "#EECEB9", "border": "none", "border-radius": "30px", "cursor": "pointer", "fontWeight": "bold"
                            }
                        ), href="/"
                    ),
                    style={"float": "right", "width": "12%", "margin-right": "1%"}
                )
            ], style={
                "display": "flex", 'backgroundColor': '#BB9AB1', "alignItems": "center", "justifyContent": "space-between", "width": "100%", "height": "60px"}
            ),

            # Suchleiste unter dem Header
            html.Div([
                dcc.Input(
                    id="athletes",
                    type="text",
                    placeholder="Search for an athlete",
                    style={"fontSize": "20px", "height": "40px", "backgroundColor": "#EECEB9", "border": "#BB9AB1", "fontWeight": "bold", "width": "40%", "margin-top": "10px", "margin-left": "1%"}
                )
            ], style={"width": "100%", "display": "flex"}),

            # Hauptinhalt: Info-Box und Graphen
            html.Div([
                # Scrollbare Info-Box
                html.Div(
                    id="info",
                    style={
                        "width": "40%", "height": "80vh", "overflowY": "auto", "backgroundColor": "#FEFBD8", "padding": "10px", "box-sizing": "border-box", "float": "left", "margin-left": "0.5%"
                    }
                ),
                # Container für die Graphen
                html.Div([
                    html.Div(
                        dcc.Graph(id="ath_pie", figure=fig_ath, style={"width": "100%", "height": "34vh"}),
                        style={"width": "38%", "height": "34vh", "display": "inline-block", "vertical-align": "top"}
                    ),
                    html.Div(
                        dcc.Graph(id="gauche_athlete", figure={}, style={"width": "100%", "height": "34vh"}),
                        style={"width": "60%", "height": "34vh", "display": "inline-block", "vertical-align": "top", "margin-left": "2%"}
                    ),
                    html.Div([
                        dash_table.DataTable(
                        id='ath_table',
                        columns=[
                                {"name": "Platzierung", "id": "Platzierung"},
                                {"name": "Athlete", "id": "athlete_full_name"},
                                {"name": "Games Participations", "id": "games_participations"},
                                {"name": "Gold", "id": "Gold"},
                                {"name": "Silber", "id": "Silber"},
                                {"name": "Bronze", "id": "Bronze"}],
                        data=ath_df2[:500].to_dict("records"),
                        page_action="none",
                        style_table={"width": "100%", "display": "flex", "overflowY": "auto", "height": "44vh", "fontWeight": "bold"},
                        style_header={'backgroundColor': '#BB9AB1', 'color': 'black', "fontWeight": "bold", "fontSize": "18px", "position": "sticky", "top": 0, "zIndex": 2},
                        style_data={'backgroundColor': '#e0dec8', 'color': 'black'},
                        style_cell={"minwidth": "80px", "whiteSpace": "normal", "textOverflow": "ellipsis"},
                        style_cell_conditional=[
                            {'if': {'column_id': 'Platzierung'}, 'width': '10%'},
                            {'if': {'column_id': 'Athlete'}, 'width': '35%'},
                            {'if': {'column_id': 'Games Participations'}, 'width': '10%'},
                            {'if': {'column_id': 'Gold'}, 'width': '15%', "backgroundColor": "#FFD700"},
                            {'if': {'column_id': 'Silber'}, 'width': '15%'},
                            {'if': {'column_id': 'Bronze'}, 'width': '15%'}],
                        style_data_conditional=[
                            {"if": {"column_id": "Gold"}, "backgroundColor": "#694F8E"},
                            {"if": {"column_id": "Silber"}, "backgroundColor": "#B692C2"},
                            {"if": {"column_id": "Bronze"}, "backgroundColor": "#E3A5C7"}
                            ])
                        ], style={"width": "100%", "height": "44vh", "position": "absolute", "bottom": "0"})
                    ], style={"width": "55%", "height": "80vh", "float": "right", "display": "flex", "justify-content": "space-between", "position": "relative", "margin-right": "1%"}),
                ], style={"width": "100%", "height": "100vh","display": "flex", "justify-content": "space-between", "margin-top": "10px"})], 
            style={"width": "100%"})
