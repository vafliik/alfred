from database import db

class Test(db.Model):

    __tablename__ = "test"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    name = db.Column(db.String)

    results = db.relationship('Result', backref='test', lazy=True)

    def __init__(self, project_id, name):
        self.project_id = project_id
        self.name = name

    def __repr__(self):
        return 'Test({})'.format(self.name)
