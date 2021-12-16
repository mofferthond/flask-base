from app import db
from app.wakkerdam.models import Dead

class Player(db.Model):
    __tablename__ = "players"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _user = db.relationship("User", back_populates="_players")
    _userId = db.Column("userId", db.Integer, db.ForeignKey('users.id'))
    _game = db.relationship("Game")
    _gameId = db.Column("gameId", db.Integer, db.ForeignKey("games.id"))
    _character = db.relationship("Character")
    _characterId = db.Column("characterId", db.Integer, db.ForeignKey("characters.id"))

    # referenced
    _chatters = db.relationship("Chatter")

    def __init__(self, user, game, character):
        self.setUser(user)
        self.setGame(game)
        self.setCharacter(character)
    
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
    
    def getCharacter(self):
        return self._character
    
    def setCharacter(self, character):
        self._character = character

    def getChatters(self):
        return self._chatters

    def isDead(self):
        return isinstance(self.getCharacter(), Dead)