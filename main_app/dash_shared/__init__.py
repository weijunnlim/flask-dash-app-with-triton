import dash_html_components as html

#nav bar
def shared_dash_nav_links() -> html.Div:
    link_style = {'marginLeft': '10px'}
    links = html.Div(
        id='shared-navigation-links',
        style={'display': 'flex', 'flexWrap': 'wrap', 'marginTop': '15px', 'marginBottom': '15px', 'backgroundColor': 'lightBlue'},
        children=[
            html.Div('These links are part of the dash layout, shared by both applications'),
            html.A(
                href='/',
                children='Home',
                style=link_style
            ),
            html.A(
                href='/app_1',
                children='App 1 As Jinja iFrame',
                style=link_style
            ),
            html.A(
                href='/app_1_raw_dash',
                children='App 1 Native Dash Layout',
                style=link_style
            ),
            html.A(
                href='/non_dash_app',
                children='Non Dash Flask Endpoint',
                style=link_style
            ),
            #writes the name on navbar
            html.A(
                href='/cat_dog',
                children='Cat Dog Prediction',
                style=link_style
            ),
            html.A(
                href='/text_converter',
                children= 'Text Converter',
                style=link_style
            )
        ]
    )
    return links
