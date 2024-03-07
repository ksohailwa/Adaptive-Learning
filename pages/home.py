from app import app
import dash
import dash_html_components as html

app = dash.Dash(__name__)
layout = html.Div(
    children=[
        html.Header(
            children=[
                
                html.H1("Welcome to Adaptive Learning!", style={'margin-bottom': '10px'}),
                html.P("Meet our dynamic Master's team – Bahareh, Shima, Maryam, Sohail, Qintha, and 2 Mohammed We're thrilled to introduce our project designed to transform your learning experience.", style={'margin-bottom': '1px'}),
                html.Img(src='..\\assets\\animation.gif', alt="Project Photo",
                         style={'width': '100%'})
            ],
            style={'text-align': 'center'}
        ),
        html.Section(
            children=[
                html.H1("About the Project", style={'margin-bottom': '10px'}),
                html.P("Adaptive Learning – a personalized journey tailored just for you. Answer a few questions, and our machine learning algorithms identify your academic peers, providing personalized recommendations.", style={'margin-bottom': '10px'}),
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
    style={'max-width': '800px', 'margin': 'auto'}  
)

if __name__ == '__main__':
    app.run_server(debug=True)
