import plotly.express as px

def olympic_hosts_map(df, season, game):
    if season != "All":
        df = df[df["game_season"] == season]

    if game != "All":
        df = df[df["game_slug"] == game]


    center_lat = 0
    center_lon = 0

    fig = px.scatter_geo(
            data_frame=df,
            lat="lat",
            lon="lon",
            color="game_year",
            hover_name="game_name",
            hover_data={"lat": False, "lon": False, "game_year": False},
            template="plotly_dark",
            title="Olympic Games since 1896",
            width=1000,
            height=600
            )

    fig.update_geos(projection_type="natural earth",
                    center={"lat": center_lat, "lon": center_lon})

    return fig


def medal_table_figure(df2):
    fig = px.bar(
            df2,
            x="country_name",
            y=["Goldcounter", "Silbercounter", "Bronzecounter"],
            title="Medaillenspiegel",
            labels={"value": "Anzahl an Medaillen", "variable": "Medal Type"},
            template="plotly_dark"
            )
    return fig

def medal_map_figure(df2):
    fig = px.choropleth(
            data_frame=df2,
            locationmode="country names",
            locations="country_name",
            color="Total",
            title="Distribution of medals",
            template="plotly_dark",
            width=1000,
            height=600
            )

    fig.update_geos(projection_type="natural earth")

    return fig



