from alfred_server import app, db
from models.build import Build
from models.project import Project
from models.result import Result
from models.test import Test
from models.test_run import TestRun

with app.app_context():
    db.init_app(app)

    db.drop_all()
    db.create_all()

    project = Project('Adco')
    build = Build(build_nr=1, project_id=project.id)
    tr = TestRun(status="Bla")

    project.builds.append(build)
    build.test_runs.append(tr)

    # test1 = Test(name="test_pass")
    # test2 = Test(name="test_fail")

    db.session.add(project)
    db.session.add(build)
    db.session.add(tr)
    # db.session.add(test1)
    # db.session.add(test2)
    db.session.flush()

    # result1 = Result(test_run_id=tr.id, test_id=test1.id, status="pass")
    # result2 = Result(test_run_id=tr.id, test_id=test2.id, status="fail")
    #
    # db.session.add(result1)
    # db.session.add(result2)

    db.session.commit()
