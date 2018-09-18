from flask import Flask, render_template, make_response, request, jsonify, abort, send_from_directory
from flask_googlecharts import GoogleCharts, BarChart, LineChart

from database import db, get_or_create
from models.build import Build
from models.result import Result
from models.test_run import TestRun
from models.test import Test
from models.project import Project

from flask_apidoc import ApiDoc

# Blueprints
from api.api import api, get_project_by_id_or_name
from demo.demo import demo

app = Flask("alfred")

app.config.from_pyfile('flask.cfg')


# allow routes like /projects as well as /projects/
app.url_map.strict_slashes = False

app.register_blueprint(api)
app.register_blueprint(demo)

dtb = db.init_app(app)

doc = ApiDoc(app=app)
charts = GoogleCharts(app)


@app.route('/')
@app.route('/projects')
def index():
    pass_chart = LineChart("pass_chart", options={'colors': ['green', 'red'], 'curveType': 'function', 'legend': {'position': 'none'}})
    pass_chart.add_column("number", "Day")
    pass_chart.add_column("number", "Pass")
    pass_chart.add_column("number", "Fail")
    pass_chart.add_rows([["1", 62, 30],
                            ["2", 60, 32],
                            ["3", 36, 56],
                            ["4", 33, 53],
                            ["5", 79, 0]])

    charts.register(pass_chart)

    fail_chart = LineChart("fail_chart", options={'curveType': 'function', 'legend': {'position': 'none'}})
    fail_chart.add_column("number", "Day")
    fail_chart.add_column("number", "Pass")
    fail_chart.add_column("number", "Fail")
    fail_chart.add_rows([["1", 53, 10],
                            ["2", 70, 22],
                            ["3", 36, 56],
                            ["4", 10, 63],
                            ["5", 0, 85]])

    charts.register(fail_chart)

    projects = Project.query.all()
    return render_template('index.html', title='Home', projects=projects)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/projects/<int:project_id>/builds', methods=['GET'])
@app.route('/projects/<string:project_name>/builds', methods=['GET'])
def get_project(project_id=None, project_name=None):
    project = get_project_by_id_or_name(project_id, project_name)
    if not project:
        abort(404)
    return render_template('project.html', title='Project', project=project)


@app.route('/projects/<int:project_id>/builds/<build_nr>/runs', methods=['GET'])
@app.route('/projects/<string:project_name>/builds/<build_nr>/runs', methods=['GET'])
def get_build(build_nr, project_id=None, project_name=None):
    project = get_project_by_id_or_name(project_id, project_name)
    build = Build.query.filter_by(project_id=project.id, build_nr=build_nr).first_or_404()
    return render_template('build.html', title='Build', build=build, project=project)


@app.route('/projects/<int:project_id>/builds/<build_nr>/runs/<test_run_id>/results', methods=['GET'])
@app.route('/projects/<string:project_name>/builds/<build_nr>/runs/<test_run_id>/results', methods=['GET'])
def get_run(build_nr, test_run_id, project_id=None, project_name=None):
    project = get_project_by_id_or_name(project_id, project_name)
    build = Build.query.filter_by(project_id=project.id, build_nr=build_nr).first_or_404()
    test_run = TestRun.query.filter_by(id=test_run_id, build_nr=build_nr).first_or_404()
    test_results = Result.query.filter_by(test_run_id=test_run_id).join(Test, Test.id == Result.test_id).all()
    return render_template('test_run.html', title='Test Run', build=build, project=project, test_run=test_run,
                           test_results=test_results)


@app.route('/report/<test_run_id>', methods=['GET'])
def test_run_results(test_run_id):
    # test_run = TestRun.query.get(test_run_id)
    test_run_results = Result.query.filter(Result.test_run_id == test_run_id).all()

    return render_template('report.html',
                           test_run_id=test_run_id,
                           results=test_run_results,
                           )


@app.route('/test-run/start/<build_nr>', methods=['POST'])
def start_test_run(build_nr):
    build = get_or_create(db.session, Build, project_id=1, build_nr=build_nr)
    test_run = TestRun(status="running", comment="Automatic run")
    build.test_runs.append(test_run)

    db.session.add(build)
    db.session.add(test_run)
    db.session.commit()

    response = make_response('{{"test_run_id": {}}}'.format(test_run.id))
    response.headers['Content-Type'] = 'application/json'
    return response

#  Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    host = '0.0.0.0'
    port = app.config['PORT']
    app.run(host=host, port=port, threaded=True, debug=True)
