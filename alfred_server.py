from flask import Flask, render_template, make_response, request, jsonify

from database import db, get_or_create
from models.build import Build
from models.result import Result
from models.test_run import TestRun
from models.test import Test
from models.project import Project

# Blueprints
from api.api import api

app = Flask(__name__)
app.config.from_pyfile('flask.cfg')
app.register_blueprint(api)
dtb = db.init_app(app)



@app.route('/')
def index():
    all_builds = Build.query.all()
    return render_template('index.html', title='Alfred', builds=all_builds)


@app.route('/builds', methods=['GET'])
def get_builds():
    build_list = []
    builds = Build.query.all()
    for build in builds:
        build_list.append(
            {
                'build_nr': build.build_nr,
                'created': build.created,
            }
        )

    return jsonify(Builds=build_list)


@app.route('/builds', methods=['POST'])
def create_build():
    payload = request.json
    build_nr = payload.get("build_nr")
    comment = payload.get("comment")

    build = get_or_create(db.session, Build, project_id=1, build_nr=build_nr)
    build.comment = comment
    db.session.commit()
    return jsonify(build_nr=build.build_nr, comment=build.comment), 201

@app.route('/builds/<build_nr>', methods=['PATCH'])
def update_build(build_nr):
    build = Build.query.get(build_nr)
    payload = request.json
    build.comment = payload.get("comment")
    db.session.commit()
    return jsonify(build_nr=build.build_nr), 200


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


@app.route('/tests/<test_run_id>', methods=['POST'])
def save_test_list(test_run_id):
    test_run = TestRun.query.get(test_run_id)

    test_names = request.json

    for test_name in test_names:
        test = get_or_create(db.session, Test, name=test_name)
        db.session.add(test)
        result = Result(test_run.id, test.id, status="Not run")
        db.session.add(result)

    db.session.commit()
    response = make_response('{{"test_added": {}}}'.format(len(test_names)))
    response.headers['Content-Type'] = 'application/json'
    return response



if __name__ == '__main__':
    host = '0.0.0.0'
    port = app.config['PORT']
    app.run(host=host, port=port, threaded=True, debug=True)
