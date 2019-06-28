from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Pet(db.Model):
    
    __tablename__ = 'pets'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(20),
        nullable=False
    )

    species = db.Column(
        db.String(20),
        nullable=False
    )

    photo_url = db.Column(
        db.Text,
    )

    age = db.Column(
        db.Integer,
        nullable=False
    )

    notes = db.Column(
        db.Text,
    )

    available = db.Column(
        db.Boolean,
        default=True
    ) 

    def __repr__(self):
        p = self
        return f"<Pet {p.id} {p.name} {p.species} {p.age} {p.available}>"
