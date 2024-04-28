import dash
from dash import dcc, html, Output, Input, State
import dash_labs as dl
import dash_bootstrap_components as dbc

# Use a dark theme from dash_bootstrap_components
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.DARKLY], use_pages=True
)

# Define the offcanvas layout
offcanvas = html.Div(
    [
        dbc.Button("≡", id="open-offcanvas", n_clicks=0, style={"backgroundColor": "rgb(26, 118, 255)", "color": "#FFFFFF"}),
        dbc.Offcanvas(
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(page["name"], href=page["path"])
                    for page in dash.page_registry.values()
                    if page["module"] != "pages.not_found_404"
                ]
            ),
            id="offcanvas",
            is_open=False,
            style={ "backgroundColor": "#000000"},
        ),
    ],
    className="my-3"
)

# Define the app layout with a black background
app.layout = dbc.Container([
   html.Div([
    offcanvas,
    html.H1('Library Management Dashboard', style={'textAlign': 'center', 'color': '#FFFFFF', 'display': 'inline-block','paddingLeft':'400px', 'marginRight': '30px'}),  # Add Library Management System text
], className="d-flex justify-content-space-around align-items-center text-white p-4"),
    dash.page_container,
    dcc.Location(id='url', refresh=False)  # Location component to track page URL
], fluid=True, style={'backgroundColor': '#000000'})  # Set background color to black

# Callback to toggle the offcanvas
@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open



# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8001)
