import dash_bootstrap_components as dbc
import dash_html_components as html

def shared_dash_nav_links() -> dbc.Navbar:
    # Define link style
    link_style = {'marginLeft': '10px', 'color': 'white'}
    
    # Create Navbar items
    nav_items = [
        dbc.NavItem(dbc.NavLink('Cat Dog Prediction', href='/cat_dog', style=link_style, external_link=True)),
        dbc.NavItem(dbc.NavLink('Text Converter', href='/text_converter', style=link_style, external_link=True)),
        dbc.NavItem(dbc.NavLink('Stroke Predictor', href='/stroke_predictor', style=link_style, external_link=True)),
        dbc.NavItem(dbc.NavLink('Table', href='/table', style=link_style, external_link=True)),
    ]

    # Add brand/logo text
    brand = dbc.NavbarBrand("Home", href="/home", style={"color": "white", "fontWeight": "bold"}, external_link=True)

    # Create the Navbar
    navbar = dbc.Navbar(
        dbc.Container([
            dbc.Row(
                [
                    dbc.Col(brand, width="auto"),  
                    dbc.Col(dbc.Nav(nav_items, navbar=True), width="auto"),  
                ],
                align="center"
            ),
        ]),
        color="dark",  
        dark=True,  
        sticky="top",  
        className="mb-4",
    )

    return navbar
