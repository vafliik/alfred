from database import db
from .result import Result

class TestRun(db.Model):

    __tablename__ = "test_run"

    id = db.Column(db.Integer, primary_key=True)
    build_id = db.Column(db.Integer, db.ForeignKey('build.id'))
    number = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime)
    comment = db.Column(db.String)

    results = db.relationship('Test', secondary=Result.results, backref='results', lazy=True)

    def __init__(self, number, created, comment=None):
        self.number = number
        self.created = created
        self.comment = comment

    def __repr__(self):
        return 'Test Run({})'.format(self.number)
