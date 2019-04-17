from slackbot.bot import respond_to
from slackbot.bot import listen_to
from .db import DB

class DBController:

    def __init__(self):
        self.db = DB()

    def initializeDB(self, dbName):
        self.db.connect(dbName)

    def disconnect(self):
        self.db.disconnect()
