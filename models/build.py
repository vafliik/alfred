from datetime import datetime

from database import db

class Build(db.Model):

    __tablename__ = "build"

    build_nr = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    created = db.Column(db.DateTime)
    comment = db.Column(db.String)

    test_runs = db.relationship('TestRun', backref='build', lazy=True)

    def __init__(self, build_nr, project_id, created=None, comment=None):
        self.build_nr = build_nr
        self.project_id = project_id
        self.created = created or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.comment = comment

    def __repr__(self):
        return '<Build({})>'.format(self.build_nr)
