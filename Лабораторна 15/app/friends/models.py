from app import db


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Friends {self.name} {self.surname}"
