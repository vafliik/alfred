from flask import Flask, render_template

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
    test_run_results = Test.query.join(TestRun.results).filter(TestRun.id==test_run_id).all()

    return render_template('report.html',
                           test_run_id=test_run_id,
                           results=test_run_results,
                           )

if __name__ == '__main__':
    db.mapper(Result, Result.results)
    host = '0.0.0.0'
    port = app.config['PORT']
    app.run(host=host, port=port, threaded=True, debug=True)