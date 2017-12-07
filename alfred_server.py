from flask import Flask, render_template, make_response, request

from database import db
from models.build import Build
from models.result import Result
from models.test_run import TestRun
from models.test import Test
from models.project import Project

app = Flask(__name__)
app.config.from_pyfile('flask.cfg')
dtb = db.init_app(app)


@app.route('/')
def index():
    all_builds = Build.query.all()
    return render_template('index.html', title='Alfred', builds=all_builds)


@app.route('/report/<test_run_id>')
def test_run_results(test_run_id):
    # test_run = TestRun.query.get(test_run_id)
    test_run_results = Result.query.filter(Result.test_run_id == test_run_id).all()

    return render_template('report.html',
                           test_run_id=test_run_id,
                           results=test_run_results,
                           )


@app.route('/report/<build_nr>', methods=['POST'])
def store_report(build_nr):

    build = get_or_create(db.session, Build, number=build_nr)
    test_run = TestRun(comment="Automatic run")
    build.test_runs.append(test_run)

    db.session.add(build)
    db.session.add(test_run)

    test_names=request.json

    for test_name in test_names:
        test = get_or_create(db.session, Test, name=test_name)
        db.session.add(test)
        result = Result(test_run.id, test.id, status="Not run")
        db.session.add(result)


    db.session.commit()
    response = make_response('{"success": true}')
    response.headers['Content-Type'] = 'application/json'
    return response


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


if __name__ == '__main__':
    host = '0.0.0.0'
    port = app.config['PORT']
    app.run(host=host, port=port, threaded=True, debug=True)
