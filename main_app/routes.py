from flask import Blueprint, render_template, request, redirect, url_for, flash
from main_app.dash_shared import shared_dash_nav_links
from flask_login import login_user, logout_user, login_required, current_user
from main_app.classes.student import Student
from main_app.extensions import db

server_bp = Blueprint('main', __name__)

@server_bp.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html', dash_url='/login/')

@server_bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    return render_template('signup.html', dash_url='/signup/')


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

@server_bp.route('/')
def index():
    students = Student.query.all()
    return render_template('student_index.html', students=students)


@server_bp.route('/<int:student_id>/edit/', methods=('GET', 'POST'))
def edit(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        student.username = username
        student.password = password

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('student_edit.html', student=student)

@server_bp.route('/student/<int:student_id>', methods=['GET'])
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student_detail.html', student=student)

@server_bp.post('/<int:student_id>/delete/')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('main.index'))


