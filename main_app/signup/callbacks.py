from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from main_app.classes.student import Student
from dash.exceptions import PreventUpdate
from main_app.extensions import db
from werkzeug.security import generate_password_hash

def register_callbacks(dash_app):
    @dash_app.callback(
        [Output("signup-status", "children"),
         Output('url', 'pathname')],
        [Input("signup-button", "n_clicks")],
        [State("username", "value"), State("password", "value")],
        prevent_initial_call=True
    )
    def register_user_dash(n_clicks, username, password):
        if not n_clicks:
            raise PreventUpdate
        
        if Student.query.filter_by(username=username).first():
            return dbc.Alert("Username already taken", color="danger"), None

        else:
            hashed_password = generate_password_hash(password)
            student = Student(username = username, password = hashed_password)
            db.session.add(student)
            db.session.commit()
            return dbc.Alert("Registered successfully!", color="success"), '/login/'
            