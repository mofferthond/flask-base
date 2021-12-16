from app import db

class Chatter(db.Model):
    __tablename__ = "chatters"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _player = db.relationship("Player")
    _playerId = db.Column("playerId", db.Integer, db.ForeignKey("players.id"))
    _chat = db.relationship("Chat")
    _chatId = db.Column("chatId", db.Integer, db.ForeignKey("chats.id"))

    # referenced
    _messages = db.relationship("Message")
    _chatLogs = db.relationship("ChatLog")

    def __init__(self, player, chat):
        self.setPlayer(player)
        self.setChat(chat)

    def getId(self):
        return self._id

    def getPlayer(self):
        return self._player

    def setPlayer(self, player):
        self._player = player

    def getChat(self):
        return self._chat

    def setChat(self, chat):
        self._chat = chat

    def getMessages(self):
        return self._messages

    def getChatLogs(self):
        return self._chatLogs

