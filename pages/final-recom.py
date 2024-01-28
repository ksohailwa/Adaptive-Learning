import pandas as pd
import dash_mantine_components as dmc
import dash_core_components as dcc
from dash import Input, Output, State, html, ctx
from dash_iconify import DashIconify
from app import app
from dash_core_components import Dropdown
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy import text
layout = html.Div(
    children=[
        html.Header(
            children=[
                html.H1("Your Recommendation", style={'margin-bottom': '10px'}),
                #html.P("Welcome to our exciting project! Let us recommend you how to learn in the best way!",
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
