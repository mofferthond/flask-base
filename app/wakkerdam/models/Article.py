from app import db

class Article(db.Model):
    __tablename__ = "articles"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _text = db.Column("text", db.String(1000))
    _publisher = db.Column("publisher", db.String(50))
    _playerCreated = db.relationship("Player")
    _playerCreatedId = db.Column("playerCreatedId", db.Integer, db.ForeignKey("players.id"))
    _newspaper = db.relationship("Newspaper")
    _newspaperId = db.Column("newspaperId", db.Integer, db.ForeignKey("newspapers.id"))
    

    def __init__(self, text, publisher, playerCreated, newspaper):
        self.setText(text)
        self.setPublisher(publisher)
        self.setPlayerCreated(playerCreated)
        self.setNewspaper(newspaper)

    def getId(self):
        return self._id

    def getText(self):
        return self._text

    def setText(self, text):
        self._text = text

    def getPublisher(self):
        return self._publisher

    def setPublisher(self, publisher):
        self._publisher = publisher

    def getPlayerCreated(self):
        return self._playerCreated

    def setPlayerCreated(self, playerCreated):
        self._playerCreated = playerCreated

    def getNewspaper(self):
        return self._newspaper

    def setNewspaper(self, newspaper):
        self._newspaper = newspaper