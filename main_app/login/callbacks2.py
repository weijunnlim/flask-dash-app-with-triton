from dash.dependencies import Input, Output

def register_callbacks2(dash_app):
    @dash_app.callback(
        Output('url', 'href'),
        Input('signup-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def redirect_to_signup(n_clicks):
        return "/signup/"