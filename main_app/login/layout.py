import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

layout = dbc.Container(
    [
        dcc.Location(id='url', refresh=True),  # Used for redirection
        dbc.Row(
            dbc.Col(
                html.H2("Login"),
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
                        dbc.Button("Login", id="login-button", color="primary"),
                    ],
                    method="POST",
                ),
                width={'size': 6, 'offset': 3}
            )
        ),
        dbc.Row(
            dbc.Col(html.Div(id="login-status"), width={'size': 6, 'offset': 3})
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    dbc.Row(
                        [
                            dbc.Col(html.P("Don't have an account?"), width="auto"),
                            dbc.Col(
                                dbc.Button("Sign Up", id="signup-button", color="secondary", outline=True),
                                width="auto"
                            )
                        ],
                        className="align-items-center"
                    ),
                    className="text-center mt-3"
                ),
                width={'size': 6, 'offset': 3}
            )
        ),
    ],
    style={"marginTop": 50}
)
