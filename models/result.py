from database import db


class Result(db.Model):

    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    test_run_id = db.Column(db.Integer, db.ForeignKey('test_run.id'))
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    status = db.Column(db.String)


    def __init__(self, test_run_id, test_id, status):
        self.test_run_id = test_run_id
        self.test_id = test_id
        self.status = status

    def __repr__(self):
        return 'Result({})'.format(self.status)
