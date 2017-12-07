from database import db

class Test(db.Model):

    __tablename__ = "test"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Test({})'.format(self.name)
