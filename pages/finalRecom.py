import dash_html_components as html
import dash
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

layout = html.Div(
    [
        html.H1("HI"),
    ]
)

@app.callback(Output('url', 'pathname'), Input('url', 'pathname'))
def display_page(pathname):
    return pathname

if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True)
