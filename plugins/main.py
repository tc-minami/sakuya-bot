from slackbot.bot import respond_to
from slackbot.bot import default_reply
from slackbot.bot import listen_to
from .dbController import DBController

dbController = DBController()

#DB SETTINGS
__DB_NAME = "mainDB.db"

@respond_to(".*")
def respondYesIam(message):
    message.reply("お呼びでしょうか旦那様")

@listen_to("^[Dd][Bb][\s　]+[Ss]tart[\s　]*$")
def startDB(message):
    dbController.initializeDB(__DB_NAME)
    message.reply("DB " + __DB_NAME + " を初期化しました。")

@listen_to("^[Dd][Bb][\s　]+[Ss]top[\s　]*$")
def stopDB(message):
    dbController.disconnect()
    message.reply("DB " + __DB_NAME + " を終了しました。")
