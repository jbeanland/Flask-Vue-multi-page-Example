from flask import render_template

from app.main import bp


@bp.route('/')
@bp.route('/index')
def bars():
    return render_template('index.html')


@bp.route('/about')
def sliders():
    return render_template('about.html')
