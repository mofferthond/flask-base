from app import db
from app.wakkerdam.models.Actor import Dead

class Player(db.Model):
    __tablename__ = "players"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _user = db.relationship("User", back_populates="_players")
    _userId = db.Column("userId", db.Integer, db.ForeignKey('users.id'))
    _game = db.relationship("Game")
    _gameId = db.Column("gameId", db.Integer, db.ForeignKey("games.id"))

    # referenced
    _chatters = db.relationship("Chatter")
    _actors = db.relationship("Actor")

    def __init__(self, user, game):
        self.setUser(user)
        self.setGame(game)
    
    def getId(self):
        return self._id

    def getUser(self):
        return self._user
    
    def setUser(self, user):
        self._user = user

    def getGame(self):
        return self._game

    def setGame(self, game):
        self._game = game

    def getChatters(self):
        return self._chatters
    
    def getActors(self):
        return self._actors

    def getActiveActors(self):
        result = []
        for actor in self.getActors():
            if actor.isActive():
                result.append(actor)
        return result

    def isDead(self):
        for actor in self.getActiveActors():
            if isinstance(actor, Dead):
                return True
        return False