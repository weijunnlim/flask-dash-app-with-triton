from dash.dependencies import Input, Output, State
from flask_login import login_user
import dash_bootstrap_components as dbc
from main_app.classes.student import Student
from dash.exceptions import PreventUpdate
from werkzeug.security import check_password_hash

def register_callbacks(dash_app):
    @dash_app.callback(
        [Output("login-status", "children"),
         Output('url', 'pathname')],
        [Input("login-button", "n_clicks")],
        [State("username", "value"), State("password", "value")],
        prevent_initial_call=True
    )
    def login_user_dash(n_clicks, username, password):
        if not n_clicks:
            raise PreventUpdate

        student = Student.query.filter_by(username=username).first()

        if student and check_password_hash(student.password, password):
            login_user(student)
            return dbc.Alert("Logged in successfully!", color="success"), '/home/'
        else:
            return dbc.Alert("Invalid username or password", color="danger"), None