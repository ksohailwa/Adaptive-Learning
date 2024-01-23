from app import app
import dash
import dash_html_components as html

# Initialize the Dash app
app = dash.Dash(__name__)

# Define your layout with improved styling
layout = html.Div(
    children=[
        html.Header(
            children=[
                html.H1("Adaptive Learning", style={'margin-bottom': '10px'}),
                html.P("Welcome to our exciting project! Let us recommend you how to learn in the best way!",
                       style={'margin-bottom': '20px'}),
                html.Img(src='..\\assets\\animation.gif', alt="Project Photo",
                         style={'width': '100%', 'margin-bottom': '20px'})
            ],
            style={'text-align': 'center'}
        ),
        html.Section(
            children=[
                html.H2("About us", style={'margin-bottom': '10px'}),
                html.P(
                    "Here, you can find different analyses from students "
                    "--"
                )
            ],
            style={'text-align': 'center', 'margin-bottom': '20px'}
        ),
        html.Section(
            children=[
                html.Img(src='..\\assets\\ibm_logo.png', alt="Project Photo",
                         style={'width': '50%', 'margin-bottom': '20px'})
            ],
            style={'text-align': 'center'}
        )
    ],
    style={'max-width': '800px', 'margin': 'auto'}  # Center the content and limit its width
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
