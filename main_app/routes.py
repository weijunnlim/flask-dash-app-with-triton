from flask import Blueprint, render_template, request, redirect, url_for, flash
from main_app.dash_shared import shared_dash_nav_links
from flask_login import login_user, logout_user, login_required, current_user
from main_app.forms.forms import LoginForm
from main_app.classes.user import User
import flask

server_bp = Blueprint('main', __name__)

@server_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #look up from user class
        user_data = User.get_by_username(form.username.data)
        
        if user_data and user_data.password == form.password.data:
            user = User(id=user_data.id, username=user_data.username, password=user_data.password)
            login_user(user)
            flask.flash('Logged in successfully.')

            next_url = request.args.get('next') or url_for('main.home_template')
            return redirect(next_url)
        else:
            flask.flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)


@server_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))


@server_bp.route('/home/')
def home_template():
    navbar = shared_dash_nav_links()
    user = {'username': current_user.username}
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

@server_bp.route('/meta_sam2/')
def meta_sam2_template():
    navbar = shared_dash_nav_links()
    return render_template('dash.html', dash_url='/meta_sam2/', navbar = navbar)



