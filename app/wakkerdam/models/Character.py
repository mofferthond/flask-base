from app import db

"""

I chose for a Single Table Inheritance database structure performance wise. 
It's not the best design wise but for heavy use I don't want to always have to load two tables.
More of this on
https://docs.sqlalchemy.org/en/14/orm/inheritance.html

"""



class Character(db.Model):
    __tablename__ = "characters"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _name = db.Column("name", db.String(50))
    _description = db.Column("description", db.String(2000))
    _shortDescription = db.Column("shortDescription", db.String(500))
    _tag = db.Column("tag", db.String(50))
    _isWolf = db.Column("isWolf", db.Boolean)

    # referenced
    _players = db.relationship("Player")
    # _actionTypes = db.relationship("ActionType")

    def __init__(self, name, description, shortDescription, tag, isWolf):
        self.setName(name)
        self.setDescription(description)
        self.setShortDescription(shortDescription)
        self.setTag(tag)
        self.setIsWolf(isWolf)

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getShortDescription(self):
        return self._shortDescription

    def setShortDescription(self, shortDescription):
        self._shortDescription = shortDescription

    def getTag(self):
        return self._tag
        
    def setTag(self, tag):
        self._tag = tag

    def getIsWolf(self):
        return self._isWolf

    def setIsWolf(self, isWolf):
        self._isWolf = isWolf

    def getPlayers(self):
        return self._players


class Wolf(Character):
    def __init__(self, name, description, shortDescription, tag):
        Character.__init__(self, name, description, shortDescription, tag, 1)

class Villager(Character):
    def __init__(self, name, description, shortDescription, tag):
        Character.__init__(self, name, description, shortDescription, tag, 0)

class Dead(Character):
    _wasCharacter = db.relationship("Character")
    _wasCharacterId = db.Column("wasCharacter", db.Integer, db.ForeignKey("characters.id"))
    def __init__(self, wasCharacter):
        _wasCharacter = wasCharacter

class regularWolf(Wolf):
    def __init__(self):
        Wolf.__init__(
            self,
            name="Wolf",
            description="Een gewone wolf. Deze wint als alle burgers uit het spel zijn. Verder heeft het geen bijzondere eigenschappen.",
            shortDescription="Gewone wolf",
            tag="wolf"
        )

class regularVillager(Villager):
    def __init__(self):
        Villager.__init__(
            self,
            name="Burger", 
            description="Een gewone burger. Deze wint als alle wolven uit het spel zijn. Verder heeft het geen bijzondere eigenschappen.", 
            shortDescription="Gewone burger", 
            tag="villager"
        )

class Detective(Villager):
    def __init__(self):
        Villager.__init__(
            self,
            name="Detective", 
            description="De detective is een burger die elke nacht twee spelers uit kan kiezen. Van deze spelers krijg je vervolgens te weten of ze in het zelfde kamp zitten. (Wolf & Wolf, Burger & Burger, stelletje)", 
            shortDescription="Kan 2 spelers vergelijken en zien of ze in het zelfde kamp zitten", 
            tag="detective"
        )

class Journalist(Villager):
    def __init__(self):
        Villager.__init__(
            self,
            name="Journalist", 
            description="De journalist kan van één krantenartikel per dag kijken of deze geschreven is door een wolf of door een burger.", 
            shortDescription="Kan van krantenartikelen kijken of deze door een wolf is geschreven", 
            tag="journalist"
        )