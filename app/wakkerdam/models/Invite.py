from app import db

class Invite(db.Model):
    __tablename__ = 'invites'
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _game = db.relationship("Game")
    _gameId = db.Column("gameId", db.Integer, db.ForeignKey("games.id"))
    _user = db.relationship("User")
    _userId = db.Column("UserId", db.Integer, db.ForeignKey("users.id"))


    def __init__(self, game, user):
        self.setGame(game)
        self.setUser(user)
    
    def getId(self):
        return self._id

    def getGame(self):
        return self._game

    def setGame(self, game):
        self._game = game

    def getUser(self):
        return self._user
    
    def setUser(self, user):
        self._user = user
