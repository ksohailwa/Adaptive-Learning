import dash_mantine_components as dmc
from dash import Input, Output, html, dcc
from dash_iconify import DashIconify

import pages
from app import app

server = app.server

def create_main_nav_link(icon, label, href):
    return dcc.Link(
        dmc.Group(
            #direction='row',
            position='center',
            spacing=10,
            style={'margin-bottom':5},
            children=[
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),
                    size=25,
                    radius=5,
                    color='indigo',
                    variant="filled",
                    style={'margin-left':10}
                ),
                dmc.Text(label, size="sm", color="gray", style={'font-family':'IntegralCF-Regular'}),
            ]
        ),
        href=href,
        style={"textDecoration": "none"},
    )

def create_accordianitem(icon, label, href):
    return dcc.Link(
        dmc.Group(
            #direction='row',
            position='left',
            spacing=10,
            style={'margin-bottom':10},
            children=[
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),
                    size=30,
                    radius=30,
                    color='indigo',
                    variant="light",
                ),
                dmc.Text(label, size="sm", color="gray", style={'font-family':'IntegralCF-Regular'}),
            ]
        ),
        href=href,
        style={"textDecoration": "none"},
    )

app.layout = dmc.MantineProvider(
    id = 'dark-moder', 
    withGlobalStyles=True, 
    children = [
        html.Div(
            children = [

                dmc.Header(
                    height=70,
                    fixed=True,
                    pl=0,
                    pr=0,
                    pt=0,
                    style = {'background-color':'#4B73EF'},
                    children=[

                        dmc.Container(
                            fluid=True,
                            children=[
                                dmc.Group(
                                    position="apart",
                                    align="center",
                                    children=[
                                        dmc.Center(
                                            children=[
                                                dcc.Link(
                                                    dmc.ThemeIcon(
                                                        html.Img(src= '..\\assets\\ibm_logo.png', style={'width':43}),
                                                        radius='sm',
                                                        size=44,
                                                        variant="filled",
                                                        color="gray",
                                                    ),
                                                    href=app.get_relative_path("/"),
                                                ),
                                                dcc.Link(
                                                    href=app.get_relative_path("/"),
                                                    style={"paddingTop": 16, "paddingLeft":10, "paddingBottom":5, "paddingRight":10, "textDecoration": "none"},
                                                    children=[
                                                        dmc.MediaQuery(
                                                            smallerThan="sm",
                                                            styles={"display": "none"},
                                                            children=[
                                                                dmc.Group(
                                                                    #direction='column',
                                                                    align='center', spacing=0, position='center', children=[
                                                                    dmc.Text("AdaptiveLearning", size="xl", color="dark", style={'font-family': 'Arial', 'font-weight': 'bold'}),
                                                                    #dmc.Text("Data Detectives Group", color="lime", size="lg", style={'margin-top': 4, 'font-family': 'Verdana'})
                                                                    ]

                                                                    
                                                                ) 
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                dmc.MediaQuery(
                                                    largerThan="sm",
                                                    styles={"display": "none"},
                                                    children=[

                                                    ]
                                                ),
                                            ]
                                        ),
                                        dmc.Group(
                                            #direction = 'row',
                                            position="right",
                                            align="center",
                                            spacing="md",
                                            children=[
                                                html.Div(id = 'indicatorbox', className = 'indicator-box',
                                                    children=[

                                                    ]
                                                ),
                                                html.A(
 
                                                ),
                                                
                                                html.A(

                                                ),

                                                html.A(
                                                        dmc.ThemeIcon(
                                                        DashIconify(icon = 'mdi:github'),
                                                        color = 'dark'
                                                    ),
                                                    href = 'https://github.com/MaryamMalahnejad/LA--AdaptiveLearning/',
                                                    target ='_blank'

                                                )
                                            ],
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
                dmc.Modal(
                    id = 'the-modal',
                    overflow = 'inside',
                    size = 'xl',
                    children = [
                        
                    ],
                    opened = False
                ),

                dmc.Navbar(
                    fixed=True,
                    width={"base": 300},
                    pl='sm',
                    pr='xs',
                    pt=0,
                    hidden=True,
                    hiddenBreakpoint='sm',
                    children=[
                        dmc.ScrollArea(
                            offsetScrollbars=True,
                            type="scroll",
                            children=[
                                dmc.Group(
                                    #direction = 'column',
                                    align = 'center',
                                    position = 'center',\
                                    spacing = 'xs',
                                    children =[
                                        dmc.Text('Data Detectives Group', style = {'font-family': 'Arial, sans-serif', 'font-style': 'normal'}, size = 'sm'),
                                      #  dmc.Text('----', style = {'font-family':'IntegralCF-RegularOblique'}, size = 'sm')
                                    ]
                                ),
                                
                                dmc.Divider(label='Menu', style={"marginBottom": 20, "marginTop": 5}),
                                dmc.Group(
                                    #direction="column",
                                    children=[
                                        create_main_nav_link(
                                            icon="mdi:home-circle",
                                            label="Home",
                                            href=app.get_relative_path("/"),
                                        ),
                                        create_main_nav_link(
                                            icon="mdi:google-analytics",
                                            label="Analysis",
                                            href=app.get_relative_path("/analysis"),
                                        ),
                                        create_main_nav_link(
                                            icon="mdi:layers-search",
                                            label="Recommendation",
                                            href=app.get_relative_path("/recommendation"),
                                        ),
                                    ],
                                ),
                               
                            ],
                        )
                    ],
                ),

                dcc.Location(id='url'),
                dmc.MediaQuery(
                    largerThan="xs",
                    styles={'height':'100%', 'margin-left':'300px', 'margin-top':70},
                    children = [
                        html.Div(
                            id='content',
                            style={'margin-top':'70px'}
                        )
                    ],
                ),
            ]
        )
    ]
)
@app.callback(Output('content', 'children'),
                [Input('url', 'pathname')])
def display_content(pathname):
    page_name = app.strip_relative_path(pathname)
    if not page_name:  
        return pages.home.layout
    elif page_name == 'analysis':
        return pages.analysis.layout
    elif page_name == 'recommendation':
        return pages.recommendation.layout
    elif page_name == 'finalRecom':
        return pages.finalRecom.layout
    
@app.callback([Output(component_id='liveindicator', component_property='className'),
              Output(component_id='indicatorpulse', component_property='className')],
             [Input(component_id='interval', component_property='n_intervals')])

def update_indicator(n):

    return 'live-indicator', 'indicator-pulse'
if __name__ == '__main__':
    app.run_server(debug=True)
