from app import db
from datetime import datetime
from app.wakkerdam.models.constants.Character import Character

"""

I chose for a Single Table Inheritance database structure performance wise. 
It's not the best design wise but for heavy use I don't want to always have to load two tables.
More of this on
https://docs.sqlalchemy.org/en/14/orm/inheritance.html

"""

CHARACTERS = {
    "wolf": {
        "name": "Wolf",
        "description": "Een gewone wolf. Deze wint als alle burgers uit het spel zijn. Verder heeft het geen bijzondere eigenschappen.",
        "shortDescription": "Gewone wolf",
        "alliance": "BAD",
        "tag": "wolf"   
    },
    "villager": {
        "name": "Burger",
        "description": "Een gewone burger. Deze wint als alle wolven uit het spel zijn. Verder heeft het geen bijzondere eigenschappen.",
        "shortDescription": "Gewone burger",
        "alliance": "GOOD",
        "tag": "villager"
    },
    "detective": {
        "name": "Detective",
        "description": "De detective is een burger die elke nacht twee spelers uit kan kiezen. Van deze spelers krijg je vervolgens te weten of ze in het zelfde kamp zitten. (Wolf & Wolf, Burger & Burger, stelletje)", 
        "shortDescription": "Kan 2 spelers vergelijken en zien of ze in het zelfde kamp zitten",
        "alliance": "GOOD",
        "tag": "detective"
    },
    "journalist": {
        "name": "Journalist",
        "description": "De journalist kan van één krantenartikel per dag kijken of deze geschreven is door een wolf of door een burger.", 
        "shortDescription": "Kan van krantenartikelen kijken of deze door een wolf is geschreven", 
        "alliance": "GOOD",
        "tag": "journalist"
    }
}



class Actor(db.Model):
    __tablename__ = "actors"
    __bind_key__ = None
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _character = db.relationship("Character")
    _characterId = db.Column("characterId", db.ForeignKey("characters.id"))
    _player = db.relationship("Player")
    _playerId = db.Column("playerId", db.Integer, db.ForeignKey("players.id"))
    _timeCreated = db.Column("timeCreated", db.Integer)
    _timeDeactivated = db.Column("timeDeactivated", db.Integer)
    _becameActor = db.relationship("Actor", remote_side=[_id], enable_typechecks=False)
    _becameActorId = db.Column("becameActorId", db.Integer, db.ForeignKey("actors.id"))

    # referenced
    _actions = db.relationship("Action")
    _wasActors = db.relationship("Actor", remote_side=[_becameActorId])

    def __init__(self, character, player, timeCreated=int(round(datetime.now().timestamp()))):
        self.setCharacter(character)
        self.setPlayer(player)
        self.setTimeCreated(timeCreated)

    def getCharacter(self):
        return self._character

    def setCharacter(self, character):
        self._character = character

    def getPlayer(self):
        return self._player

    def setPlayer(self, player):
        self._player = player

    def getTimeCreated(self):
        return self._timeCreated

    def setTimeCreated(self, timeCreated):
        self._timeCreated = timeCreated

    def getTimeDeactivated(self):
        return self._timeDeactivated

    def setTimeDeactivated(self, timeDeactivated):
        self._timeDeactivated = timeDeactivated

    def deactivate(self):
        if self.isActive():
            self.setTimeDeactivated(int(round(datetime.now().timestamp())))

    def isActive(self):
        if self._timeDeactivated == None:
            return True
        return False

    def getActions(self):
        return self._actions

    def declareDead(self, deadActor):
        self.deactivate()
        self._becameActor = deadActor

class Dead(Actor):
    def __init__(self, player):
        Actor.__init__(self, Character.query.filter_by(_tag="dead").first(), player)

class Villager(Actor):
    def __init__(self, player):
        Actor.__init__(self, Character.query.filter_by(_tag="villager").first(), player)

class Wolf(Actor):
    def __init__(self, player):
        Actor.__init__(self, Character.query.filter_by(_tag="wolf").first(), player)