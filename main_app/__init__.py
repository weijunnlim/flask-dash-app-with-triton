from flask import Flask, request, url_for
from flask.helpers import get_root_path
from dash import Dash
from os import getpid
from dash_bootstrap_components.themes import BOOTSTRAP
#import dash_auth
from flask_login import LoginManager, current_user
from main_app.routes import server_bp
from main_app.classes.student import Student
import flask
from main_app.extensions import db

# VALID_USERNAME_PASSWORD_PAIRS = {
#     'hello': 'world'
# }

def create_app(dash_debug, dash_auto_reload):
    server = Flask(__name__, static_folder='static')

    # configure flask app/server here
    server.config.from_object('config.Config')

    #Set up Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(server)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Student.query.get(user_id)
    
    server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(server)
    

    #register all dash apps
    from main_app.home.layout import layout as home_layout
    from main_app.home.callbacks import register_callbacks as home_callbacks
    register_dash_app(
        flask_server=server,
        title='Home Page',
        base_pathname='home',
        layout=home_layout,
        register_callbacks_funcs=[home_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )

    from main_app.cat_dog.layout import layout as cat_dog_layout
    from main_app.cat_dog.callbacks import register_callbacks as cat_dog_callbacks
    register_dash_app(
        flask_server=server,
        title='Cat Dog Prediction',
        base_pathname='cat_dog',
        layout=cat_dog_layout,
        register_callbacks_funcs=[cat_dog_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )

    from main_app.text_converter.layout import layout as text_converter_layout
    from main_app.text_converter.callbacks import register_callbacks as text_converter_callbacks
    register_dash_app(
        flask_server=server,
        title='Text Converter',
        base_pathname='text_converter',
        layout=text_converter_layout,
        register_callbacks_funcs=[text_converter_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )

    from main_app.stroke_predictor.layout import layout as stroke_predictor_layout
    from main_app.stroke_predictor.callbacks import register_callbacks as stroke_predictor_callbacks
    register_dash_app(
        flask_server=server,
        title='Stroke Predictor',
        base_pathname='stroke_predictor',
        layout=stroke_predictor_layout,
        register_callbacks_funcs=[stroke_predictor_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )

    from main_app.table.layout import layout as table_layout
    from main_app.table.callbacks import register_callbacks as table_callbacks
    register_dash_app(
        flask_server=server,
        title='Table',
        base_pathname='table',
        layout=table_layout,
        register_callbacks_funcs=[table_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )

    from main_app.meta_sam2.layout import layout as meta_sam2_layout
    from main_app.meta_sam2.callbacks1 import register_image_upload_callback as meta_sam2_callbacks1
    from main_app.meta_sam2.callbacks2 import segmented_image_callback as meta_sam2_callbacks2
    register_dash_app(
        flask_server=server,
        title='Meta SAM2',
        base_pathname='meta_sam2',
        layout=meta_sam2_layout,
        register_callbacks_funcs=[meta_sam2_callbacks1, meta_sam2_callbacks2],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )


    from main_app.login.layout import layout as login_layout
    from main_app.login.callbacks import register_callbacks as login_callbacks
    from main_app.login.callbacks2 import register_callbacks2 as login_callbacks2
    register_dash_app(
        flask_server=server,
        title='Login',
        base_pathname='login',
        layout=login_layout,
        register_callbacks_funcs=[login_callbacks, login_callbacks2],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )

    from main_app.signup.layout import layout as signup_layout
    from main_app.signup.callbacks import register_callbacks as signup_callbacks
    register_dash_app(
        flask_server=server,
        title='Signup',
        base_pathname='signup',
        layout=signup_layout,
        register_callbacks_funcs=[signup_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )



    # register extensions here
    register_blueprints(server)

    # if running on gunicorn with multiple workers this message should print once for each worker if preload_app is set to False
    print(f'Flask With Dash Apps Built Successfully with PID {str(getpid())}.')
    return server


def register_dash_app(flask_server, title, base_pathname, layout, register_callbacks_funcs, dash_debug, dash_auto_reload, external_stylesheets= None):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dash_app = Dash(
        __name__,
        server=flask_server,
        url_base_pathname=f'/{base_pathname}/',
        assets_folder=get_root_path(__name__) + '/static/',
        meta_tags=[meta_viewport],
        external_stylesheets=external_stylesheets,
        # external_scripts=[]
    )

    # auth = dash_auth.BasicAuth(
    #     my_dash_app,
    #     VALID_USERNAME_PASSWORD_PAIRS
    # )


    with flask_server.app_context():
        my_dash_app.title = title
        my_dash_app.layout = layout
        my_dash_app.css.config.serve_locally = True
        my_dash_app.enable_dev_tools(debug=dash_debug, dev_tools_hot_reload=dash_auto_reload)
        if register_callbacks_funcs:
            for call_back_func in register_callbacks_funcs:
                call_back_func(my_dash_app)

        @my_dash_app.server.before_request
        def restrict_access():
            public_routes = ['/meta_sam2/', '/table/', '/login/', '/signup/', '/']
            current_path = request.path

            #only public routes can access without logging in
            if any(current_path.startswith(route) for route in public_routes):
                return  

            #if login successful
            if current_user.is_authenticated:
                return
    
            return flask.redirect(url_for('main.login'))


            
def register_blueprints(server):
    from main_app.routes import server_bp
    server.register_blueprint(server_bp)
