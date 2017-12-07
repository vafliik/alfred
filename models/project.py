from database import db

class Project(db.Model):

    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    builds = db.relationship('Build', backref='project', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Project({})'.format(self.name)
