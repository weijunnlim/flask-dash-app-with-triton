from flask import Blueprint, render_template
from main_app.dash_shared import shared_dash_nav_links

server_bp = Blueprint('main', __name__)


@server_bp.route('/home/')
def home_template():
    navbar = shared_dash_nav_links()
    user = {'username': 'User'}
    return render_template('index.html', dash_url='/home/', user=user, navbar = navbar)


@server_bp.route('/cat_dog/')
def cat_dog_template():
    navbar = shared_dash_nav_links()
    return render_template('dash.html', dash_url='/cat_dog/', navbar = navbar)

@server_bp.route('/text_converter/')
def text_converter_template():
    navbar = shared_dash_nav_links()
    return render_template('dash.html', dash_url='/text_converter/', navbar = navbar)

@server_bp.route('/stroke_predictor/')
def stroke_predictor_template():
    navbar = shared_dash_nav_links()
    return render_template('dash.html', dash_url='/stroke_predictor/', navbar = navbar)


@server_bp.route('/table/')
def table_template():
    navbar = shared_dash_nav_links()
    return render_template('dash.html', dash_url='/table/', navbar = navbar)



