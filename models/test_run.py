from datetime import datetime

from database import db

class TestRun(db.Model):

    __tablename__ = "test_run"

    id = db.Column(db.Integer, primary_key=True)
    build_id = db.Column(db.Integer, db.ForeignKey('build.id'))
    created = db.Column(db.DateTime)
    comment = db.Column(db.String)

    results = db.relationship('Result', backref='test_run', lazy=True)

    def __init__(self, created=None, comment=None):
        self.created = created or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.comment = comment

    def __repr__(self):
        return 'Test Run({})'.format(self.id)
