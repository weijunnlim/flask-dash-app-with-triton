from flask import Blueprint, render_template

server_bp = Blueprint('main', __name__)


@server_bp.route('/')
def index():
    user = {'username': 'User'}
    return render_template("index.html", title='Home Page', user=user)


@server_bp.route('/non_dash_app')
def non_dash_page():
    user = {'username': 'Some Unrelated Non Dash App or Page'}
    return render_template("index.html", title='Non Dash Page', user=user)


@server_bp.route('/app_1/')
def app_1_template():
    return render_template('dash.html', dash_url='/app_1_raw_dash/')


@server_bp.route('/cat_dog/')
def cat_dog_template():
    return render_template('cat_dog.html', dash_url='/cat_dog/')

@server_bp.route('/text_converter/')
def text_converter_template():
    return render_template('cat_dog.html', dash_url='/text_converter/')



