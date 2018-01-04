from flask import Blueprint, render_template, current_app
from flask_googlecharts import GoogleCharts, BarChart

demo = Blueprint("demo", "demo", url_prefix="/demo", template_folder='templates')


@demo.route('/', methods=['GET'])
def index():
    return render_template('demo/index.html', title='Demo Home')
