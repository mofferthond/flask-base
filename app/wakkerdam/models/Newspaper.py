from app import db
from datetime import datetime

class Newspaper(db.Model):
    __tablename__ = "newspapers"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _game = db.relationship("Game")
    _gameId = db.Column("game", db.Integer, db.ForeignKey("games.id"))
    _date = db.Column("date", db.String(10))


    # referenced
    _articles = db.relationship("Article")

    def __init__(self, game, date=datetime.now().strftime("%y-%m-%d")):
        self.setGame(game)
        self.setDate(date)

    def getId(self):
        return self._id
    
    def getDate(self):
        return self._date

    def getDateFormatted(self):
        date = self.getDate()
        year, month, day = int(date[:4]), int(date[5:7]), int(date[8:])
        return datetime(year, month, day).strftime("%d %B %y")

    def setDate(self, date):
        self._date = date

    def getGame(self):
        return self._game

    def setGame(self, game):
        self._game = game   