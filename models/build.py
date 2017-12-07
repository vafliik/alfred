from datetime import datetime

from database import db

class Build(db.Model):

    __tablename__ = "build"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    number = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime)

    test_runs = db.relationship('TestRun', backref='build', lazy=True)

    def __init__(self, number, created=None):
        self.number = number
        self.created = created or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return 'Build({})'.format(self.number)
