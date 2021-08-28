from database import db

class Imdb(db.EmbeddedDocument):
    imdb_id = db.StringField()
    rating = db.DecimalField()
    votes = db.IntField()

class Cast(db.DynamicEmbeddedDocument):
    pass

class Director(db.DynamicDocument):
    pass


class Movie(db.Document):
    title = db.StringField(required=True)
    year = db.IntField()
    rated = db.StringField()
    director = db.ReferenceField(Director)
    cast = db.EmbeddedDocumentListField(Cast)
    poster = db.FileField()
    imdb = db.EmbeddedDocumentField(Imdb)







