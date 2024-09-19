import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

layout = dbc.Container(
    [
        dcc.Location(id='url', refresh=True),  
        dbc.Row(
            dbc.Col(
                html.H2("Sign Up"),
                width={'size': 6, 'offset': 3},
                className="text-center"
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Form(
                    [
                        dbc.CardGroup(
                            [
                                dbc.Label("Username", html_for="username"),
                                dbc.Input(type="text", id="username", placeholder="Enter your username", size=32),
                            ]
                        ),
                        dbc.CardGroup(
                            [
                                dbc.Label("Password", html_for="password"),
                                dbc.Input(type="password", id="password", placeholder="Enter your password", size=32),
                            ]
                        ),
                        dbc.Button("Sign Up", id="signup-button", color="primary"),
                    ],
                    method="POST",
                ),
                width={'size': 6, 'offset': 3}
            )
        ),
        dbc.Row(
            dbc.Col(html.Div(id="signup-status"), width={'size': 6, 'offset': 3})
        ),
    ],
    style={"marginTop": 50}
)
