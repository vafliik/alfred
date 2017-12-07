from database import db


class Result:

    def __init__(self, test_run_id, test_id, status):
        self.test_run_id = test_run_id
        self.test_id = test_id
        self.status = status

    def __repr__(self):
        return 'Result({})'.format(self.status)

    # "helper" table
    results = db.Table("results",
                       db.metadata,
                       db.Column("id", db.Integer, primary_key=True),
                       db.Column("test_run_id", db.Integer, db.ForeignKey("test_run.id")),
                       db.Column("test_id", db.Integer, db.ForeignKey("test.id")),
                       db.Column("status", db.String)
                       )
    # # unique index of hippie_id and dog_id
    # db.Index("love", dogs.c.hippie_id, dogs.c.dog_id, unique=True)
