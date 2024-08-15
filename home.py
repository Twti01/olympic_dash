import dash 
from dash import html, dcc, Output, Input, dash_table
from pandas._libs.algos import backfill
from data_proc import dfs, medal_tally
from plot_fun import olympic_hosts_map, medal_map_figure

app = dash.Dash(__name__, pages_folder="pages", use_pages=True)

app.layout = html.Div([
    html.Br(),
    html.P("Multi-Page Dash-Plotly Web App", className="text-dark"),
    html.Div(children=[
        dcc.Link(page["name"], href=page["relative_path"], className="btn")\
                for page in dash.page_registry.values()
        ]),
    dash.page_container
    ], className="col-8")

if __name__ == "__main__":
    app.run(debug=True)

