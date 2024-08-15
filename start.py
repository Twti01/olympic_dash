import dash
from dash import html, dcc, Output, Input
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

df = pd.read_csv("olympic_hosts.csv")

print(df[:5])

df2 = pd.read_csv("olympic_medals.csv")

df2 = df2[["slug_game", "event_title", "discipline_title", "event_gender", "medal_type", "participant_type", "athlete_full_name", "country_name"]]

country_mapping = {
        "Russian Federation": "Russia",
        "Soviet Union": "Russia",
        "People's Republic of China": "China",
        "ROC": "China",
        "Federal Republic of Germany": "Germany",
        "Germany": "Germany",
        "German Democratic Republic (Germany)": "Germany",
        "Democratic People's Republic of Korea": "South Korea",
        "Republic of Korea": "South Korea"
        }

mask = df2['country_name'].isin(country_mapping.keys())

df2.loc[mask, "country_name"] = df2.loc[mask, "country_name"].replace(country_mapping)

df2['discipline_event_country'] = df2['discipline_title'] + df2['event_title'] + df2['country_name'] + df2["event_gender"] + df2["participant_type"] + df2["slug_game"]


def sortby(df):
    gold_counts = {}
    silver_counts = {}
    bronze_counts = {}
    gold_result = []
    silver_result = []
    bronze_result = []

    for idx, row in df.iterrows():
        key = row['discipline_event_country']

        #Gold
        if row['medal_type'] == 'GOLD':
            if key not in gold_counts:
                gold_counts[key] = 1
                gold_result.append(1)
            else:
                gold_result.append(0)
        else:
            gold_result.append(0)
        #Silver
        if row['medal_type'] == 'SILVER':
            if key not in silver_counts:
                silver_counts[key] = 1
                silver_result.append(1)
            else:
                silver_result.append(0)
        else:
            silver_result.append(0)
        #Bronze
        if row['medal_type'] == 'BRONZE':
            if key not in bronze_counts:
                bronze_counts[key] = 1
                bronze_result.append(1)
            else:
                bronze_result.append(0)
        else:
            bronze_result.append(0)

    
    return gold_result, silver_result, bronze_result


df2["Gold"], df2["Silber"], df2["Bronze"] = sortby(df2)

df2["Goldcounter"] = df2.groupby("country_name")["Gold"].cumsum()
df2["Silbercounter"] = df2.groupby("country_name")["Silber"].cumsum()
df2["Bronzecounter"] = df2.groupby("country_name")["Bronze"].cumsum()

new_df = df2[["country_name", "Goldcounter", "Silbercounter", "Bronzecounter"]]

print(new_df[:-5])

new_df.to_csv("medals_output.csv")

app.layout = html.Div([

    html.H1("Web application with Dash", style={'text-allign': 'center'}),

    dcc.Dropdown(id="slct_game_season",
                 options=[
                     {'label': "Winter", "value": "Winter"},
                     {"label": "Sommer", "value": "Summer"},
                     {'label': "all", "value": "All"}],
                 multi=False,
                 value="All",
                 style={"width": "40%"}
                 ),

    html.Div(id='Output_container', children=[]),
    html.Br(),

    dcc.Graph(id='olympic_hosts', figure={}),

    html.Div(id="second_container", children=[]),
    html.Br(),
dcc.Graph(id="medal_table", figure={})
])

@app.callback(
        [Output(component_id='Output_container', component_property='children'),
         Output(component_id='olympic_hosts', component_property='figure')],
         [Input(component_id='slct_game_season', component_property='value')]
    )
def update_graph(option_slct):
    print(option_slct)
    print(type(option_slct))

    container = "The season chosen by user was: {}".format(option_slct)

    dff = df.copy()
    if option_slct != "All":
        dff = dff[dff['game_season'] == option_slct]

    fig = px.scatter_geo(
            data_frame=dff,
            lat="lat",
            lon="lon",
            color="game_year",
            hover_name="game_name",
            hover_data={"lat": False, "lon": False, "game_year": False},
            template="plotly_dark",
            title="Olympic Games since 1896",
            width=1000,
            height=400
            )

    return container, fig


@app.callback([Output(component_id="medal_table", component_property="figure")],
        [Input(component_id="slct_game_season", component_property="value")]
    )

def medal_graph():
    pass



if __name__ == "__main__":
    app.run_server(debug=True)
