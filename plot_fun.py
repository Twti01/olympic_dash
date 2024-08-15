import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from functools import reduce
from turfpy.measurement import bbox
from dash import html

color_palette = ["#c3abdb", "#6d16c4"]   #FEFBD8, "#EECEB9", "#ccb541", "#BB9AB1", "#987D9A"
heat_color_palette = ["#E3A5C7", "#B692C2", "#694F8E"]
pio.templates["custom"] = go.layout.Template(
layout = {
        "title":
        {
            "font": {"family": "Sans-serif",
                     "size": 30,
                     "color": "black"}
            },
        "font": {"family": "Sans-serif",
                 "size": 16,
                 "color": "black"},
        "colorway": color_palette,
        "geo": {
            "bgcolor": "#FEFBD8",
            "lakecolor": "white",
            "landcolor": "#EBE9E8",
            "showland": True,
            "subunitcolor": "white",
            "countrycolor": "black"
            },
            "paper_bgcolor": "#FEFBD8",
            "plot_bgcolor": "#FEFBD8",
        })
    

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
            hover_name="game_name",
            hover_data={"lat": False, "lon": False, "game_year": False},
            template="custom",
            color_discrete_sequence=[color_palette[-1]]
            )

    fig.update_geos(projection_type="natural earth",
                    center={"lat": center_lat, "lon": center_lon}
                    )
    fig.update_traces(marker=dict(size=6))

    fig.update_layout(
            autosize=True,
            margin=dict(l=10, r=0, t=30, b=0),
            title=dict(y=0.95)
            )

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
            template="custom",
            color_continuous_scale=color_palette,
            range_color=[df2["Total"].min(), df2["Total"].max()]
            )

    fig.update_geos(projection_type="natural earth")


    fig.update_layout(
            autosize=True,
            margin=dict(l=10, r=10, t=0, b=0),
            )

    fig.update_traces(
            hovertemplate="<b>Land:</b> %{location}<br><b>Anzahl der gesammelten Medaillen:</b> %{z}<extra></extra>"
            )

    return fig

def medal_heatmap_figure(medal_heat):
    fig = go.Figure(go.Heatmap(
        z=medal_heat[["Gold", "Silber", "Bronze"]].values.T,
        x=medal_heat["country_3_letter_code"],
        y=["Gold", "Silber", "Bronze"],
        colorscale=heat_color_palette,
        ))
    fig.update_layout(paper_bgcolor="#FEFBD8",
                      title_font=dict(size=24, color="black", family="Sans-serif"),
                      )
    return fig

def pie_ath_figure(ath):
    fig = px.pie(ath,
                 values="percentage",
                 names="medal_type",
                 title="Medal chances for athletes",
                 color="medal_type",
                 color_discrete_map={
                     "Gold": heat_color_palette[2], 
                     "Silber": "#c3abdb",
                     "Bronze": heat_color_palette[0],
                     "No Medal": "FEFBD8"
                     })

    fig.update_layout(paper_bgcolor='#BB9AB1',
                      plot_bgcolor='#BB9AB1')
    return fig


def gauge_figure(ath, athlete_name):


    if ath.empty:
        return empty_figure("Diese Grafik basiert auf die Suchanfrage.")

    athlete_data = ath.iloc[0]

    ath_gold = athlete_data.get("Gold", 0)
    ath_silber = athlete_data.get("Silber", 0)
    ath_bronze = athlete_data.get("Bronze", 0)

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=ath_gold,
        title={"text": "Gold Medals"},
        gauge={
            "axis": {"range": [0, 23]},
            "bar": {"color": "gold"},
            "steps": [
                {"range": [0, 23], "color": "lightyellow"}
                ],
            "threshold": {
                "line": {"color": "darkgoldenrod", "width": 4},
                "thickness": 0.75,
                "value": ath_gold
                }
            },
        domain={"x": [0, 0.25], "y": [0, 1]}

        ))
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=ath_silber,
        title={"text": "Silver Medals"},
        gauge={
            "axis": {"range": [0, 6]},
            "bar": {"color": "silver"},
            "steps": [
                {"range": [0, 6], "color": "lightgrey"}
                ],
            "threshold": {
                "line": {"color": "grey", "width": 4},
                "thickness": 0.75,
                "value": ath_silber
                }
            },
        domain={"x": [0.38, 0.62], "y": [0, 1]}

        ))
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=ath_bronze,
        title={'text': "Bronze Medals"},
        gauge={
            'axis': {'range': [0, 6]},
            'bar': {'color': "darkgoldenrod"},
            'steps': [
                {'range': [0, 6], 'color': "#e6b78c"}
            ],
            'threshold': {
                'line': {'color': "brown", 'width': 4},
                'thickness': 0.75,
                'value': ath_bronze
            }
        },
        domain={'x': [0.75, 1], 'y': [0, 1]}
    ))

    fig.update_layout(
            title={"text": f'Medal Count for {athlete_name}',
                   "y": 0.95,
                   "x": 0.5,
                   "xanchor": "center",
                   "yanchor": "top",
                   "pad": {"b": 10}},
            autosize=False,
            margin=dict(l=50, r=50, b=50, t=120, pad=4),
            paper_bgcolor="#c3abdb",
            plot_bgcolor="#c3abdb"
        )

    return fig

def empty_figure(message):
    # Erzeugt eine leere Figur mit einer benutzerdefinierten Nachricht
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=20)
    )
    fig.update_layout(
        xaxis=dict(showticklabels=False, zeroline=False, showgrid=False),
        yaxis=dict(showticklabels=False, zeroline=False, showgrid=False),
        paper_bgcolor="#c3abdb",
        plot_bgcolor="#c3abdb"
    )
    return fig


def medal_bar_figure(df2):

    df_melted = df2.melt(id_vars=["country_3_letter_code"], value_vars=["Bronze", "Silber", "Gold"],
                             var_name="Medal", value_name="Count")

    fig = px.bar(df_melted, 
                 x="country_3_letter_code",
                 y="Count",
                 color="Medal",
                 color_discrete_map={"Gold": heat_color_palette[2], "Silber": heat_color_palette[1], "Bronze": heat_color_palette[0]}
                 )

    fig.update_xaxes(title_text="")

    return fig



